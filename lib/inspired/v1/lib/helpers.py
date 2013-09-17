""" model helpers used for each child model """
from sqlalchemy.orm import MapperExtension
import datetime

class BaseExtension(MapperExtension):
    """Base entension class for all entity """

    def before_insert(self, mapper, connection, instance):
        """ set the created_at  """
        instance.created_at = datetime.datetime.now()

    def before_update(self, mapper, connection, instance):
        """ set the updated_at  """
        instance.updated_at = datetime.datetime.now()

