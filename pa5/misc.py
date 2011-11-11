#PA 4
import math
import re

"Miscellaneous functions to practice Python"

class Failure(Exception):
    """Failure exception"""
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

# Problem 1

# data type functions

def closest_to(l,v):
    """Return the element of the list l closest in value to v.  In the case of
       a tie, the first such element is returned.  If l is empty, None is returned."""
    closest = None
    for k in l:
        if closest == None:
            closest = k
        elif math.fabs(closest - v) > math.fabs(k - v):
            closest =  k
    return closest

def make_dict(keys,values):
    """Return a dictionary pairing corresponding keys to values."""
    d = {}
    for k, v in zip(keys,values):
        d[k] = v
    return d
   
# file IO functions
def word_count(fn):
    """Open the file fn and return a dictionary mapping words to the number
       of times they occur in the file.  A word is defined as a sequence of
       alphanumeric characters and _.  All spaces and punctuation are ignored.
       Words are returned in lower case"""
    f = open(fn)
    lf = re.split(r'\W+',f.read().lower())
    d = {}
    for w in lf:
        if w in d:
            d[w] += 1
        else:
            d[w] = 1
    del d['']
    return d








