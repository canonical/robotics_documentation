
# Migrate a `cos-registration-server` database from sqlite3 to postgresql

```{warning}
**Beta Notice**: {{COS_ROB}} is currently in `beta`.
Content and features may change,
and some functionality may be incomplete or experimental.
Feedback is welcome as we continue to improve.
```

The first version of `cos-registration-server` used
[SQLite3](https://sqlite.org/) as its database backend.

Starting with version `1/stable`, `cos-registration-server` now uses
[PostgreSQL](https://www.postgresql.org/) as its database backend
to enhance the performance,
reliability, and scalability.

This guide explains how to migrate an existing
`cos-registration-server` database from SQLite3 to PostgreSQL.

At the end of this process,
the `cos-registration-server` instance
will be using PostgreSQL as its database backend,
with all data migrated from the previous SQLite3 database.

## Am I concerned?

In order to determine if you need to follow this migration guide,
check if your existing `cos-registration-server` instance
is using SQLite3 as its database backend.

```bash
juju ssh --container cos-registration-server cos-registration-server/0 \
ls /server_data/db.sqlite3 \
&& echo "You should migrate" \
|| echo "No need to migrate"
```

This command checks if the SQLite3 database file exists,
and lets you know whether you need to migrate or not.

## Prerequisites

- A running instance of `cos-registration-server-k8s` using SQLite3.
- A running instance of `postgresql-k8s` or
a Juju deployment where you can deploy it.

## Export the SQLite3 database

First,
we retrieve all the data
from the SQLite3 database file from the existing `cos-registration-server` instance.

To do so,
we run `django` commands inside the container running our `cos-registration-server`:

```bash
juju ssh --container cos-registration-server cos-registration-server/0 \
DATABASE_BASE_DIR_DJANGO=/server_data/ \
/usr/bin/python3 \
/usr/lib/python3.10/site-packages/cos_registration_server/manage.py \
dumpdata   \
--natural-foreign \
--natural-primary \
--exclude contenttypes \
--exclude sessions \
--exclude admin.logentry
--indent 2 \
--output /tmp/data_export.json
```

```{note}
Everything happening on this `cos-registration-server` instance
after the dumpdata won't be included in the exported data,
and will be lost.
Make sure to stop any activity on the `cos-registration-server`
while performing this migration.
```

We've now exported all the data from the SQLite3 database file.
This file `data_export.json` contains all the data we need to migrate to PostgreSQL.

We now retrieve this file from
the `cos-registration-server` container to our local machine:

```bash
juju scp --container cos-registration-server \
cos-registration-server/0:/tmp/data_export.json data_export.json
```

We now have all the data from our previous deployment.

To make sure we won't reuse this old SQLite3 database by mistake,
we can move the SQLite3 database file from the `cos-registration-server` instance:

```bash
juju ssh --container cos-registration-server cos-registration-server/0 \
mv /server_data/db.sqlite3 /server_data/db.sqlite3.migrated
```

## Set up PostgreSQL

```{tip}
You can skip this step if you already have a Juju/Charm PostgreSQL instance running.
```

If no PostgreSQL instance is already available in the Juju model,
we can deploy the `postgresql-k8s` charm:

```bash
juju deploy postgresql-k8s postgresql --channel 14/stable --trust
```

## Import the data into the new PostgreSQL deployment

We refresh the instance of `cos-registration-server-k8s`,
pulling the latest release that includes PostgreSQL support:

```bash
juju refresh cos-registration-server \
--channel 1/stable
```

Then,
connect the `cos-registration-server` instance to the `postgresql` instance:

```bash
juju integrate postgresql cos-registration-server
```

### Import the database file inside the new container

We now copy the `data_export.json` file
available locally to the `cos-registration-server` instance:

```bash
juju scp --container cos-registration-server data_export.json cos-registration-server/0:/tmp/data_export.json
```

```{warning}
Note that we are importing the database file
inside the `cos-registration-server` instance,
and not the postgresql instance itself.

This is because we will use Django to load the data into PostgreSQL.
```

### Load the data into PostgreSQL

First,
we must retrieve the `DATABASE_URL` value
used by the `cos-registration-server` instance:

```bash
juju ssh cos-registration-server/0 \
PEBBLE_SOCKET=/charm/containers/cos-registration-server/pebble.socket \
/charm/bin/pebble plan \
| grep DATABASE_URL
```

This will output a line similar to:

```bash
      "DATABASE_URL": "postgres://username:password@hostname:port/databasename",
```

Copy the value of `DATABASE_URL` (the part between the quotes) and
replace `XXXXXXXXXX` in the command below.
Now we can use this value while loading the data with Django.

```bash
juju ssh --container cos-registration-server \
cos-registration-server/0 \
DATABASE_URL=XXXXXXXXXX SECRET_KEY_DJANGO=\$\(cat /server_data/secret_key\) \
/usr/bin/python3 \
/usr/lib/python3.10/site-packages/cos_registration_server/manage.py \
loaddata /tmp/data_export.json
```

All the data from the previous SQLite3 database is now imported into PostgreSQL.

Make sure to run proper tests with the new `cos-registration-server`
to ensure everything is working as expected.
