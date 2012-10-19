"""
Report generation helpers.

The functions defined here take some date within a reporting period and
return the start and end dates of that period.
"""

from collections import namedtuple
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, FR, SU

Period = namedtuple('Period', 'start end')

### Weekly reporting

def weekly_reporting_period(anchor, offset=0):
    # Find Sunday in the given week
    end = anchor + relativedelta(weeks=offset) + relativedelta(weekday=SU)
    return Period(end - relativedelta(weeks=1), end)

### Sprint reporting

# TODO: move these into configuration
sprint_start_weekday = FR
sprint_length_weeks = 2
first_sprint_week_of_year = 1

def sprint_end(anchor):
    # Find the next instance of the sprint start/end weekday
    # This will either be the end date of a sprint, or the equivalent
    # weekday partway through a sprint
    anchor = (anchor.date() + relativedelta(weekday=sprint_start_weekday))

    # Find 1-based sprint week number
    week_of_year = int(anchor.strftime('%U'))
    week_of_sprint = (week_of_year + first_sprint_week_of_year) % sprint_length_weeks + 1

    sprint_weeks_remaining = sprint_length_weeks - week_of_sprint
    return anchor + relativedelta(weeks=sprint_weeks_remaining)

def sprint_reporting_period(anchor, offset=0):
    end = sprint_end(anchor) + relativedelta(weeks=offset * sprint_length_weeks)
    return Period(end - relativedelta(weeks=sprint_length_weeks), end)

### Monthly reporting

def monthly_reporting_period(anchor, offset=0):
    # Find the first day in the given month
    start = anchor.replace(day=1) + relativedelta(months=offset)
    return Period(start, start + relativedelta(months=1))
