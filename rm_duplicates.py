#! /usr/bin/python3

"""
rm_duplicates.py removes file duplicates from a directory recursively or prints them on standard output stream.

It accepts following command line arguments:
	-p:	print a list of duplicate file names together with their digest (content hash values). Commented
		out lines, the ones starting with '#', represent files which will be kept after removing duplicates.
	-d:	remove/delete duplicates. If there are multiple files having identical content, then only one
		per unique content will remain after the removal of duplicates. The file with shortest name
		(path + file name) stays.
	path:	path to a directory from which all duplicates are removed recursively (i.e. duplicates removed
		from all arbitrary nested subdirectories as well). If path is not supplied then current working
		directory is used.
-p and -d are mutually exclusive. Use one or the other but not both.
Command line arguments can be supplied in any order.
Prints help if no arguments supplied or used incorrectly. Print error message if invalid directory supplied.

Examples:
	./rm_duplicates.py -p /home/viktor/Documents
		Prints duplicates found in specified directory.
	./rm_duplicates.py /home/viktor/Documents -p
		Does the same thing. Argument order doesn't matter.
	./rm_duplicates.py -d /home/viktor/Documents
		Removes duplicates from specified directory.
	./rm_duplicates.py
		Prints help.
"""

import os, sys, hashlib 

def walk(dirname):
	"""
	It is a generator function generating file names (path + name) found in directory supplied
	as an argument. It descends recursively into all subdirectories.
	"""
	for name in os.listdir(dirname):
		path = os.path.join(dirname, name)
		if os.path.isfile(path) and not os.path.islink(path):
			yield path
		elif os.path.isdir(path) and not os.path.islink(path):
			yield from walk(path)

def file_digest(file):
	"Returns sha1 hash value calculated for the content of a file supplied as an argument. "
	with open(file, 'rb') as f:
		hash_alg = hashlib.sha1()
		hash_alg.update(f.read())
	return hash_alg.hexdigest()


class Unique_content:
	"""
	One instance of the class represents unique file content and keeps a list of file names having this content.
	self.digest and self.file must hold values at all times.
	self.rest holds a list of duplicates. If self.rest is empty it means that there is only one file with such content.
	self.size holds file size in bytes.
	"""
	def __init__(self, digest, file, size):
		self.digest = digest
		self.file = file
		self.size = size
		self.rest = []

	def __str__(self):
		head = '#{0}\t{1}'.format(self.digest, self.file)
		if self.rest:
			rows = [' {0}\t{1}'.format(self.digest, f) for f in self.rest]
			tail = '\n'.join(rows)
			return '{0}\n{1}'.format(head, tail)
		else:
			return head

	def append(self, file):
		"""
		Appends a file.
		NOTE: User must supply a file with the same digest as in self.digest which was set during initialisation.
		"""
		self.rest.append(file)

	def reorder(self):
		"After reordering self.file gets the shortest name (path + file), self.rest gets the rest."
		self.rest.append(self.file)
		self.rest.sort(key=lambda s: len(s))
		self.file = self.rest.pop(0)

	def remove_duplicates(self):
		"Removes list of files from self.rest and from a file system."
		while self.rest:
			file = self.rest.pop()
			os.remove(file)

	def get_redundancy_size(self):
		"Returns total size in bytes of all redundant files/duplicates."
		return self.size * len(self.rest)

	def get_redundant_files_count(self):
		"Returns total count of all redundant files/duplicates."
		return len(self.rest)


class Unique_content_directory:
	"It is a container and controller of Unique_content instances."
	def __init__(self):
		self.files = {}

	def __str__(self):
		body = '\n'.join([str(self.files[k]) for k in self.files])
		stats = '#\t{0} files can be deleted freeing\n#\t{1} bytes of space'.format(
				self.get_redundant_files_count(),
				self.get_redundancy_size())
		return body + '\n' + stats if body else stats

	def append(self, file):
		"Appends file to self.files by creating a new Unique_content instance or appending to the existing one."
		digest = file_digest(file)
		size = os.path.getsize(file)
		if digest in self.files:
			self.files[digest].append(file)		# Making sure Unique_content.append() is used correctly
		else:
			self.files[digest] = Unique_content(digest, file, size)

	def reorder(self):
		for k, v in self.files.items():
			v.reorder()	

	def remove_singles(self):
		"Removes Unique_content instances without duplicates."
		self.files = {k: v for k, v in self.files.items() if v.rest}

	def remove_duplicates(self):
		"Removes duplicates from each Unique_content instance."
		for k, v in self.files.items():
			v.remove_duplicates()

	def get_redundancy_size(self):
		total = 0		
		for k, v in self.files.items():
			total += v.get_redundancy_size()
		return total

	def get_redundant_files_count(self):
		total = 0
		for k, v in self.files.items():
			total += v.get_redundant_files_count()
		return total
		

def help():
	print(__doc__)
	sys.exit(1)

def validate_arguments():
	"""
	Validates comand line arguments and returns tuple consisting of a flag (eitehr '-p' or '-d') and optional path.
	If path wasn't supplied then None is returned instead of path string. It is not checked if path represents a directory.
	"""
	args_list = sys.argv[1:]
	args = set(args_list)
	if len(args_list) != len(args):	# Duplicates in command line arguments
		help()
	known_flags = set(['-p', '-d'])
	flags = set([arg for arg in args if arg.startswith('-')])
	rest = args - flags

	if len(flags - known_flags):	# Unexpected flags on command line
		help()
	if len(flags) != 1:		# Only one flag is expected, either -p or -d
		help()
	if len(rest) > 1:		# There can be only one (optional) non flag argument - directory path
		help()
	flag = flags.pop()
	path = rest.pop() if rest else None
	return flag, path


def main():
	flag, path = validate_arguments()

	# directory is either valid path specifying directory or it's current working directory
	if path:
		if os.path.isdir(path) and not os.path.islink(path):
			directory = path
		else:
			print('Error: path must specify a directory.')
			sys.exit(1)
	else:
		directory = os.getcwd()

	# Populate unique content directory with files from directory
	content_dir = Unique_content_directory()
	for file in walk(directory):
		content_dir.append(file)
	content_dir.remove_singles()	# Keep only content with duplicates
	content_dir.reorder()		# Reorder so that after deletion of duplicates shortest file names are kept

	# Depending on the flag print list of files to remove or actually remove them
	if flag == '-p':
		print(content_dir)
	elif flag == '-d':
		content_dir.remove_duplicates()

if __name__ == '__main__':
	main()

