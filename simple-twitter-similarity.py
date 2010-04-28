#!/usr/bin/env python

import twitter

# Some extra stopwords to remove
STOPWORDS = ["http", "rt", "//bit.ly/", "RT"]

def preprocess(text, preprocessing):
    """
    Preprocess the text.
        preprocessing = None or 'string.split' means simply use string.split.
        preprocessing = pytextpreprocess means use the pytextpreprocess library.
    """
    import string
    if preprocessing is None or preprocessing == "string.split":
        return string.split(text)
    elif preprocessing == "pytextpreprocess":
        import textpreprocess
        return string.split(textpreprocess.textpreprocess(text))

def representation(statuses, preprocessing):
    """
    Get the representation for a particular user, as represented by a list of statuses.
    This representation is given as a dict: term=>value
    """
    from collections import defaultdict
    repr = defaultdict(int)
    for s in statuses:
        for t in preprocess(s.text, preprocessing):
            if t in STOPWORDS: continue
            repr[t] += 1
    return repr

def cosine(repr1, repr2):
    """
    Compute the Cosine similarity between repr1 and repr2 (http://en.wikipedia.org/wiki/Cosine_distance).
    Each repr is given as a dict: term=>value.

    Note: We could also use scipy.sparse operations, which are more
    concise, but this would require constructing a term=>id map. See
    common.idmap in my Python common package.
    """
    import math
    norm1 = 0.
    for t in repr1: norm1 += repr1[t] * repr1[t]
    norm1 = math.sqrt(norm1)
    norm2 = 0.
    for t in repr2: norm2 += repr2[t] * repr2[t]
    norm2 = math.sqrt(norm2)

#    from common.mydict import sort as dictsort
#    print dictsort(repr1)[:10]
#    print dictsort(repr2)[:10]

    import sets
    allterms = sets.ImmutableSet(repr1.keys() + repr2.keys())

    sim = 0.
    for t in allterms:
#        print "%.3f = %.3f * %.3f, %s" % (repr1[t] * repr2[t],repr1[t], repr2[t], t.encode("utf-8"))
        sim += (1. * repr1[t] * repr2[t] / (norm1 * norm2))

    return sim

_api = None
def similarity(user1, user2, preprocessing=None):
    """
    Compute the similarity of twitter user1 and user2, using the
    methodology described in the README.
    See the README for more notes and details about this method.
    """
    global _api
    if _api is None: _api = twitter.Api()

    statuses1 = _api.GetUserTimeline(user1, count=200)
    statuses2 = _api.GetUserTimeline(user2, count=200)

    print >> sys.stderr, "Loaded %d statuses for %s" % (len(statuses1), user1)
    print >> sys.stderr, "Loaded %d statuses for %s" % (len(statuses2), user2)

    repr1 = representation(statuses1, preprocessing)
    repr2 = representation(statuses2, preprocessing)

    return cosine(repr1, repr2)

if __name__ == "__main__":
    import sys
    from optparse import OptionParser
    usage = "usage: %prog [options] user1 user2"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--preprocessing", dest="preprocessing",
                      help="'string.split' or 'pytextpreprocess' [default: string.split]", default="string.split")

    (options, args) = parser.parse_args()

    if len(args) != 2:
        print >> sys.stderr, parser.print_help()
        assert 0
    print similarity(args[0], args[1], preprocessing=options.preprocessing)
