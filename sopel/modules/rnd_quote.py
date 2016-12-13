# coding=utf-8
"""
rand.py - Rand Module
Copyright 2013, Ari Koivula, <ari@koivu.la>
Licensed under the Eiffel Forum License 2.

http://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function, division

from sopel.module import commands, example
import random
import sys
import os
import codecs

def get_quote(who):
    quote_dir = "/home/unlogic/quotes/"
    with codecs.open(os.path.join (quote_dir, who), encoding='utf-8') as fh:
        quotes = []
        for line in fh:
            quotes.append(line)

    random.seed()
    select = random.randint(0, len(quotes) - 1)
    print (quotes[select])
    return quotes[select]


@commands('sgarbi')
def sgarbi(bot, trigger):
    bot.say(u"Sgarbi says: %s" % get_quote('sgarbi.txt'))


@commands('hicks')
def hicks(bot, trigger):
    bot.say(u"Bill Hicks says: %s" % get_quote('hicks.txt'))


@commands('mcafee')
def mcafee(bot, trigger):
    bot.say(u"John McAfee says: %s" % get_quote('mcafee.txt'))

if __name__ == "__main__":
    from sopel.test_tools import run_example_tests
    run_example_tests(__file__)
