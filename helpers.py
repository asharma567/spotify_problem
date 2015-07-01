'''
utility functions for playlist maker
'''

import string 


PUNC_SET = set(string.punctuation)

def memoize(fn):
    stored_results = {}
    def memoized(*args):
        try:
            # try to get the cached result
            return stored_results[args]
        except KeyError:
            # nothing was cached for those args. let's fix that.
            result = stored_results[args] = fn(*args)
            return result
    return memoized


def make_verbose(fn):
    '''
    used for debugging purposes 
    to take note of args being 
    passed the function each call
    '''

    def verbose(*args):
        print '%s(%s)' % (fn.__name__, ', '.join(repr(arg) for arg in args))
        return fn(*args)
    return verbose

def pop_from_str(in_str, phrase_str):
    return in_str.replace(phrase_str, '').replace('  ', ' ')

def normalize_string(target_str):
    removed_punc_str = ''.join([char for char in target_str if char not in PUNC_SET])
    return removed_punc_str.lower()
