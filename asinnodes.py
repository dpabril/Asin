'''
--------------------------------------------------------------------------------------
======================================================================================

This file contains the definitions for Asin's abstract syntax tree. If checking the
documentation of this file, please check along with the docstrings in 'asinhelper.py'

======================================================================================
--------------------------------------------------------------------------------------
'''
import asintable
from asinerrs import *
from asinhelper import *

# Getting the (pseudo-)hash table (in the form of a list two dictionaries)
Table = asintable.HashTable()
asintable.kargahan(Table)

def pinchAll(expression):
    while isinstance(expression, Grain):
        expression = expression.pinch()
    return expression

# ====================================================================================
#                              ~: AST Node definitions :~
# ====================================================================================

class SaltBlock:
    '''
    SaltBlock represents a block of code, a clause, or comma-separated expressions.
    We called it SaltBlock, as many grains (class Grain) clumped together make a block of salt
    '''
    def __init__(self, grains=None):
        '''
        The list "grains" represents the children nodes of the SaltBlock object
        '''
        if grains is None:
            grains = []
        self.grains = grains
    def __len__(self):
        '''
        Allows other functions to know the length of the grains list within a SaltBlock object
        '''
        return len(self.grains)
    def __iter__(self):
        '''
        defines an iterable within the class that refers to a SaltBlock object's grains variable
        '''
        return iter(self.grains)
    def pinch(self):
        toReturn = []
        for i in self:
            if isinstance(i, ExitStmt):
                # returns an ExitStmt instance that will trigger a 'break'
                return i
            result = i.pinch()
            if isinstance(result, ExitStmt):
                # returns an ExitStmt instance that will trigger a 'break'
                return result
            elif result is not None:
                toReturn.append(result)
        return toReturn

class Primitive(Grain):
    '''
    Primitive is a class for primitive values (integer, float, string, true, false)
    '''
    def __init__(self, value):
        self.value = value
    def pinch(self):
        return self.value

class Identifier(Grain):
    '''
    Identifier is a class that represents a variable's name
    '''

    # by default, an identifier is assumed not to refer to a function
    isfunc = False
    def __init__(self, identifier):
        self.identifier = identifier
    def bindToValue(self, value):
        '''
        Adds an entry to the hash table attaching a value to the identifier
        '''
        Table.setVar(self.identifier, value)
    def selfDestruct(self):
        '''
        Deletes the entry that has key=identifier from the hash table
        '''
        Table.delVar(self.identifier)
    def pinch(self):
        if not self.isfunc:
            return Table.getVar(self.identifier)
        else:
            return Table.getFunc(self.identifier)

class Array(Grain):
    '''
    Array trivially represents an an array/list similar to Python's
    '''
    def __init__(self, entries: SaltBlock = None):
        self.entries = entries
    def pinch(self):
        if self.entries is not None:
            return self.entries.pinch()
        else:
            return []

class BinOp(Grain):
    '''
    BinOp is an expression class representative of binary operations
    '''
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def pinch(self):
        left = self.left.pinch()
        right = self.right.pinch()

        try:
            # Arithmetic
            if self.op == '+':
                returnValue = left + right
            elif self.op == '-':
                returnValue = left - right
            elif self.op == '*':
                returnValue = left * right
            elif self.op == '/':
                returnValue = left / right
            elif self.op == '//':
                returnValue = left // right
            elif self.op == '**':
                returnValue = left ** right
            elif self.op == '%':
                returnValue = left % right
            # Comparison
            elif self.op == '==':
                returnValue = left == right
            elif self.op == '!=':
                returnValue = left != right
            elif self.op == '>':
                returnValue = left > right
            elif self.op == '>=':
                returnValue = left >= right
            elif self.op == '<':
                returnValue = left < right
            elif self.op == '<=':
                returnValue = left <= right
            # Logical
            elif self.op == 'at':
                returnValue = left and right
            elif self.op == 'o':
                returnValue = left or right
            return returnValue

        except TypeError:
            # raise an error when the operation on two operands doesn't work
            raise MaalatNaOperasyon(left, self.op, right, left.__class__.__name__, self.op, right.__class__.__name__)
        except ArithmeticError:
            # raise an error when dividing an numerical expression by 0
            raise MaalatNaAritmetika(left.__class__.__name__, left)

class UnaOp(Grain):
    '''
    UnaOp is a class that handles the 'not' and '-' operators for
    singular expressions (i.e. of the form [operator][expression])
    '''
    def __init__(self, op, expression):
        self.op = op
        self.expression = expression
    def pinch(self):
        if self.op == '-':
            operand = self.expression.pinch()
            try:
                return -(operand)
            except TypeError:
                raise MaalatNaOperasyon('-', operand.__class__.__name__, '-', operand)
        elif self.op == 'hindi':
            return not(self.expression.pinch())

class AssignStmt(Grain):
    '''
    AssignStmt is instantiated when a value is being assigned to a variable
    '''
    def __init__(self, ident: Identifier, value):
        self.ident = ident
        self.value = value
    def pinch(self):
        self.ident.bindToValue(self.value.pinch())

class CompAssignStmt(Grain):
    '''
    CompAssignStmt is instantiated when a compund assignment operation is being performed
    '''
    def __init__(self, ident: Identifier, op, value):
        self.ident = ident
        self.op = op
        self.value = value
    def pinch(self):
        try:
            operator = ''
            if self.op == '+=':
                operator = '+'
            elif self.op == '-=':
                operator = '-'
            elif self.op == '*=':
                operator = '*'
            elif self.op == '/=':
                operator = '/'
            elif self.op == '//=':
                operator = '//'
            elif self.op == '**=':
                operator = '**'
            elif self.op == '%=':
                operator = '%'

            oldVal = self.ident.pinch()
            val = self.value.pinch()

            if operator == '+':
                self.ident.bindToValue(oldVal + val)
            elif operator == '-':
                self.ident.bindToValue(oldVal - val)
            elif operator == '*':
                self.ident.bindToValue(oldVal * val)
            elif operator == '/':
                self.ident.bindToValue(oldVal / val)
            elif operator == '//':
                self.ident.bindToValue(oldVal // val)
            elif operator == '**':
                self.ident.bindToValue(oldVal ** val)
            elif operator == '%':
                self.ident.bindToValue(oldVal % val)
        except TypeError:
            raise MaalatNaOperasyon(oldVal, operator, val, oldVal.__class__.__name__, operator, val.__class__.__name__)

class IfStmt(Grain):
    '''
    IfStmt is instantiated when an if-conditional statement is processed
    '''
    def __init__(self, condition, ifSeg: SaltBlock, elseSeg = None):
        self.condition = condition
        self.ifSeg = ifSeg
        self.elseSeg = elseSeg
    def pinch(self):
        if self.condition.pinch():
            return self.ifSeg.pinch()
        elif self.elseSeg is not None:
            return self.elseSeg.pinch()

class WhileStmt(Grain):
    '''
    WhileStmt is instantiated when a while-statement is encountered;
    a SaltBlock object as the loop body is run as long as the condition holds true
    '''
    def __init__(self, condition, loopBody: SaltBlock):
        self.condition = condition
        self.loopBody = loopBody
    def pinch(self):
        while self.condition.pinch():
            loopBodyRes = self.loopBody.pinch()
            if isinstance(loopBodyRes, ExitStmt):
                break
                
class ForStmt(Grain):
    '''
    ForStmt is instantiated when the interpreter reads a for-loop clause;
    the loop body (a SaltBlock object) will be run from <start> to <end>
    '''

    def __init__(self, iterator: Identifier, start, end, loopBody: SaltBlock):
        self.iterator = iterator
        self.start = start
        self.end = end
        self.loopBody = loopBody
    def pinch(self):
        begin = self.start.pinch()
        finish = self.end.pinch() + 1
        for count in range(begin, finish):
            self.iterator.bindToValue(count)
            loopBodyRes = self.loopBody.pinch()
            if isinstance(loopBodyRes, ExitStmt):
                break
        self.iterator.selfDestruct()


class PrintStmt(Grain):
    '''
    PrintStmt handles the printing pseudo-function of Asin
    '''
    def __init__(self, toPrint: SaltBlock):
        self.toPrint = toPrint
    def pinch(self):
        toPrintList = self.toPrint.pinch()
        print(*toPrintList)

class ExitStmt(Grain):
    '''
    ExitStmt is the class for handling a break statement
    '''
    def __iter__(self):
        return []
    def pinch(self):
        pass

class ArrAccess(Grain):
    '''
    ArrAccess represents an instruction to access an array at a certain index
    '''
    def __init__(self, arrName: Identifier, index):
        self.arrName = arrName
        self.index = index
    def pinch(self):
        arrId = self.arrName.pinch()
        elemPos = self.index.pinch()
        if elemPos.__class__.__name__ != 'int':
            # raise TypeError
            raise MaalatNaIndeks(elemPos.__class__.__name__, elemPos)
        elif elemPos >= len(arrId) or elemPos < -len(arrId):
            # raise IndexError
            raise MaalatNaIndeks(elemPos, arrId, 0, len(arrId) - 1)
        else:
            return self.arrName.pinch()[elemPos]

class AsinFunctionCall(Grain):
    '''
    An AsinFunctionCall object/node is instantiated when a function call
    (as per the grammar) is encountered. Please refer to class AsinFunction
    for additional information
    '''
    def __init__(self, funcName: Identifier, arguments: SaltBlock = None):
        self.funcName = funcName
        self.arguments = arguments
    def pinch(self):
        function = self.funcName.pinch()
        argList = []

        if self.arguments is not None:
            for arg in self.arguments:
                argList.append(pinchAll(arg))

        # returns a Python function in the dictionary, encapsulated
        # by AsinFunction which has a defined pinch() function
        return function.pinch(argList)