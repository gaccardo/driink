from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DRIINK",
    settings_files=['settings.toml', '.secrets.toml'],
)
