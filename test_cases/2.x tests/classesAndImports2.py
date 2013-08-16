#This program prints hello world twice
import sys

class HelloWorldGenerator():
	"""Wooo a docstring"""
	def __init__(self):
		#functions might not just have comments
		print "HelloWorld"
		self.str = "Hello World"
	
	def sayHello(self):
		print self.str

def main():
	hwg = HelloWorldGenerator()
	hwg.sayHello()
	
	
if __name__ == '__main__':
	main()