#!/usr/bin/env python2.6

import ff
import sg

import itertools
from pprint import pformat

def main():
    tests = [
        ('map1', test_map1),
        ('reduce1', test_reduce1),
        ('map2', test_map2),
        ('reduce2', test_reduce2),
        ('genSentence', test_genSentence)
    ]

    total, passed = 0, 0
    for label, func in tests:
        try:
            tpassed, ttotal = func()
        except Exception as e:
            if e.args == ('not implemented',):
                print "  SKIP: %s (not implemented)" % label
            else:
                raise
        else:
            if tpassed != ttotal:
                print "FAILED: %s" % label,
            else:
                print "PASSED: %s" % label,
            print "(%i/%i passed)" % (tpassed, ttotal)
            passed += tpassed
            total += ttotal

    print
    print "Passed %i / %i tests." % (passed, total)

def test_function(func, inputs, outputs):
    passed = 0
    for input, output in zip(inputs, outputs):
        try:
            actual = func(*input)
        except Exception as e:
            if e.args == ('not implemented',):
                raise
            else:
                print "Called %s(%s)." % (func.__name__, ', '.join(map(repr, input)))
                print "Raised exception: %r" % e
        else:
            if actual != output:
                print "Called %s(%s)." % (func.__name__, ', '.join(map(repr, input)))
                print "Expected:"
                print pformat(output)
                print "Got:"
                print pformat(actual)
            else:
                passed += 1

    return (passed, len(inputs))

def test_map1():
    fi = ['foo', '2']
    inputs = [
        [fi, ["hello There, World, how-are you doing today? it's a \"fine\" day indeed."]],
        [fi, ["It Sure Is a great day, my dear 8ball, is it not? Weather IS GREAT."]],
        [fi, ["one two three four five six seven 8ight 9ine 10en 11even twelve thirteen fourteen fifteen sixteen"]],
        [fi, ["YOU don't know about me without you have read a book by the name of The"]]
    ]

    fo = ['1', 'foo', '2']
    outputs = [
        [
            (['hello', 'there', 'world', 'how', 'are'], fo),
            (['there', 'world', 'how', 'are', 'you'], fo),
            (['world', 'how', 'are', 'you', 'doing'], fo),
            (['how', 'are', 'you', 'doing', 'today'], fo),
            (['are', 'you', 'doing', 'today', 'its'], fo),
            (['you', 'doing', 'today', 'its', 'a'], fo),
            (['doing', 'today', 'its', 'a', 'fine'], fo),
            (['today', 'its', 'a', 'fine', 'day'], fo),
            (['its', 'a', 'fine', 'day', 'indeed'], fo)
        ], [
            (['it', 'sure', 'is', 'a', 'great'], fo),
            (['sure', 'is', 'a', 'great', 'day'], fo),
            (['is', 'a', 'great', 'day', 'my'], fo),
            (['a', 'great', 'day', 'my', 'dear'], fo),
            (['is', 'it', 'not', 'weather', 'is'], fo),
            (['it', 'not', 'weather', 'is', 'great'], fo)
        ], [
            (['one', 'two', 'three', 'four', 'five'], fo),
            (['two', 'three', 'four', 'five', 'six'], fo),
            (['three', 'four', 'five', 'six', 'seven'], fo),
            (['twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen'], fo)
        ], [
            (['you', 'dont', 'know', 'about', 'me'], fo),
            (['dont', 'know', 'about', 'me', 'without'], fo),
            (['know', 'about', 'me', 'without', 'you'], fo),
            (['about', 'me', 'without', 'you', 'have'], fo),
            (['me', 'without', 'you', 'have', 'read'], fo),
            (['without', 'you', 'have', 'read', 'a'], fo),
            (['you', 'have', 'read', 'a', 'book'], fo),
            (['have', 'read', 'a', 'book', 'by'], fo),
            (['read', 'a', 'book', 'by', 'the'], fo),
            (['a', 'book', 'by', 'the', 'name'], fo),
            (['book', 'by', 'the', 'name', 'of'], fo),
            (['by', 'the', 'name', 'of', 'the'], fo)
        ]
    ]

    return test_function(ff.map1, inputs, outputs)

def test_reduce1():
    inKey = ['a', 'b', 'c', 'd', 'e']

    sequence = [
        ['1', 'aa', '2472'],
        ['1', 'aa', '240'],
        ['1', 'aaa', '300'],
        ['1', 'aaa', '42'],
        ['1', 'b', '1'],
        ['1', 'bbb', '10928']
    ]

    inputs = [(inKey, l) for l in itertools.permutations(sequence)]
    outputs = [['6', 'aa', '240']] * len(inputs)

    return test_function(ff.reduce1, inputs, outputs)
    
def test_map2():
    inKey = ['a', 'b', 'c', 'd', 'e']
    inputs = [
        (inKey, ['6', 'foo', '42']),
        (inKey, ['1', 'bar', '3'])
    ]

    prefix = ['b', 'c', 'd', 'e']
    outputs = [
        [(['a'], prefix + ['6', 'foo', '42'])],
        [(['a'], prefix + ['1', 'bar', '3'])]
    ]

    return test_function(ff.map2, inputs, outputs)

def test_reduce2():
    prefix = ['b', 'c', 'd', 'e']
    sequence = [
        prefix + ['18', 'aa', '4'],
        prefix + ['18', 'aa', '42'],
        prefix + ['18', 'aaa', '4'],
        prefix + ['18', 'b', '3'],
        prefix + ['17', 'a', '2'],
        prefix + ['1', 'bb', '1']
    ]
    inputs = [(['a'], i) for i in itertools.permutations(sequence)]
    outputs = [prefix + ['18', 'aa', '4']] * len(inputs)

    return test_function(ff.reduce2, inputs, outputs)

def test_genSentence():
    def test_mcf():
        inputs = [('my',), ('old',), ('sugar',), ('all',)]
        outputs = [
            ['boy', 'says', 'the', 'old', '2', 'huckleberry', '3781'],
            ['rags', 'and', 'my', 'sugar', '1', 'huckleberry', '74'],
            ['there', 'was', 'and', 'all', '1', 'huckleberry', '1190'],
            ['the', 'time', 'and', 'never', '2', 'huckleberry', '428']
        ]

        return test_function(sg.mostCommonFragment, inputs, outputs)

    def test_sg1():
        inputs = [(w, 1) for w in ['my', 'old', 'sugar', 'all']]
        outputs = ['my boy says the old', 'old rags and my sugar', 'sugar there was and all', 'all the time and never']

        return test_function(sg.genSentence, inputs, outputs)

    def test_sg():
        inputs = [
            ('my', 2),
            ('my', 4),
            ('no', 4)
        ]
        outputs = [
            'my boy says the old rags and my sugar',
            'my boy says the old rags and my sugar there was and all the time and never',
            'no use to try to put in the time i didnt want to put in the time'
        ]

        return test_function(sg.genSentence, inputs, outputs)

    # This is so that we won't run these expensive tests if genSentence hasn't
    # been implemented yet (in which case it'll raise a 'not implemented' Exception)
    try:
        sg.genSentence('w', 1)
    except Exception as e:
        if e.args == ('not implemented',):
            raise

    sg.runBothPhases(1000, ["huckleberry"])
    passed, total = map(sum, zip(test_mcf(), test_sg1(), test_sg()))

    return (passed, total)

if __name__ == '__main__':
    main()
