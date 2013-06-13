"""This is a docstring. Sometimes they get referenced by code..
referenced strings like this one should not be deleted"""

class testobject:
	"""this docstring is not going to be referenced, so it should be remove"""
	def __init__(self):
		"""doc strings can
		be
		multi line"""
		print("hello world")

if __name__ == '__main__':
	print(__doc__)
	testobject()
	