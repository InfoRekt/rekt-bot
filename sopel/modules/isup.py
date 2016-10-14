# coding=utf-8
"""Simple website status check with isup.me"""
# Author: Elsie Powell http://embolalia.com
from __future__ import unicode_literals, absolute_import, print_function, division

import requests
from sopel.module import commands


@commands('isup')
def isup(bot, trigger):
    """isup.me website status checker"""
    site = trigger.group(2)
    if not site:
        return bot.reply("What site do you want to check?")

    if site[:7] != 'http://' and site[:8] != 'https://':
        if '://' in site:
            protocol = site.split('://')[0] + '://'
            return bot.reply("Try it again without the %s" % protocol)
        else:
            site = 'http://' + site

    if not '.' in site:
        site += ".com"

    try:
        r = requests.get(site)
    except requests.exceptions.ConnectionError:
        bot.say(site + ' looks down to me')

    if r.status_code == 200:
        bot.say(site + ' looks fine to me.')
    elif r.status_code == 404:
        bot.say(site + ' looks ok, but returning 404')
    else:
        bot.say(site + ' looks down to me')

