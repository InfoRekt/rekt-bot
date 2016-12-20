# coding=utf-8
"""
"""
from __future__ import unicode_literals, absolute_import, print_function, division

from sopel.module import commands, example, priority
import random
import sys


@commands('roulette')
@priority('low')
def roulette(bot, trigger):
    number = random.randint(0, 6)
    nick = trigger.nick
    channel = trigger.sender
    if number == 4:
        bot.say('BANG')
        bot.write(['KICK', channel, nick], "You lose")
    else:
        bot.say('CLICK')


if __name__ == "__main__":
    from sopel.test_tools import run_example_tests
    run_example_tests(__file__)
