from pyHasher import hash,normalisePy
import sys;

	
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
		dumpAssertFail(f1,f2)
		print('assertTrue FAIL: ', f1, " != ", f2)		
		return 0
		
def dumpAssertFail(f1,f2):
	""" Normalises two files and outputs to file
	Input:
		f1,f2- files to be normalised
	Output:
		Creates two files: f1-dump and f2-dump local directory of f1 and f2.
		return - None
	"""
	
	minifier = normalisePy(f1)
	f1=open(f1+"-dump","wb")
	if sys.version_info.major == 3:
		f1.write(bytes(minifier,'UTF-8'))
	else: 
		f1.write(minifier)
	f1.close()
	minifier = normalisePy(f2)
	f2=open(f2+"-dump","wb")
	if sys.version_info.major == 3:
		f2.write(bytes(minifier,'UTF-8'))
	else: 
		f2.write(minifier)
	f2.close()

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
		dumpAssertFail(f1,f2)
		print('assertFalse FAIL: ', f1, " == ", f2,)
		return 0
		
		


def main():
	#Determine version number:
	#python3: Minimum 3.3 is required.
	#python2.x: Needs to be run from Python 2.7
	testDir = 'test_cases'
	if sys.version_info.major == 3:
		if sys.version_info.minor >= 3:
			testDir = testDir + "/" + "2.x tests"
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
	total = 15
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
	success += assertFalseHash('docstrings.py', 'docstrings2.py',testDir);
	#Tests indiscriminate removal of docstrings
	success += assertTrueHash('docstrings.py', 'docstrings3.py',testDir);	
	success += assertTrueHash('docstrings.py', 'docstrings4.py',testDir);		
	print("Simple whitebox testing: ",success," out of ",total, " passed.", total-success," failed")	; 

	
if __name__ == '__main__':
	main()