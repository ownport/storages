import os

from packages import peewee
# from utils import normalize_path


metadata_db_proxy = peewee.Proxy()
class Scheme(peewee.Model):

    item_id         = peewee.CharField(index=True)
    key             = peewee.CharField(index=True)
    value           = peewee.CharField(index=True)

    class Meta:
        database = metadata_db_proxy
        db_table = 'metadata'
        indexes = (
            # unique index for item_id, key, value
            (('item_id', 'key', 'value'), True),
        )

    def as_dict(self):

        return {'item_id': self.item_id, 'key': self.key, 'value': self.value}


class Metadata(object):

    def __init__(self, path):
        ''' path - path to metadata file (sqlite)
        '''                
        self._db = peewee.SqliteDatabase(path)
        metadata_db_proxy.initialize(self._db) 
        if not Scheme.table_exists():
            Scheme.create_table()


    def put(self, item_id, metadata=list()):
        ''' store item_id metadata into database
        '''
        if not item_id:
            raise RuntimeError('ItemId is not defined, %s' % item_id)

        if not isinstance(metadata, list):
            raise RuntimeError('Metadata is not defined or defined not as a list of (key,value), %s' % metadata)

        with self._db.transaction():
            for k, v in metadata:
                try:
                    Scheme.create(**{'item_id': item_id, 'key': k, 'value': v}) 
                except peewee.IntegrityError:
                    # TODO update metadata
                    pass

        return self.get(item_id)


    def get(self, item_id=None):
        ''' get metadata
        '''
        if not item_id:
            _metadata = list()
            for item in Scheme.select(Scheme.item_id).group_by(Scheme.item_id):
                _metadata.append((item.item_id, [(meta.key, meta.value) \
                    for meta in Scheme.select().where(Scheme.item_id == item.item_id)]))
        else:
            _metadata = (item_id, [(meta.key, meta.value) \
                for meta in Scheme.select().where(Scheme.item_id == item_id)])
        return _metadata


    def delete(self, item_id):
        ''' delete item 
        '''
        with self._db.transaction():
            if isinstance(item_id, (list, tuple)):
                for meta in Scheme.select().where(Scheme.item_id << item_id):
                    meta.delete_instance()                
            else:
                for meta in Scheme.select().where(Scheme.item_id == item_id):
                    meta.delete_instance()


    def search(self, k, v):
        ''' select item_ids where metadata key = k and metadata value = v
        '''
        return [f.item_id for f in Scheme.select(Scheme.item_id)
                                    .where(Scheme.key == k, Scheme.value == v)
        ]


    def count(self):
        ''' return count of records in database
        '''
        return Scheme.select().group_by(Scheme.item_id).count()
