import os
import sys
from logging.config import fileConfig
from dotenv import load_dotenv  # Import dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

load_dotenv()  # .env faylini yuklash

# Django loyihasi yo'lini qo'shish
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.base'  # 'config' loyiha sozlamalari papkasi nomi

from django.conf import settings
from django.apps import apps

def get_metadata():
    metadata = None
    apps.populate(settings.INSTALLED_APPS)

    for app_config in apps.get_app_configs():
        if hasattr(app_config, 'models_module'):
            for model in apps.get_models(app_config):
                if not model._meta.abstract:
                    if metadata is None:
                        metadata = model._meta.managed and model._meta.db_table is not None and model.objects.db
                    else:
                        metadata = metadata if metadata == model.objects.db else None
    return metadata

target_metadata = get_metadata()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.environ.get("DATABASE_URL")  # .env dan olish
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=os.environ.get("DATABASE_URL")  # .env dan olish
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            dialect_opts={"paramstyle": "named"},
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()