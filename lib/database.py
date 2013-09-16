""" database handler """
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../conf')

from inspired_config import SQLALCHEMY_DATABASE_URI

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
