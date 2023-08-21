import sys

from auth.src.migrations.runner.composite import alembic_runner

alembic_runner(*sys.argv[1:])
