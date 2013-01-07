"""
Synchronises local database with GitHub.
"""

import argparse
import itertools

import github

from survivor import config, init
from survivor.models import User, Issue

def create_user(github_user):
    "Creates a `survivor.models.User` from a `github.NamedUser`."
    user = User(github_id=github_user.id)
    for k in ('login', 'name', 'email', 'avatar_url', 'gravatar_id'):
        setattr(user, k, getattr(github_user, k))
    return user.save()

def get_or_create_user(github_user):
    """
    Get or create a `survivor.models.User` from a partially-loaded
    `github.NamedUser`.
    """
    try:
        return User.objects.get(login=github_user.login)
    except User.DoesNotExist:
        return create_user(github_user)

# Map primitive survivor.models.Issue attrs to github.Issue attrs
issue_attr_map = {
    'number': 'number',
    'title': 'title',
    'state': 'state',
    'opened': 'created_at',
    'closed': 'closed_at',
    'updated': 'updated_at',
    'url': 'html_url',
    }

def create_issue(github_issue):
    "Creates a `survivor.models.Issue` from a `github.Issue`."
    issue = Issue(**dict((issue_attr, getattr(github_issue, github_attr))
                         for issue_attr, github_attr in issue_attr_map.items()))

    issue.reporter = get_or_create_user(github_issue.user)
    if github_issue.assignee:
        issue.assignee = get_or_create_user(github_issue.assignee)

    # TODO comments, labels

    return issue.save()

def sync(types, verbose=False):
    "Refresh selected collections from GitHub."

    auth_token = config['github.oauth_token']
    account_name, repo_name = config['github.repo'].split('/')

    account = github.Github(auth_token).get_user(account_name)

    if 'users' in types:
        User.drop_collection()
        # FIXME: can this come from config?
        for github_user in account.get_repo(repo_name).get_collaborators():
            try:
                user = create_user(github_user)
            except:
                print 'Error creating user: %s' % github_user
                raise
            if verbose: print 'created user: %s' % user.login

    if 'issues' in types:
        Issue.drop_collection()
        repo = account.get_repo(repo_name)
        issues = itertools.chain(repo.get_issues(state='open'),
                                 repo.get_issues(state='closed'))
        for gh_issue in issues:
            try:
                issue = create_issue(gh_issue)
            except:
                print 'Error creating %s' % gh_issue
                raise
            if verbose: print 'created issue: %s' % issue.title

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Synchronises local DB with GitHub')
    argparser.add_argument('model', nargs='*', help='model types to sync')
    argparser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='verbose output')

    args = argparser.parse_args()
    types = args.model or ('users', 'issues')
    
    init()
    sync(types, args.verbose)
