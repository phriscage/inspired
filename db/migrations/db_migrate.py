#!/usr/bin/env python
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
    """ create a new migration by comparing the existing model in the db """

    migration = (SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_%s.py' % (
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
    print "-" * 80
    print script
    open(migration, "wt").write(script)
    #api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print 'New migration saved as ' + migration
    print 'Current database version: ' + str(api.db_version(
            SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", dest="model", type=str,
        help="sqlalchemy model, I.E: 'sqlalchemy.model:Model", required=True)
    parser.add_argument("-n", "--name", dest="name", type=str,
        help="migration name", required=True)
    args = parser.parse_args()
    create_migration(args.__dict__['model'], args.__dict__['name'])
    

