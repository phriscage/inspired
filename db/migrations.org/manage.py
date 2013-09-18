#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../conf')
from inspired_config import SQLALCHEMY_DATABASE_URI
from inspired_config import SQLALCHEMY_MIGRATE_REPO

from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url=SQLALCHEMY_DATABASE_URI, repository=SQLALCHEMY_MIGRATE_REPO, 
        debug='False')
