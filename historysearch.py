"""
This is the script to search things in the dialogue history of QAMatcher

(Evania Lina Fasya - 2017 - https://github.com/evania)

"""

import os
import re

def history(utterance):
	history = []
	new_utterance = ''
	
	with open("qamatcher/resources/qamatcher/history.txt", "a") as f:
		if utterance is not "":
			f.write(utterance + '\n')
			
	ff = open("qamatcher/resources/qamatcher/history.txt", "r+")
	for line in ff.readlines():
		if line is not "":
			history.append(line)
	while len(history) > 2:
		history = history[-2:]
	
	utterance_help = re.search('[Hh]appen(.{1,})', history[0])
	
	
	change_utt_1 = re.match('^([Ww]hat happen[a-z]{0,3}\?{0,3})$', utterance)
	change_utt_2 = re.match('^([Ww]hat happen[a-z]{0,3} [a-z]{1,5}\?{0,3})$', utterance)
	change_utt_3 = re.match('^([Ww]hat.{0,2} [a-z]{1,5}\?{0,3})$', utterance)
	change_utt_4 = re.match('^([Ww]hat\?{0,3})$', utterance)
	change_utt_5 = re.match('^([Aa]nd {0,1}(then|next){0,1}\?{0,3})$', utterance)
	change_utt_6 = re.match('^(([Nn]ext|[Tt]hen)\?{0,3})$', utterance)
	
	if (change_utt_1 is not None) or (change_utt_2 is not None) or (change_utt_3 is not None) or (change_utt_4 is not None) or (change_utt_5 is not None) or (change_utt_6 is not None):
		#print "change_utterance_1"
		if utterance_help is not None:
			utterance_help_word = utterance_help.group(0)
			new_utterance = 'What ' + utterance_help_word
		else:
			new_utterance = utterance
	else:
		new_utterance = utterance
	
	'''
	long_utterance = re.match('[Ww]hat happen.{15,}', utterance) # the user's question is long
	if long_utterance is None:
		utterance_help = re.search('[Hh]appen(.{1,})', history[0])
		if utterance_help is not None:
			utterance_help_word = utterance_help.group(0)
			
			new_utterance = 'What ' + utterance_help_word
		else:
			new_utterance = utterance
	else:
		new_utterance = utterance
	'''
	return new_utterance
	

utterance = raw_input("Enter question: ") 
new_utterance = history(utterance)


with open("qamatcher/resources/qamatcher/last_question_adjusted.txt", "w") as j:
	if new_utterance is not "":
		j.write(new_utterance+"\n")