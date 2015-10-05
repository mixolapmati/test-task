#!/usr/bin/env python2.7
import unittest
from aliasdict import AliasDict


class TestAliasdict(unittest.TestCase):
	def setUp(self):
		d = {'foo': 1, 'bar': 'baz'}
                self.ad = AliasDict(d)
	def test_ad(self):
		self.assertEqual(self.ad['foo'], 1)
		self.assertIn('foo',self.ad)
	def test_set_alias(self):
		self.ad.set_alias('foo', ('foo_1', 'foo_2'))
		self.assertIn('foo_1', self.ad)
		self.assertEqual(self.ad['foo_2'], 1)
		self.ad['foo_1'] = 33
		self.assertEqual(self.ad['foo'], 33)
	def test_get_main_key(self):
                self.ad.set_alias('foo', ('foo_1', 'foo_2'))
		self.assertEqual(self.ad.get_main_key('foo_1'), 'foo')
	def test_update(self):
		d = {'foo': 2 }
		self.ad.update(d)
		self.assertEqual(self.ad['foo'], 2)
		self.ad.set_alias('foo', ('foo_1', 'foo_2'))
		d = {'foo_2': 'baz'}
		self.ad.update(d)
		self.assertEqual(self.ad['foo_1'], 'baz')
	def test_exceptions(self):
		d = {'foo': 1, 'bar': 'baz'}
		self.ad = AliasDict(d)
		d = str(d)
		self.assertRaises(TypeError, self.ad.update, d)
	def test_doc(self):
		print("DOC_TEST: ")
		import doctest, aliasdict
		doctest.testmod(aliasdict)

if __name__ == "__main__":
	unittest.main()
	doc_test()
