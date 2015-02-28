import unittest

from storages import webcontent

class SchemeTest(unittest.TestCase):

    def test_create_scheme(self):
        
        scheme = webcontent.Scheme()
        self.assertEqual(type(scheme), webcontent.Scheme)
        self.assertEqual(scheme.as_dict(), {'content_id': None, 'headers': None, 'payload': None} )


class WebContentTest(unittest.TestCase):

    def test_create_webcontent(self):

        content = webcontent.WebContent(':memory:')
        self.assertTrue(type(content), webcontent.WebContent)


    def test_store_webcontent(self):

        content = webcontent.WebContent(':memory:')

        content.put(u'1', {u'k1':u'v1'}, u'test')
        self.assertEqual(content.count(), 1)

        content.put(u'1', {u'k1':u'v1'}, u'test')
        self.assertEqual(content.count(), 1)

        self.assertEqual(content.get(), [(u'1', {u'k1': u'v1'}, u'test')])
        self.assertEqual(content.get(u'1'), (u'1', {u'k1': u'v1'}, u'test'))
        self.assertEqual(content.get(u'2'), ())

        content.delete(u'1')
        self.assertEqual(content.count(), 0)


    def test_put_webcontent(self):

        content = webcontent.WebContent(':memory:')
        self.assertRaises(RuntimeError, content.put, None, {})
        self.assertRaises(RuntimeError, content.put, (None, None, None))


    def test_delete_many(self):

        content = webcontent.WebContent(':memory:')

        content.put(u'1', {u'k1':u'v1'}, u'test')
        content.put(u'2', {u'k1':u'v1'}, u'test')
        content.put(u'3', {u'k1':u'v1'}, u'test')
        self.assertEqual(content.count(), 3)

        content.delete([u'1', u'2', u'3'])
        self.assertEqual(content.count(), 0)

