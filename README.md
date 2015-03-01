# Storages

[![Build Status](https://travis-ci.org/ownport/storages.svg)](https://travis-ci.org/ownport/storages)

The collection of simple storages on python

- Metadata
- Web content
- Files

[peewee](https://github.com/coleifer/peewee) library is used which allow you to store data in 
sqlite, mysql, postgresql databases. The access to items provides by get(), put(), delete(), search() methods

## Metadata

All data in metadata storage are saved as collection of key/value with specific item_id: 

```python
item = (u'item_id', (('k1','v1'), ('k2','v2'), ('k3','v3'),)
```

One unique id with multiple pairs of key/value

Example of usage:

```python
>>> from storages.metadata import Metadata
>>> meta = Metadata(':memory:')
>>>
>>> meta.put('b1', [('k1','v1'),])
('b1', [(u'k1', u'v1')])
>>> meta.put('b1', [('k1','v1'),('k2','v2')])
('b1', [(u'k1', u'v1'), (u'k2', u'v2')])
>>>
>>> meta.get()
[(u'b1', [(u'k1', u'v1'), (u'k2', u'v2')])]
>>> meta.get('b1')
('b1', [(u'k1', u'v1'), (u'k2', u'v2')])
>>> meta.get('b2')
('b2', [])
>>>
>>> meta.count()
1
>>> meta.search('k2', 'v2')
[u'b1']
>>>
>>> meta.delete('b1')
>>> meta.count()
0
>>> 
```


## Web Content

Web content will be stored with the next fields: content_id, headers, payload. Where content_id is unique key for content. The headers keys is dictionary, serialized in database in JSON format. The payoad is web page content.

```python
>>> from storages.webcontent import WebContent
>>> content = WebContent(':memory:')
>>>
>>> content.put(u'1', {u'k1':u'v1'}, u'test')
(u'1', {u'k1': u'v1'}, u'test')
>>> content.count()
1
>>> content.get()
[(u'1', {u'k1': u'v1'}, u'test')]
>>> content.get(u'1')
(u'1', {u'k1': u'v1'}, u'test')
>>> content.delete(u'1')
>>> 
>>> content.count()
0
>>>
```

## Files

to be added later

## Change log

Based on GitHub [Milestones](https://github.com/ownport/storages/milestones)

