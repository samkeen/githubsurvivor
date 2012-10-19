# Sample configuration
# Copy this to config.py and edit as required.

config = {
    # Point this at the repo you want to report on.
    'github.repo': '99designs/githubsurvivor',

    # You'll need to create an OAuth token to access your repo.
    # See https://help.github.com/articles/creating-an-oauth-token-for-command-line-use
    'github.oauth_token': 'my-secret',

    # Your local Mongo database
    'db': 'githubsurvivor',

    # You can optionally provide a whitelist of users to display in the bug
    # leaderboards. Leave this empty to include all repo contributors.
    'leaderboard_users': (
        # 'harto',
        # 'dannymidnight',
        # 'alecsloman',
    ),

    # Whether to display the interactive debugger on error
    # Don't enable this in publicly-accessible environments
    'flask.debug': False,

    'flask.settings': {
        'host': '127.0.0.1',
        'port': 5000,
    }
}
