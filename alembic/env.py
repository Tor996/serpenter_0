import sys
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context
from models import Base, DATABASE_URL
# Add the root project directory to the sys.path
sys.path.append("..")


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Database URL
DATABASE_URL = "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/serpenter_db"


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Create a synchronous engine for Alembic
sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = sync_engine  # Use the synchronous engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
