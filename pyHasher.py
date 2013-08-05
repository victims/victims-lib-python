"""
Normalises and hashes python files using mnfy.
Author: Dulitha Ranatunga, Last Modified: August, 2013.
"""

import sys
import ast
import hashlib
import subprocess

###CONFIG###
"""
Set the environment name of your system here. e.g.
if typing 'python hello.py' runs 'hello.py' in Python2.7 then, PY27_ENV_NAME='python'
if typing 'python3 hello.py' runs 'hello.py' in Python3.3 then,
PY33_ENV_NAME='python3'
"""

PY27_ENV_NAME='python'
PY33_ENV_NAME='python3'
#############

def runInEnv(version,filepath):
	"""
	Opens up a subprocess and executes mnfy in a different python environment.
	Input:
		- version - python environment to run [2 or 3]
		- filepath - file to be normalised
	Output: (success,minifiedFile) where
		- success - 1 if the subproccess returned without error, else 0
		- minifiedFile - stdout of running mnfy on file.
	"""
	#print("Running " + filepath + " in env:"+str(version))
	if version == 2:
		env= PY27_ENV_NAME
		mnfypath='libs/mnfy273/mnfy.py'
	elif version == 3:
		env= PY33_ENV_NAME
		mnfypath='libs/mnfy3300/mnfy.py'
	else:
		return (0,None)
	# Put stderr and stdout into pipes
	proc = subprocess.Popen([env,mnfypath,filepath,"--safe-transforms"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	return_code = proc.wait()
	# Read from pipes
	if return_code:
		return (0,None)
	else:
		file=""
		for line in proc.stdout:
			file += line.decode("utf-8")
		return(1,file[:-1])	
	

def mnfy3(filepath):
	"""Calls the mnfy3.3 module to normalise a python 3.x file
	Input:
		filepath- path to be normalised
	Output: 
		SourceCode object. Call str(minifier) to get final source code.
	"""
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
	return minifier
	
def mnfy2(filepath):
	"""Calls the mnfy2.7 module to normalise a python 2.x file
	Input:
		filepath- path to be normalised
	Output: 
		SourceCode object. Call str(minifier) to get final source code.
	"""
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
	return minifier

def mnfyFailSafe(filepath):
	"""As a final backup, this is a very simplistic comment and white-space remover.
	Input:
		filepath- path to be normalised
	Output: 
		String: white-space and comment removed source of filepath.
	"""
	from libs.mnfyFailSafe.mnfy import stripFile
	return stripFile(filepath)

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
		#try 3, then 2, then failsafe
		try:
			minifier= mnfy3(filepath);
			
		except:
			success,minifier = runInEnv(2,filepath)
			if not success:
				minifier = mnfyFailSafe(filepath)
				
		
	elif sys.version_info.major == 2:
		import pdb
		
		#try 2, then 3, then failsafe
		try:
			minifier= mnfy2(filepath);
		except:		
			success,minifier = runInEnv(3,filepath)
			if not success:
				minifier = mnfyFailSafe(filepath)

	else:
		minifier = mnfyFailSafe(filepath)
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
	
	#print(printedFile)
	m = hashlib.sha512()
	for line in printedFile:
		
		m.update(line.encode('utf-8'))
	return m.hexdigest()
	
	
def main():
	#Run tests
	import argparse
	arg_parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	arg_parser.add_argument('filename',
							help='path to Python source file')
	arg_parser.add_argument('--dump', action='store_true',
                            default=False,
							help='toggle printing of source')						
	args = arg_parser.parse_args()
	
	print(hash(args.filename))
	if (args.dump):
		print(normalisePy(args.filename))


	
	
if __name__ == '__main__':
	main()