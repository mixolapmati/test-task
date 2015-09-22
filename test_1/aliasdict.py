#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
    class AliasDict provide dict functionality, but with you can set aliases to different values.
    Value will be stored only once, so if it has huge data - no memory overhead.
    First assigned key => value become main key (which print in str()).
    There are several ways for setting aliases:
        - set_alias method
        - use tuple or list in key
    So difference with dict, that AliasDict don't assign tuple as a key.
    First element of tuple become main key, the rest - aliases to it.

    Expression like element in AliasDict return True if element exist neither in main_key nor in aliases.

    get_main_key method will return main key for given key.

    Deleting alias will remove only this alias.
    Deleting main key will remove all aliases and main key with it's value.

    Iterating over AliasDict will go through main keys only.

    Examples:
    >>>d = {'foo': 1, 'bar': 'baz'}
    >>>ad = AliasDict(d)
    >>>ad.set_alias('foo', ('foo_1', 'foo_2'))
    >>>print ad['foo_2']
    1
    >>>ad['foo_1'] = 33
    >>>print ad['foo']
    33
    >>>print ad
    {'foo': 33, 'bar': 'baz'}
    >>>'foo_1' in ad
    True
    >>>'foo_3' in ad
    False

"""

from UserDict import IterableUserDict, UserDict


class AliasDict(IterableUserDict):
    def __init__(self, _dict=None):
        IterableUserDict.__init__(self)
        self.__alias = {}
        self.update(_dict)

    @staticmethod
    def __normalize_value(value):
        if type(value) in (str, int, long, float):
            return value
        elif type(value) in (tuple, list, set, frozenset):
            return list(value)
        else:
            raise TypeError('unsupported type', type(value))

    def __getitem__(self, key):
        key = self.__normalize_value(key)
        if key in self.__alias:
            return self.data[self.__alias[key]]
        else:
            raise KeyError(key)

    def __delitem__(self, key):
        if key in self.keys():
            self.__remove_aliases(key)
            del self.data[key]
        if key in self.__alias:
            del self.__alias[key]

    def __setitem__(self, key, value):
        key = self.__normalize_value(key)
        if not type(key) is list:
            self.__set_one_item(key, value)
        else:
            intersect = [k for k in key if k in self.__alias]
            if len(intersect) == 0:
                main_key = key.pop(0)
            elif len(intersect) == 1:
                main_key = intersect[0]
            else:
                if len(set([self.__alias[i] for i in intersect])) == 1:
                    main_key = intersect.pop(0)
                else:
                    raise ValueError('mix aliases with values', str(intersect))
            self.__set_one_item(main_key, value)
            if key:
                self.__set_alias(main_key, key)

    def __contains__(self, key):
        return key in self.__alias

    def __set_alias(self, key, alias):
        for a in alias:
            self.__alias[a] = self.__alias[key]

    def __set_one_item(self, key, value):
        if key in self.__alias:
            self.data[self.__alias[key]] = value
        else:
            self.__alias[key] = key
            self.data[self.__alias[key]] = value

    def __remove_aliases(self, key):
        for k in self.__alias.keys():
            if self.__alias[k] == key and key != k:
                del self.__alias[k]

    def set_alias(self, key, alias):
        key = self.__normalize_value(key)
        alias = self.__normalize_value(alias)
        if key not in self.__alias:
            raise KeyError(key)
        if type(alias) is list:
            alias.append(key)
        else:
            alias = [alias, key]
        self.__setitem__(alias, self[key])

    def get_main_key(self, key):
        return self.__alias[key]

    def update(self, _dict=None, **kwargs):
        if _dict:
            if not (isinstance(_dict, dict) or isinstance(_dict, UserDict)):
                raise TypeError('dict expected')
            for k, v in _dict.iteritems():
                self.__setitem__(k, v)
