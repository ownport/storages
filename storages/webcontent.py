import json
from packages import peewee


class DictField(peewee.Field):
    db_field = 'dict'

    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        return json.loads(value)

peewee.Database.register_fields({'dict': 'blob'})


webcontent_proxy = peewee.Proxy()
class Scheme(peewee.Model):

    content_id      = peewee.CharField(index=True, unique=True)
    headers         = DictField()
    payload         = peewee.CharField()

    class Meta:
        database = webcontent_proxy
        db_table = 'webcontent'


    def as_dict(self):

        return {
            'content_id': self.content_id, 
            'headers': self.headers, 
            'payload': self.payload
        }


class WebContent(object):

    def __init__(self, path):
        ''' path - path to metadata file (sqlite)
        '''                
        self._db = peewee.SqliteDatabase(path)
        webcontent_proxy.initialize(self._db) 
        if not Scheme.table_exists():
            Scheme.create_table()

    def put(self, content_id, headers={}, payload=None):
        ''' store web content into database
        '''
        if not content_id:
            raise RuntimeError('ContentId is not defined, %s' % content_id)

        if not headers and not payload:
            raise RuntimeError('Headers and payload are empty. Headers: %s, payload: %s' % (headers, payload))

        with self._db.transaction():
            try:
                Scheme.create(**{'content_id': content_id, 'headers': headers, 'payload': payload})
            except peewee.IntegrityError:
                # TODO update metadata
                pass
        return self.get(content_id)


    def get(self, content_id=None):
        ''' get content_id
        '''
        if not content_id:
            return [(r.content_id, r.headers, r.payload) \
                for r in Scheme.select()]
        else:
            r = Scheme.select().where(Scheme.content_id == content_id)
            if r.first():
                return (r.first().content_id, r.first().headers, r.first().payload)
            else:
                return ()


    def count(self):
        ''' return count of records in database
        '''
        return Scheme.select().count()
