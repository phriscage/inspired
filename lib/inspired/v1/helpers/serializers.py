""" serializers files handles any data format transpose functions """
import json
import datetime
import decimal
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.query import Query

class JSONEncoder(json.JSONEncoder):
    """
    Wrapper class to try calling an object's tojson() method. This allows
    us to JSONify objects coming from the ORM. Also handles dates and datetimes.
    """

    def default(self, obj):
        if isinstance(obj, datetime.date) or isinstance(obj, datetime.time):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        try:
            return obj.tojson()
        except AttributeError:
            return json.JSONEncoder.default(self, obj)


def json_encoder(revisit_self=False, columns=[]):
    """ encode a sqlalchemy ORM object using a customized JSONEncoder class.
        You can implicitly specify a set of columns prefaced by the class name.
    """
    _visited_objs = []
    if columns:
        columns = [str(val) for val in columns]

    class JSONEncoder(json.JSONEncoder):
        """
        Wrapper class to try calling an object's tojson() method. This allows
        us to JSONify objects coming from the ORM as well as child objects. 
        """

        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if revisit_self:
                    if obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)
                class_name = obj.__class__.__name__
                #print [col for col in obj.__mapper__.c.keys()]
                #print [col for col in obj.__dict__.keys()]
                fields = {}
                for field in (field for field in dir(obj) \
                    if not field.startswith('_') and field != 'metadata'):
                    if field not in obj.__dict__:
                        continue
                    class_field = '%s.%s' % (class_name, field)
                    if columns and class_field not in columns:
                        continue
                    if field in obj.__dict__:
                        val = obj.__dict__[field]
                        ## add any specific execeptions below here
                        if isinstance(val, datetime.date) \
                            or isinstance(val, datetime.time):
                            val = val.isoformat()
                        if isinstance(val, decimal.Decimal):
                            val = float(val)
                        #print "--->>>>>", field, val
                        ## many-to-many relationships recursive
                        #print field, type(val)
                        if (isinstance(val, list) and len(val) > 0 \
                            and isinstance(val[0].__class__, DeclarativeMeta)):
                            val = [self.default(c_val) for c_val in val]
                    fields[field] = val
                #print fields
                return fields
            #try:
                #return obj.tojson()
            #except AttributeError:
                #return json.JSONEncoder.default(self, obj)
    return JSONEncoder
