# coding=utf-8
"""
seen.py - Sopel Seen Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright © 2012, Elad Alfassa <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

http://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import re
import time
import datetime
from sopel.tools import Identifier
from sopel.tools.time import get_timezone, format_time
from sopel.module import commands, rule, priority, thread, require_chanmsg, require_admin


@commands('learn')
def learn(bot, trigger):
    """Learn something !learn word as deinfition"""

    if not trigger.group(2) :
        bot.say("learn <what> as <definition> - Educate me.")
        return

    regex = re.compile(r'(.+) as (.+)')
    matches = regex.match(trigger.group(2).strip())
    if not matches or len(matches.groups()) != 2:
        bot.say("learn <what> as <definition> - Educate me.")
        return

    keyword = matches.group(1)
    definition = matches.group(2)

    result = bot.db.execute('SELECT * FROM learn WHERE keyword="%s"' % keyword)
    found = result.fetchone()
    if not found:
        bot.db.execute('INSERT INTO learn (keyword, definition) '
                       'VALUES ("%s", "%s")' % (keyword, definition))
        bot.say('Added %s as %s' % (keyword, definition))
    else:
        old_defs = found[1].split('\t')
        if definition in old_defs:
            bot.say('Already know that, thanks')
            return

        new_def = '\t'.join( (found[1], definition) )
        bot.db.execute('UPDATE learn SET definition="%s" '
                       'WHERE keyword="%s"' % (new_def, keyword))
        bot.say('Learned %s as %s' % (keyword, definition))


@thread(False)
@rule('!(.*)')
@priority('low')
def say_learn(bot, trigger):
    keyword = trigger.group(1)
    result = bot.db.execute('SELECT * FROM learn WHERE keyword="%s"' % keyword)
    found = result.fetchone()
    if found:
        definitions = found[1].split('\t')
        defs = ""
        for i,d in enumerate(definitions):
            defs += '#%d %s ' % (i+1, d)

        bot.say('%s is %s' % (keyword, defs))


@require_chanmsg
@require_admin
@commands('forget')
def forget(bot, trigger):
    print('forgetting')
    if not trigger.group(2):
        bot.say('What do you want me to forget?')
        return

    regex = re.compile(r'(.+) (\d)')
    matches = regex.match(trigger.group(2).strip())
    if not matches or len(matches.groups()) != 2:
        bot.say('Use !forget <keyword> <number>')
        return

    keyword = matches.group(1)
    index = int(matches.group(2))
    result = bot.db.execute('SELECT * FROM learn WHERE keyword="%s"' % keyword)
    found = result.fetchone()
    if not found:
        bot.say('I don`t know anything about %s' % keyword)
        return

    defs = found[1].split('\t')
    try:
        forgotten = defs.pop(index-1)
    except IndexError:
        bot.say('Not a valid index')
        return

    new_def = '\t'.join(defs)
    bot.db.execute('UPDATE learn SET definition="%s" '
                   'WHERE keyword="%s"' % (new_def, keyword))
    bot.say('Forgot %s as %s' % (keyword, forgotten))


