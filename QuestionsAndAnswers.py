import sys
from Application import Application

def print_help_usage():
	print("python programm.py (Q&A File Path)")

def main():
	application = Application(sys.argv[1])
	application.run()

if __name__ == '__main__':
	main()