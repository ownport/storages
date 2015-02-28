from packages import peewee

class DictField(peewee.Fiels):
    pass


webcontent_proxy = peewee.Proxy()
class Scheme(peewee.Model):

    content_id      = peewee.CharField(index=True)
    headers         = peewee.DictField()
    payload         = peewee.CharField()

    class Meta:
        database = webcontent_proxy
        db_table = 'webcontent'
        indexes = (
            # unique index for content_id
            (('content_id'), True),
        )

    def as_dict(self):

        return {
            'content_id': self.content_id, 
            'headers': self.headers, 
            'payload': self.payload
        }
