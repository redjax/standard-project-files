"""WARNING: This is only a portion of a full alembic env.py file!

Add this code where appropriate in your initialized alembic/env.py file.
"""

...

DB_URI: sa.URL = sa.URL.create(
    drivername="sqlite+pysqlite",
    username=None,
    password=None,
    host=None,
    port=None,
    database="database.sqlite"
)

...

## Set config's sqlalchemy.url value, after "if config.config_filename is not None:"
config.set_main_option(
    "sqlalchemy.url",
    ## Use .render_as_string(hide_password=False) with sqlalchemy.URL objects,
    #  otherwise database password will be "**"
    DB_URI.render_as_string(hide_password=False)
)

...

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app.module.models import SomeModel  # Import project's SQLAlchemy table classes
from app.module.database import Base  # Import project's SQLAlchemy Base object

target_metadata = Base().metadata  # Tell Alembic to use the project's Base() object

...
