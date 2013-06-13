"""Its bad if this docstring is removed"""
class testobject:
	def __init__(self):
		print "hello world"

if __name__ == '__main__':
	print __doc__
	testobject()
	