import sys
from Application import Application

def print_help_usage():
	print("python programm.py (questions file) (answers file) [additional infos file]")

def main():
	print(sys.argv)

	if len(sys.argv) < 3:
		print_help_usage()
	elif (sys.argv[1] == "--help"):
		print_help_usage()
	else:
		if len(sys.argv) == 4:
			application = Application(sys.argv[1], sys.argv[2], sys.argv[3])
		elif len(sys.argv) == 3:
			application = Application(sys.argv[1], sys.argv[2])
		application.run()

if __name__ == '__main__':
	main()