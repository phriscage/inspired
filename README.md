Inspired
================================

A Python flask application with a relational data store that provides content metadata and merchant retailers for consumer purchasing. SQLAlchemy is used for the ORM layer and Alembic for the database migrations and version control.


Diretory Structure
-------------------------

The application folder structure is defined below:

    lib/
        inspired/
            <version>/
                lib/
                    <object>/
                api/
                    <object>/
    www/
        templates/
            <object>/
        static/
            <object>/
    db/
        migrations/
            versions/
    tests/
        lib_tests/
            inspired_tests/
                <version>_tests/
                    lib_tests/
                        <object>_tests/
                    api_tests/
                        <object>_tests/
                

Quick Start
-------------------------

Create the database from the db/create.sql
    
    $ mysql -uroot -p < db/create.sql

Verify the Alembic database migrations complete successfully:

    $ cd db
    $ $ alembic upgrade head
    INFO  [alembic.migration] Context impl MySQLImpl.
    INFO  [alembic.migration] Will assume non-transactional DDL.

Execute ./lib/main.py to launch the API.

    $ ./lib/inspired/v1/api/main.py 
    * Running on http://0.0.0.0:8000/
    * Restarting with reloader

Execute ./www/main.py to launch the UI.

    $ ./www/main.py --port 8080
    * Running on http://0.0.0.0:8080/
    * Restarting with reloader


TODO
-------------------------

* Create tiered configuration file.
* ~~Create library unit tests.~~
* ~~Create api unit tests.~~
* Create Sphinx docs fotn additional methods are added.
* Create Ant build file for RPM.
