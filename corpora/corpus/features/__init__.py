from __future__ import print_function, absolute_import
from importlib import import_module

def default_feature_finder(x):
    # rely only on the set of characters.
    from collections import Counter
    return Counter


def import_finder(lang):
    if lang.isalpha():
        try:
            m = import_module(lang, 'features')
            return m.get_features
        except ImportError as e:
            return default_feature_finder
        except AttributeError as e:
            return default_feature_finder