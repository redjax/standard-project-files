# Alembic Notes

* Install `alembic` with `pip install alembic` (or some equivalent package install command)
* Initialize `alembic`
  * If using a `src` directory, i.e. `src/app`, initialize `alembic` at `src/app/alembic`
    * `alembic init src/app/alembic`
  * If using a "flat" repository, simply run `alembic init alembic`
  * **NOTE**: You can use any name for the directory instead of "alembic." For instance, another common convention is to initialize `alembic` with `alembic init migrations`
    * Whatever directory name you choose, use that throughout these instructions where you see references to the `alembic` init path
* Edit the `alembic.ini` file
  * Change `script_location` to the path you set for alembic, i.e. `src/app/alembic`
  * Edit `prepend_sys_path`, set to `src/app`
    * This adds the script's path to `alembic` can do things like importing your app's config, loading the SQLAlchemy `Base` object, etc

```
## alembic.ini

[alembic]

script_location = src/app/alembic

...

prepend_system_path = src/app

...

```

* Edit the `alembic` `env.py` file, which should be in `src/app/alembic` (or whatever path you initialized `alembic` in)
  * If you initialized a SQLAlchemy database URI string (of type `sqlalchemy.URL`), you can import it in `env.py`, or you can create a new one:

```
## src/app/alembic.py

...

import sqlalchemy as sa

## Using a SQLite example
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
```
