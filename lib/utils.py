import yaml
from datetime import datetime

def log(msg):
  now = datetime.now()
  now_str = now.strftime('%Y-%m-%d %H:%M:%S')
  print(f'[app][{now_str}] {msg}')

def load_settings():
  with open('./settings.yml', 'r') as stream:
    return yaml.safe_load(stream)

def is_iterable(obj):
  try:
    iter(obj)
    return True
  except TypeError:
    return False
