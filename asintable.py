'''
======================================================================================
--------------------------------------------------------------------------------------

This file contains the hash table of variables and function names and values

--------------------------------------------------------------------------------------
======================================================================================
'''
import math
from asinerrs import *
from asinhelper import *

class HashTable:
    '''
    Represents a pseudo-hash table as a list of two dictionaries
    '''
    def __init__(self):
        '''
        SYMBOLS and FUNCTIONS pertain to the indices of the table, and is for our convenience only.

        TABLE is a list of two dictionaries; the first stores variable identifiers as keys pointing
        to their respective values, the second stores Asin's built-in functions.
        '''
        self.SYMBOLS = 0
        self.FUNCTIONS = 1

        self.TABLE = [{},{}]

    def setVar(self, varName, value):
        '''
        Assigns a value to an identifier. The value will become accessible
        through the key, varName.
        '''
        self.TABLE[self.SYMBOLS][varName] = value

    def getVar(self, varName):
        '''
        Returns the value accessible through the key, varName.
        If not found, raise an error akin to Python's NameError.
        '''
        if varName in self.TABLE[self.SYMBOLS]:
            return self.TABLE[self.SYMBOLS][varName]
        raise MaalatNaSimbolo(varName)

    def delVar(self, varName):
        '''
        Removes an identifier, and consequently the value bound to it,
        from the first dictionary
        '''
        del self.TABLE[self.SYMBOLS][varName]

    def setFunc(self, funcName, func):
        '''
        Assigns a function to a name. The function (func) becomes accessible
        through the key, funcName.

        NOTE: This function is only used for loading Asin's built-in functions;
              the language lacks support for user-defined functions.
        '''
        self.TABLE[self.FUNCTIONS][funcName] = func

    def getFunc(self, funcName):
        '''
        Returns the function specified by the key, funcName. If not
        found, raise an error akin to Python's NameError
        '''
        if funcName in self.TABLE[self.FUNCTIONS]:\
            return self.TABLE[self.FUNCTIONS][funcName]
        raise MaalatNaSimbolo(funcName)


# ====================================================================================
#                          ~: Asin's Functions (and loader) :~
# ====================================================================================

def palitan(array: list, index, value):
    '''
    Asin function for replacing a value in a list
    '''
    try:
        array[index] = value
    except TypeError:
        raise MaalatNaIndeks(index.__class__.__name__, index)
    except IndexError:
        raise MaalatNaIndeks(index, array, 0, len(array) - 1)

def idagdag(array: list, value):
    '''
    Asin function for appending values to an array
    '''
    array.append(value)

def tanggalan(array: list):
    '''
    Asin function for popping values from an array
    '''
    return array.pop()

def silipin(array: list):
    '''
    Asin function for getting the rightmost element of an array
    '''
    return array[-1]

def isaayos(array: list, descending: bool=False):
    '''
    Asin function for sorting an array using Python's native sort() function
    '''
    if descending:
        array.sort(reverse=True)
    else:
        array.sort()

def baligtarin(array: list):
    '''
    Asin function for reversing an array using Python's native reverse() function
    '''
    array.reverse()

def baligtad(array: list):
    '''
    Asin function for returning a reversed version of the list argument
    '''
    return list(reversed(array))

def buksan(file, access):
    '''
    Asin function for opening a file
    '''
    try:
        return open(file, access)
    except FileNotFoundError:
        raise MaalatAtNawawalangFile(file)

def basahin(file):
    '''
    Asin function for entirely reading a file
    '''
    return file.read()

def linya(file):
    '''
    Asin function for getting a line from a file at the cursor's current position
    '''
    return file.readline()

def isulat(file, toWrite):
    '''
    Asin function for writing something into a file
    '''
    file.write(toWrite)

def isara(file):
    '''
    Asin function for closing a file
    '''

def asin():
    '''
    This is a superficial function that prints "Asin" in Old English,
    a pile of salt made out of ASCII characters and the language's
    author's names
    '''
    image = """                                                                                    
               .+ydNMMMNdy+.  :oo`                     .`                          
             -dMNhso++oydMMMmmy                       od.                          
            +My-  ./oso:o:/NMM:               .y+     o`                           
           .M:   ohoshMs`  hMM/         ::`    sh   `/`       :.     --            
           :d    .  `o:    hMM+     `-odMMMNdhds` `yNMNy`  `+mMMy `/dMMy/+`        
            d`     :o`     hMM+     mMM+./+osd-    :MMM:   ` +MMM/:dmmMMh          
            `s:  `s:```````hMMo     mMM+   +h`     .MMM.     :MMM    hMMs          
              -+oNMMMMMMMMMMMMs     mMMms/dMMMdo   .MMM.     :MMM    hMMs          
              `o:..........dMMy     .+hNN+ -yMMM   .MMM.     :MMM    hMMs          
             /Nds/.       -mMMh       :s.   :MMM   .MMM.     :MMM    hMMs          
            syhmMMMNho:.++-yMMM/+:  `yNhddyooMMM   `MMM/-`   oMMM:   yMMd.-        
           -N.  `:smMMh/   .mMNs.  :NdssymMMh+-`    sMMy-   .sNMm+   -mMd+`        

                                       ( S A L T )

                                             `:`                                  
                                           `-mNms:`                               
                                         .+hhNNNNNNh-                             
                                       -sdddNNNNNNNNNo`                           
                                     :hdmhmNNNNNNNNNNNo                           
                                    :dmmNddNNNNNNNNNNNNs`                         
                                   :yNmmmmhNNNNNNNNNNNNNd/`                       
                                .+hmmmmmmmyNNNNNNNNNNNNNNNmy.                     
                              :yddmdmmmNmmhNNNNNNNNNNNNNNNNNmo-`                  
                           `:smmNmmNmmmmdhNNNNNNNNNNNNNNNNNNNNNdo.                
                          :dmNdmNmmmmmmhdNNNNNNNNNNNNNNNNNNNNNNNNd-               
                         :dmdNmmmmdmmmhNNNNNNNNNNNNNNNNNNNNNNNNNNNm+`             
                      `:smNNmmmNmmNmmhNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNh`            
                     /dmdNmmmmmNddddmNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN+            
             ````..:ommmmmmmmmmmmydNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNmo.`         
         ```..-yhydmdmmmmmNmdmmmmhNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNdo-:-```   
      ` ``.--`.:::/ohdddmmmNmmmdddmNNNNNNmNNNNNNNNNNNNNNNNNNNNNdsyhdddmdh+--..`   
         ``   `  .::--`.--.-.::/:odmmmNNNNNNmdhddh+ooso::/::/+/:-`-` `.-.`.-`` `  
                          ``  `.-...-://osoo-::--.`` `                            
    
               Proyekto sa CS 150: Programming Languages, nina
                       Don Rodolfo Abril y Padilla at Jerico Silapan y Lim"""
    print(image)

def kargahan(hashtable: HashTable):
    '''
    Loader function to add all built-in variables and
    functions to the hash table for use in Asin programs
    '''

    # SYMBOLS

    # mathematical constants
    hashtable.setVar('asin_pi', math.pi)
    hashtable.setVar('asin_e', math.e)

    # FUNCTIONS

    # typecasting functions
    hashtable.setFunc('bilang', AsinFunction(int)) # typecast to int
    hashtable.setFunc('lutang', AsinFunction(float)) # typecast to flaot
    hashtable.setFunc('titik', AsinFunction(str)) #typecast to string

    # math functions
    hashtable.setFunc('halaga', AsinFunction(abs)) # absolute value
    hashtable.setFunc('ibilog', AsinFunction(round)) # rounding off
    hashtable.setFunc('putulin', AsinFunction(math.trunc)) # truncation of fractional values (float -> integer)
    hashtable.setFunc('kisame', AsinFunction(math.ceil)) # ceiling function
    hashtable.setFunc('sahig', AsinFunction(math.floor)) # floor function
    hashtable.setFunc('iangat', AsinFunction(math.pow)) # exponentiation
    hashtable.setFunc('ibaba', AsinFunction(math.log)) # logarithmic function
    hashtable.setFunc('parisugat', AsinFunction(math.sqrt)) # square root

    hashtable.setFunc('maximo', AsinFunction(max)) # returns maximum value in list
    hashtable.setFunc('minimo', AsinFunction(min)) # returns minimum value in list

    hashtable.setFunc('haba', AsinFunction(len)) # returns the length of an iterable

    # list functions
    hashtable.setFunc('palitan', AsinFunction(palitan)) # replaces a value in a list at a certain index
    hashtable.setFunc('idagdag', AsinFunction(idagdag)) # appends a value to a list
    hashtable.setFunc('tanggalan', AsinFunction(tanggalan)) # pops a value from the list
    hashtable.setFunc('silipin', AsinFunction(silipin)) # returns the value of the last element of the list
    hashtable.setFunc('baligtarin', AsinFunction(baligtarin)) # reverses a list in-place
    hashtable.setFunc('baligtad', AsinFunction(baligtad)) # return a reversed version of the list argument

    # list functions (sorting)
    hashtable.setFunc('isaayos', AsinFunction(isaayos)) # sort a list in-place
    hashtable.setFunc('nakaayos', AsinFunction(sorted)) # return a sorted version of the list argument

    # file I/O
    hashtable.setFunc('pahingi', AsinFunction(input)) # prompts for user input through CLI
    hashtable.setFunc('buksan', AsinFunction(buksan)) # creates a file object
    hashtable.setFunc('basahin', AsinFunction(basahin)) # gets all the contents of a file
    hashtable.setFunc('linya', AsinFunction(linya)) # gets a line from the file at the cursor
    hashtable.setFunc('isulat', AsinFunction(isulat)) # writes contents to a file
    hashtable.setFunc('isara', AsinFunction(isara)) # closes a file

    # prints "Asin" and a salt pile in ASCII characters
    hashtable.setFunc('asin', AsinFunction(asin))