import os
import mongoengine

# Global configuration
config = {}

# Database connection
db = None

def app_root():
    # :-(
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

_inited = False

def parse_config(path=None):
    env = {'config': None}
    execfile(path or os.path.join(app_root(), 'config.py'), env)
    return env['config']

def init(config_path=None):
    global _inited, db

    if _inited: raise Exception('already initialised')

    # Configuration
    config.update(parse_config(config_path))

    # Database
    db_name = config['db']
    conn = mongoengine.connect(db_name, tz_aware=True)
    db = conn[db_name]

    _inited = True
