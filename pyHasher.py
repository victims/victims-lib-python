import sys
import ast
import hashlib


def normalisePy(filepath):
	"""
	This module uses the 'mnfy' module to create a semantically equivalent
	and minimised/normalised python source file ready for hashing.
	
	Input::
		filepath - path/to/sourcefile.py to be normalised.
	
	Output::
		returns string containing entire source file.
	"""
	#Check version (3.3 or 2.7) to decide which mnfy to use.
	#minify the python file	
	minifier = "";
	if sys.version_info.major == 3:
		from libs.mnfy3300.mnfy import SourceCode,safe_transforms
		with open(filepath, 'rb') as source_file:
			source = source_file.read()
		source_ast = ast.parse(source)
		#safe_transforms
		for transform in safe_transforms:
			transformer = transform()
			source_ast = transformer.visit(source_ast)
		minifier = SourceCode()
		minifier.visit(source_ast)			
	elif sys.version_info.major == 2:
		from libs.mnfy273.mnfy import SourceCode,safe_transforms
		with open(filepath, 'rb') as source_file:
			source = source_file.read()
		source_ast = ast.parse(source)
		#safe_transforms
		for transform in safe_transforms:
			transformer = transform()
			source_ast = transformer.visit(source_ast)
		minifier = SourceCode()
		minifier.visit(source_ast)			
	#Final source file
	return (str(minifier))

def hash(filepath):
	"""
	Takes the file path of a .py file and returns a hash for the minified
	version of it.
	Input: 
		- filepath: path of a ".py" file.
	
	Output:
		- sha512 hash of it. 
	"""
	printedFile = normalisePy(filepath)
	#hash
	
	print(printedFile)
	m = hashlib.sha512()
	for line in printedFile:
		
		m.update(line.encode('utf-8'))
	return m.hexdigest()
	
	
def assertTrueHash(f1,f2, test_dir=""):
	""" hashes two python files and checks if they are equivalent
	Input:
		test_dir is a prefix folder path to the file if they are both
		in the same folder
	Output:
		returns 1 if they are the same
	"""
	f1 = test_dir + "/" + f1;
	f2 = test_dir + "/" + f2;
	
	if hash(f1) == hash(f2):
		print('assertTrue PASS: ', f1, " == " , f2)
		return 1
	else:
		print('assertTrue FAIL: ', f1, " != ", f2)
		return 0

def assertFalseHash(f1,f2, test_dir=""):
	""" hashes two python files and checks if they are equivalent
	Input:
		test_dir is a prefix folder path to the file if they are both
		in the same folder
	Output:
		returns 1 if they are not the same
	"""
	if not test_dir == "":
		f1 = test_dir + "/" + f1;
		f2 = test_dir + "/" + f2;
		
	if hash(f1) != hash(f2):
		print('assertFalse PASS: ', f1, " != " , f2)
		return 1
	else:
		print('assertFalse FAIL: ', f1, " == ", f2,)
		return 0
		
		
def main():
	#Determine version number:
	#python3: Minimum 3.3 is required.
	#python2.x: Needs to be run from Python 2.7
	testDir = 'test_cases';
	if sys.version_info.major == 3:
		if sys.version_info.minor >= 3:
			testDir = testDir + "/" + "3.x tests"
		else:
			print ("Python version found: ", sys.version_info.major,".", sys.version_info.minor)
			print("Python version >= 3.3 or Python 2.7 required to run, input files do not need to be under this requirement")
			return -1;
	elif sys.version_info.major == 2:
		if sys.version_info.minor >= 7:
			testDir = testDir + "/" + "2.x tests"
		else:
			print("Python version >= 3.3 or Python 2.7 required to run, input files do not need to be under this requirement")
			return -1;
	
	### TESTS ###
	success = 0
	total = 14
	success += assertTrueHash('emptyFile.py','emptyFile2.py',testDir);
	success += assertTrueHash('helloworld.py','helloworld.py',testDir);
	success += assertTrueHash('helloworld.py','helloworld2.py',testDir);
	success += assertTrueHash('helloworld.py','helloworld3.py',testDir);
	success += assertTrueHash('helloworld.py','helloworld4.py',testDir);
	success += assertTrueHash('helloworld3.py','helloworld4.py',testDir);
	success += assertTrueHash('classesAndImports.py','classesAndImports2.py',testDir);
	success += assertTrueHash('dictionary.py','dictionary2.py',testDir);
	success += assertFalseHash('indent.py','indent2.py',testDir);
	success += assertFalseHash('helloworld.py', 'emptyFile2.py', testDir);
	success += assertFalseHash('helloworld4.py','helloworld5.py',testDir);
	success += assertFalseHash('emptyFile.py', 'classesAndImports.py',testDir);
	success += assertFalseHash('docstrings.py', 'docstrings2.py',testDir);	#Tests indiscriminate removal of docstrings
	success += assertTrueHash('docstrings.py', 'docstrings3.py',testDir);		
	print(success," out of ",total, " passed.", total-success," failed")	; 

if __name__ == '__main__':
	main()