"""
Very simple testscripts for failsafe mnfy.
Author: Dulitha Ranatunga, Last Modified: August 2013
"""

import unittest
from mnfy import *

class TestMnfy(unittest.TestCase):
	def test_EmptyDocString(self):
		input=""
		expected ="" 
		self.assertEqual(removeOneLineDocStrings(input),expected)
		
	def test_OneLineDocString(self):
		input="\"\"\" hello world \"\"\""
		expected=""
		self.assertEqual(removeOneLineDocStrings(input),expected)
		input="\"\"\" hello world \"\"\" hello back"
		expected="hello back"
		self.assertEqual(removeOneLineDocStrings(input),expected)
		input="this=\"\"\"is not a docstring\"\"\""
		expected="this=\"\"\"is not a docstring\"\"\""
		self.assertEqual(removeOneLineDocStrings(input),expected)
		
	def test_MultiLineDocstring(self):
		input="\"\"\" This comment has no bounds"
		expected="\"\"\" This comment has no bounds"
		self.assertEqual(removeOneLineDocStrings(input),expected)
	
	def test_EmptyTabReplacement(self):
		input=""
		expected=""
		self.assertEqual(replaceTabsWithSpaces(input),expected)
		input=""
		expected="   "
		self.assertNotEqual(replaceTabsWithSpaces(input),expected)
	
	
	def test_SpacesTabReplacement(self):
		input="   "
		expected="   "
		self.assertEqual(replaceTabsWithSpaces(input),expected)
		input="   "
		expected="\t"
		self.assertNotEqual(replaceTabsWithSpaces(input),expected)
		
	
	def test_TabReplacement(self):
		input="\t"
		expected="   "
		self.assertEqual(replaceTabsWithSpaces(input),expected)
		input="\tHelloWorld!"
		expected="   HelloWorld!"
		self.assertEqual(replaceTabsWithSpaces(input),expected)
		input="\t\t\tMultiTabs"
		expected="         MultiTabs"
		self.assertEqual(replaceTabsWithSpaces(input),expected)
		
	
	def test_EmptyStripFile(self):
		input="testFiles/empty.py"
		output=""
		self.assertEqual(stripFile(input),output)
	
	def test_OneLineStripFile(self):
		input="testFiles/oneline.py"
		output='print("Hello World!")'
		self.assertEqual(stripFile(input),output)
	
	def test_MultiLineStripFile(self):
		input="testFiles/multiline.py"
		output='def helloworld():\n   butNot="""this one"""\n   """Or this multiline\n      tab indented comment"""\n   print("helloworld")\nif __name__ == "__main__":\n   helloworld()'
		self.assertEqual(stripFile(input),output)

if __name__ == "__main__":
	unittest.main()