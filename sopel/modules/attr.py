# coding=utf-8
"""
"""
from __future__ import unicode_literals, absolute_import, print_function, division

from sopel.module import commands, example, priority
import random
import sys

class Dicebot():
	def __init__(self):
		self.countries = ['Russia',
					   'China',
					   'DPRK',
					   'Iran',
					   'USA',
					   'Israel']

		self.actors = ['NSA', 'GCHQ', 'Unit 21', 'Unit 61398', 'Cyber Crime',
						'Hacktivist']

		self.vulns = ['MS08-67', '0-Day', 'XSS', 'SQL-Injection', 'Bad Bios',
					  'JAVA']

		self.vectors = ['Malware', 'DDoS', 'Phishing', 'SSL MiTM',
						'Brute Force', 'Back Door']

		self.cmds = {'roll': self.roll}


	def roll(self):
		random.seed()

		result = []
		result.append(self.countries[random.randint(0, len(self.countries) - 1)])
		result.append(self.actors[random.randint(0, len(self.actors) - 1)])
		result.append(self.vulns[random.randint(0, len(self.vulns) - 1)])
		result.append(self.vectors[random.randint(0, len(self.vectors) - 1)])

		return result

	def execute_cmd_with_result(self, tweet):
		m = re.search('!(\w+)', tweet)
		if m:
			issued_cmd = m.groups()[0]
			try:
				return self.cmds[issued_cmd]()
			except KeyError:
				return None

		return None


@commands('attr')
@priority('low')
def attr(bot, trigger):
	dicebot = Dicebot()
	msg = dicebot.roll()

	bot.say('The dice have been cast. Country: %s - Actor: %s - Vuln: %s - Vector: %s' % (msg[0], msg[1], msg[2], msg[3]))


if __name__ == "__main__":
	from sopel.test_tools import run_example_tests
	run_example_tests(__file__)
