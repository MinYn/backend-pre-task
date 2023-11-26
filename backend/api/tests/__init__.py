from django import setup
import os
os.environ.setdefault("ENV_MODE", "test")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
setup()