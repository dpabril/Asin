'''
--------------------------------------------------------------------------------------
======================================================================================

This file contains the exceptions of Asin, raised upon encountering errors

======================================================================================
--------------------------------------------------------------------------------------
'''
class Maalat(Exception):
    '''
    class Maalat is the parent class bearing the error message
    reporting facility through its __str__ method
    '''
    def __init__(self):
        '''
        Exception classes that inherit Maalat have their own definitions
        of the __init__ method; arguments are passed from the other
        source files to be placed and formatted within strings
        '''
        raise NotImplementedError()
    def __str__(self):
        '''
        Allows the error message to be reported as it is
        processed through the parent class, Exception
        '''
        return self.errorReport

class MaalatAtNawawalangFile(Maalat):
    '''
    MaalatAtNawawalangFile is raised when a file passed to the interpreter
    is not found; analogous to Python's FileNotFoundError
    '''
    def __init__(self, filename):
        self.errorReport = "(InexistentFileError) : File \"{}\" not found".format(filename)
    pass

class MaalatNaOperasyon(Maalat):
    '''
    MaalatNaPagpapatakbo is analogous to Python's TypeError;
    raised when performing invalid operations with respect to operand types
    '''
    def __init__(self, *args):
        if len(args) == 6:
            self.errorReport = "(TypeError) : Invalid operation: \"{} {} {}\" <~ ({} {} {})".format(*args)
        else:
            self.errorReport = "(TypeError) : Invalid operation: \"{} {}\" <~ ({} {})".format(*args)
    pass

class MaalatNaAritmetika(Maalat):
    '''
    MaalatNaAritmetika is analogous to Python's ArithmeticError;
    raised when dividing by zero
    '''
    def __init__(self, *args):
        self.errorReport = "(ArithmeticError) : Invalid operation: Dividing {} ({}) by zero (0)".format(*args)
    pass

class MaalatNaSimbolo(Maalat):
    '''
    MaalatNaSimbolo is analogous to Python's NameError for unknown
    identifiers; raised when attempting to get the value of a variable
    or call a function with an undefined identifier
    '''
    def __init__(self, varName):
        self.errorReport = "(NameError) : \"{}\" is not a defined variable name".format(varName)
    pass

class MaalatNaLeksim(Maalat):
    '''
    MaalatNaKarakter is raised during the lexing phase when running an
    Asin program, as an unrecognized token is encountered (lexical error)
    '''
    def __init__(self, *args):
        self.errorReport = "(LexicalError) : Line {}: Column {}: Unrecognized token \"{}\"\n    in \"{}\"".format(*args)
    pass

class MaalatNaPalaugnayan(Maalat):
    '''
    MaalatNaPalaugnayan is raised during the parsing phase
    of an Asin program, when a syntax error is encountered
    '''
    def __init__(self, *args):
        if len(args) == 4:
            self.errorReport = "(SyntaxError) : Line {}: Column {}: offending token \"{}\", no matching grammar rule\n    in \"{}\"" .format(*args)
        else:
            self.errorReport = "(SyntaxError) : Reached unexpected end of input"
    pass

class MaalatNaIndeks(Maalat):
    '''
    MaalatNaIndeks is raised when there are mistakes in accessing an index of a list;
    either the index is not an integer, or is out of bounds of the list's index range
    '''
    def __init__(self, *args):
        if len(args) == 2:
            self.errorReport = "(TypeError) : {} ~> \"{}\" is not a valid index; index should be of type int".format(*args)
        else:
            self.errorReport = "(IndexError) : Index (= {}) is not within the list's ({}) index range ({} to {})".format(*args)
    pass