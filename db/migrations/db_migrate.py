#!/usr/bin/env python
""" db_migrate is an extended version of the db_migrate.py script from 
    Miguel Grinberg's sqlalchemy blog. It will check a given model against
    an existing database table and create a new migration if needed via the
    migrate.versioning api.
    http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
"""
import sys
import os
import imp
import argparse
from migrate.versioning import api
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../conf')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired_config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO


def create_migration(model, name):
    """ create a new migration for a specific model by comparing the model 
        against the table in the database.
    Args:
        model (str): model name
        name (str): name of the migration
    Raises:
        ValueError
    """

    migration_file = (SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_%s.py' % (
        api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) + 1, 
        name))
    try:
        __import__(model)
    except ImportError as error:
        raise error
    tmp_module = imp.new_module(model)
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI, 
        SQLALCHEMY_MIGRATE_REPO)
    #print old_model
    exec old_model in tmp_module.__dict__
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, 
        SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, Base.metadata)
    if len(script) == 498: 
        raise ValueError("No change in migration model: '%s'" % model)
    open(migration_file, "wt").write(script)
    #api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print "New migration saved: '%s'" % migration_file
    #print "Current database version: '%s'" + str(api.db_version(
            #SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", dest="model", type=str,
        help="sqlalchemy model, I.E: 'sqlalchemy.model:Model", required=True)
    parser.add_argument("-n", "--name", dest="name", type=str,
        help="migration name", required=True)
    args = parser.parse_args()
    create_migration(args.__dict__['model'], args.__dict__['name'])
    

