'''
--------------------------------------------------------------------------------------
======================================================================================

This is the file where we put two classes that caused problems when placed in the
file for abstract syntax tree nodes. The errors were caused by circular imports in
the files that need the two classes below, so we created another file that upon
importing, would circumvent the errors altogether.

======================================================================================
--------------------------------------------------------------------------------------
'''
class Grain:
    '''
    Represents a node in the abstract syntax tree, as do classes that inherit it.
    We called it Grain, as a grain of salt is a singular unit
    '''
    def pinch(self):
        '''
        Generally, pinch() is the function used by the program to evaluate the contents
        of nodes in the AST. pinch() is defined and overriden by other classes that inherit Grain.
        We called it pinch, pertaining to the act of getting a pinch of salt
        '''
        raise NotImplementedError()

class AsinFunction(Grain):
    '''
    AsinFunction encapsulates a native Python function for use with Asin
    '''
    def __init__(self, funcName):
        self.funcName = funcName

    def pinch(self, arguments):
        return self.funcName(*arguments)