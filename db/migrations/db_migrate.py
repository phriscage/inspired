#!/usr/bin/env python
""" db_migrate is an extended version of the db_migrate.py script from 
    Miguel Grinberg's sqlalchemy blog. It will check a given model against
    an existing database table and create a new migration if needed via the
    migrate.versioning api.
    http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
"""
from __future__ import absolute_import
import sys
import os
import imp
import inspect
import re
import argparse
from migrate.versioning import api
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../conf')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../')
from database import Base
from inspired_config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO


def create_migration(directory, name, create=False):
    """ create a new migration for all model(s) within a given directory
        and subdirectory by comparing the model(s) against the table
        in the database.
    Args:
        directory (str): directory name
        name (str): name of the migration
        create (bol): create flag
    Raises:
        ImportError
    """

    directory = '../../lib/inspired/v1/lib'
    if not os.path.isdir(directory):
        raise ValueError("'%s' is not a directory" % directory)

    for root, dir_names, file_names in os.walk(directory):
        for file in file_names:
            if re.search(r'^[a-z]+\.py$', file):
                tmp_model = '.'.join([value for value in os.path.join(root, 
                    file)[:-3].split('/') if value != '..'])
                try:
                    module = __import__(tmp_model)
                except ImportError as error:
                    raise error
    old_models = api.create_model(SQLALCHEMY_DATABASE_URI, 
        SQLALCHEMY_MIGRATE_REPO)
    ## just need to create a dummy tmp_module with 'meta' to generate the
    ## update_script
    tmp_module = imp.new_module(directory)
    exec old_models in tmp_module.__dict__
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, 
        SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, Base.metadata)
    if len(script) == 498: 
        raise ValueError("No change in migration directory: '%s'" % directory)
    if create:
        migration_file = (SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_%s.py' % (
            api.db_version(SQLALCHEMY_DATABASE_URI, 
            SQLALCHEMY_MIGRATE_REPO) + 1, name))
        open(migration_file, "wt").write(script)
        #api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        print "New migration saved: '%s'" % migration_file
    else:
        print script
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", dest="directory", type=str,
        help="sqlalchemy model parent directory", required=True)
    parser.add_argument("-n", "--name", dest="name", type=str,
        help="migration name", required=True)
    parser.add_argument("-c", "--create", 
        help="create the migration file", action='store_true')
    kwargs = parser.parse_args().__dict__
    create_migration(**kwargs)
    

