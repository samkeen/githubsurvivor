"""
Jinja2 template helpers
"""

def format_datetime(datetime, fmt=None):
    "Arbitrary datetime formatting."
    return datetime.strftime(fmt) if fmt else datetime.isoformat()

def register_helpers(app):
    "Register filters and functions in the Jinja2 environment."
    app.jinja_env.filters['format_datetime'] = format_datetime
