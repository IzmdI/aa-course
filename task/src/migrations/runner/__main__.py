import sys

from task.src.migrations.runner.composite import alembic_runner

alembic_runner(*sys.argv[1:])
