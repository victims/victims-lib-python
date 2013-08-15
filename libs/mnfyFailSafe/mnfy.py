"""
A very basic minifier of python code.
Author: Dulitha Ranatunga, Last Modified: August 2013
"""

def removeOneLineDocStrings(line):
	"""Removes one line docstrings such as this one"""
	"""
	Input:
		-source: line
	Output:
		-oneline docstrings stripped, or original line.
	"""
	temp = line.lstrip()
	if len(temp) >= 3 and temp[:3] == "\"\"\"":
		temp = temp[3:]
		if "\"\"\"" in temp:
			temp = temp[temp.find("\"\"\"")+3:]
			return temp.lstrip()
	return line

def replaceTabsWithSpaces(line,numSpaces=3):
	"""Replaces \t in the leading indentation with spaces
	Input: 
		- line: line to be replaced
		- numSpaces: number of spaces for each tab.
	Output:
		- line
	"""
	index = (len(line)-len(line.lstrip()))
	return line[:index].expandtabs(numSpaces)+line[index:]
	

def stripFile(filepath):
	"""Given a sourcecode file, this will:
		-Remove one line docstrings
		-Replace indentation-tabs with spaces
		-Remove trailing comments and whitespace
		-Note: \n line endings are returned.
	Input:
		filepath - file to be stripped
	Output:
		a single string containing the entire transformed source code
	"""
	with open(filepath,'r') as source_file:
		source = source_file.readlines()
	newSource =""
	for line in source:
		line = replaceTabsWithSpaces(line);
		line = line.partition('#')[0]#remove comments
		line = removeOneLineDocStrings(line) #remove one line doc strings
		line = line.rstrip() #remove white space
		if len(line) > 0 and not line.isspace():
			newSource += line + "\n"
	if len(newSource)> 0 and newSource[-1] == '\n':
		return newSource[:-1]
	return newSource
	
def main():
	#Run tests
	import argparse
	arg_parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	arg_parser.add_argument('filename',
							help='path to Python source file')
	args = arg_parser.parse_args()
	
	print(stripFile(args.filename))


	
	
if __name__ == '__main__':
	main()