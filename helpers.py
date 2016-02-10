'''
utility functions for playlist maker
'''

import string 
PUNC_SET = set(string.punctuation)

def memoize(fn):
    '''
    I: function with args 
    O: creates a hash table with the args

    a general decorator used for caching can be applied to any function
    '''
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
    I: function with args
    O: print of function call with args
    
    used for debugging purposes to take note of args being 
    passed the function each call
    '''

    def verbose(*args):
        print '%s(%s)' % (fn.__name__, ', '.join(repr(arg) for arg in args))
        return fn(*args)
    return verbose

def deadline(timeout, *args):
    '''
    I: an integer value, which represents the deadline for a function to execute in terms of seconds 
    O: no return value, just raises an error TimedOutExc if the it's activated

    place @deadline on top of the function
    '''
    def decorate(f):
        def handler(signum, frame):
            raise TimedOutExc()

        def new_f(*args):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout)
            return f(*args)
            signa.alarm(0)

        new_f.__name__ = f.__name__
        return new_f
    return decorate

def pop_from_str(in_str, phrase_str):
    return in_str.replace(phrase_str, '').replace('  ', ' ')

def normalize_string(target_str):
    removed_punc_str = ''.join([char for char in target_str if char not in PUNC_SET])
    return removed_punc_str.lower()
