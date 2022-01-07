import os

from dynaconf import Dynaconf
from pyspark import SparkConf

ENVVAR_PREFIX = "WASP"
ENV_SWITCHER = "WASP_ENV"

default_settings_file = os.path.join(os.path.dirname(__file__), "settings_default.toml")
private_settings_file = os.path.join(os.path.dirname(__file__), "settings_private.toml")

settings = Dynaconf(
    envvar_prefix=ENVVAR_PREFIX,
    preload=[default_settings_file],
    settings_files=["settings.toml", ".secrets.toml"],
    includes=[private_settings_file],
    merge_enabled=True,
    environments=True,
    env_switcher=ENV_SWITCHER,
)
"""Settings for the app."""


def load_spark_config():
    spark_conf = SparkConf()
    for (key, val) in settings.swarm.sparkconfig:
        spark_conf.set(key, val)
    return spark_conf
