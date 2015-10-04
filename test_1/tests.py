#python -m doctest aliasdict.py
#python -m unittest aliasdict
import unittest
from aliasdict import AliasDict


class TestAliasdict(unittest.TestCase):
	def test_ad(self):
		d = {'foo': 1, 'bar': 'baz'}
		ad = AliasDict(d)
		self.assertEqual(ad['foo'], 1)
		self.assertEqual('foo' in ad, True)
	def test_set_alias(self):
		d = {'foo': 1, 'bar': 'baz'}
		ad = AliasDict(d)
		ad.set_alias('foo', ('foo_1', 'foo_2'))
		self.assertEqual('foo_1' in ad, True)
		self.assertEqual(ad['foo_2'], 1)
		ad['foo_1'] = 33
		self.assertEqual(ad['foo'], 33)
	def test_get_main_key(self):
		d = {'foo': 1, 'bar': 'baz'}
                ad = AliasDict(d)
                res = ad.set_alias('foo', ('foo_1', 'foo_2'))
		self.assertEqual(ad.get_main_key('foo_1'), 'foo')
#		self.assertRaises()
	def test_update(self):
		d = {'foo': 1, 'bar': 'baz'}
                ad = AliasDict(d)
		d = {'foo': 2, 'bar': 'baz'}
		ad.update(d)
		self.assertEqual(ad['foo'], 2)
		ad.set_alias('foo', ('foo_1', 'foo_2'))
		d = {'foo_2': 'baz'}
		ad.update(d)
		self.assertEqual(ad['foo_1'], 'baz')
		
	def test_doc(self):
		print("DOC_TEST: ")
		import doctest, aliasdict
		doctest.testmod(aliasdict)

#doc_test()

if __name__ == "__main__":
	unittest.main()
	#doc_test()
	#import doctest
	#doctest.testmod()
