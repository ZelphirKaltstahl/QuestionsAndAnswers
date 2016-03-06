from Helper import truncate_number

class FileReader:
	"""The FileReader is a class whose instances can read files."""
	def __init__(self):
		super(FileReader, self).__init__()
	
	def read_file(self, path_to_file):
		list_of_lines = []
		with open(path_to_file, "r") as file_object:
			for line in file_object:
				list_of_lines.append(line.strip())
		return list_of_lines