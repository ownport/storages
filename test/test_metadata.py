import os
import unittest

from storages import metadata

class SchemeTest(unittest.TestCase):

    def test_create_scheme(self):
        
        scheme = metadata.Scheme()
        self.assertEqual(type(scheme), metadata.Scheme)


    def test_scheme_as_dict(self):

        scheme = metadata.Scheme()
        self.assertEqual(scheme.as_dict(), {'item_id': None, 'key': None, 'value': None})        


class MetadataTest(unittest.TestCase):

    def test_create_metadata(self):

        database_path = 'tmp/test_create_metadata.sqlite'
        meta = metadata.Metadata(database_path)
        self.assertTrue(os.path.exists(database_path))
        os.remove(database_path)
        self.assertTrue(not os.path.exists(database_path))

    def test_store_metadata(self):

        database_path = 'tmp/test_store_metadata.sqlite'
        meta = metadata.Metadata(database_path)
        self.assertTrue(os.path.exists(database_path))

        self.assertRaises(RuntimeError, meta.put, None, None)
        self.assertRaises(RuntimeError, meta.put, 'a1', None)
        meta.put('b1', [('k1','v1'),])
        meta.put('b1', [('k1','v1'),('k2','v2')])
        meta.put('b1', [('k2','v3'),('k3','v2')])
        self.assertEqual(meta.get('b1'), ('b1', [('k1','v1'),('k2','v2'),('k2','v3'),('k3','v2')]))

        meta.delete('b1')
        self.assertEqual(meta.get('b1'), ('b1', []))

        os.remove(database_path)
        self.assertTrue(not os.path.exists(database_path))


    def test_get_metadata(self):

        database_path = 'tmp/test_get_metadata.sqlite'
        meta = metadata.Metadata(database_path)
        self.assertTrue(os.path.exists(database_path))

        meta.put('b1', [('k1','v1')])
        meta.put('b2', [('k2','v2')])
        meta.put('b3', [('k3','v3')])
        self.assertEqual(meta.get(), [(u'b1', [(u'k1', u'v1')]), (u'b2', [(u'k2', u'v2')]), (u'b3', [(u'k3', u'v3')])])

        meta.delete(['b1', 'b2', 'b3'])
        self.assertEqual(meta.count(),0)
        
        os.remove(database_path)
        self.assertTrue(not os.path.exists(database_path))


    def test_search_metadata(self):

        database_path = 'tmp/test_search_metadata.sqlite'
        meta = metadata.Metadata(database_path)
        self.assertTrue(os.path.exists(database_path))

        meta.put('b1', [('k1','v1')])
        meta.put('b2', [('k1','v2')])
        meta.put('b3', [('k1','v3')])

        self.assertEqual(meta.search('k1', 'v2'), ['b2'])
        
        os.remove(database_path)
        self.assertTrue(not os.path.exists(database_path))

