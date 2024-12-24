import os
from sqlalchemy import create_engine
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from alembic import command


def get_alembic_config():
    """Prepare the Alembic configuration with dynamic database URL."""
    db_path = os.path.expanduser("~/.local/share/driink/driink.db")
    alembic_cfg = Config("driink/alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    return alembic_cfg


def has_pending_migrations():
    """Check if there are unapplied migrations."""
    alembic_cfg = get_alembic_config()
    script = ScriptDirectory.from_config(alembic_cfg)

    db_path = os.path.expanduser("~/.local/share/driink/driink.db")
    engine = create_engine(f"sqlite:///{db_path}")
    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()
        latest_rev = script.get_current_head()

    return current_rev != latest_rev


def ensure_migrations():
    """Run migrations if there are pending migrations."""
    if has_pending_migrations():
        print("database requires updates")
        alembic_cfg = get_alembic_config()
        command.upgrade(alembic_cfg, "head")
        print("database update ready")