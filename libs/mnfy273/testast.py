"""Test AST"""

import ast

class FirstParser(ast.NodeVisitor):

    def __init__(self):
        pass

    def visit_Print(self, node):
		print 
		print "print",
		if node.dest:
			print ">>", str(node.dest)
		if (node.dest is not None) and (len(node.values)>0):
			print ",",
		if len(node.values) >= 1:
			for val in node.values[:-1]:
				if isinstance(val,ast.Str):
					self.visit(val)
					print ",",
			val = node.values[-1]
			if isinstance(val,ast.Str):
				self.visit(val)
		if not node.nl:
			print ","
			
		print 
	      
    def visit_Str(self,node):
        print repr(node.s),

def main():
    import optparse
    parser = optparse.OptionParser(__doc__.strip())
    opts, args = parser.parse_args()

    if not args:
        parser.error("You need to specify the name of Python files to print out.")

    import traceback
    for fn in args:
        print '\n\n%s:\n' % fn
        try:
            with open(fn, 'rb') as source_file:
                source = source_file.read()
            source_ast = ast.parse(source)  
            fp = FirstParser()
            fp.visit(source_ast)
        except SyntaxError, e:
            traceback.print_exc()

if __name__ == '__main__':
    main()	  