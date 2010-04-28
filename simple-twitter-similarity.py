#!/usr/bin/env python

import twitter

def preprocess(text, preprocessing):
    """
    Preprocess the text.
        preprocessing = None or 'string.split' means simply use string.split.
        preprocessing = pytextpreprocess means use the pytextpreprocess library.
    """
    if preprocessing is None or preprocessing == "string.split":
        import string
        return string.split(text)
    elif preprocessing == "pytextpreprocess":
        import textpreprocess
        return textpreprocess.textpreprocess(text)

def representation(statuses, preprocessing):
    """
    Get the representation for a particular user, as represented by a list of statuses.
    """
    for s in statuses:
        print preprocess(s.text, preprocessing)

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

    print representation(statuses1, preprocessing)
    print representation(statuses2, preprocessing)

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
