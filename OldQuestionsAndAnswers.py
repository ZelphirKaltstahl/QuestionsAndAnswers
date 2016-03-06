#!/usr/bin/python

import sys
import random
from decimal import Decimal, localcontext, ROUND_DOWN

import StateWriter

available_commands = ['exit', '?', '!d', 'all', '+', '-']
exit_calls = ["exit", "quit", "exit()", "quit()"]
help_calls = ['?']

def readFile(path_to_file="questions.voc"):
	list_of_lines = []
	with open(path_to_file, "r") as file_object:
		for line in file_object:
			list_of_lines.append(line.strip())
	return list_of_lines

def print_help_usage():
	print("python programm.py questions_file answers_file")

def print_all(questions, answers):
	for i in range(len(questions)):
		print(questions[i] + ":" + answers[i])

def ask(questions, answers):
	deactivated_questions = []
	asked = 0
	answered = 0

	while(True):
		if len(deactivated_questions) < len(questions):
			
			random_number = random.randint(0, len(questions)-1)
			while random_number in deactivated_questions:
				random_number = random.randint(0, len(questions)-1)

			asked += 1
			action_taken = False

			while(not action_taken):
				some_input = input("Translate: \"" + questions[random_number] + "\"")
				print("Answer: " + answers[random_number])
				user_input = input("Command ('?' for help):")

				if user_input == "!d":
					deactivated_questions.append(random_number)
					answered += 1
					print("Question deactivated.")
					action_taken = True

				elif user_input == "all":
					print_all(questions, answers)
					action_taken = True
				
				elif user_input == 'exit':
					action_taken = True
					sys.exit(0)
					
				elif user_input == '?':
					print_help()

				elif user_input == '+':
					answered += 1
					action_taken = True

				elif user_input == '-':
					action_taken = True

				user_input = None

			print_result(asked, answered)
		else:
			print("All questions deactivated. Exiting now...")
			sys.exit(0)



def truncate_python(number, places):
	if not isinstance(places, int):
		raise ValueError("Decimal places must be an integer.")
	if places < 1:
		raise ValueError("Decimal places must be at least 1.")
	# If you want to truncate to 0 decimal places, just do int(number).

	with localcontext() as context:
		context.rounding = ROUND_DOWN
		exponent = Decimal(str(10 ** -places))
	return Decimal(str(number)).quantize(exponent).to_eng_string()

def truncate(num, digits):
	num_string = str(num)
	if '.' in num_string:
		digits += 1
	return float(num_string[:digits])

def truncate_decimals(num, digits):
	num_string = str(num)
	parts = num_string.split('.', -1)
	if '.' in num_string:
		parts[1] = parts[1][:digits]
		for part in parts: print(part)
		return float('.'.join(parts))
	else:
		return num

def print_result(asked, answered):
	percentage = (100.0 / float(asked)) * float(answered)
	percentage = truncate_python(percentage, 3)
	print("\nasked:", asked, "\nanswered:", percentage, "% correctly\n", sep='', end='\n')

def print_help():
	print(
		"\n"+
		"Available commands:\n"+
		"!d:deactivate\n"+
		"all:print all\n"+
		"exit:exit\n"+
		"?:help\n"+
		"+:mark correctly answered\n"
		"-:mark wrongly answered\n"
	)

def main():
	if len(sys.argv) < 2:
		print_help_usage()
	elif (sys.argv[1] == "--help"):
		print_help_usage()
	else:
		print("")
		questions = readFile(path_to_file=sys.argv[1])
		answers = readFile(path_to_file=sys.argv[2])

		ask(questions=questions, answers=answers)
		
		

if __name__ == "__main__":
	main()