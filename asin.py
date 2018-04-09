'''
--------------------------------------------------------------------------------------
======================================================================================

This is the main file for the project that executes the tasks of the Asin interpreter.
Aside from running the interpreter with ./asin <filename>, you may also enter the
command python asin.py <filename> which would work just as well.

======================================================================================
--------------------------------------------------------------------------------------
'''
import sys
from asinyacc import *
from asinerrs import *
from asintable import asin

sys.tracebacklimit = 5
arglen = len(sys.argv)
if arglen == 1:
    '''
    If no command line parameter pertaining to a file for use with Asin is
    specified, print a guiding message.
    '''
    guide = """

        Greetings, user! If you do not know how to use the Asin interpreter,
        kindly follow the instructions below so that you can be able to
        run your program.

        Maligayang bati, user! Kung lingid man sa iyong kaalaman kung paano
        gamitin ang interpreter ng Asin, maaari lamang sanang iyong sundin
        ang panuto sa ibaba upang patakbuhin ang iyong program:

            Unix-like OS: ./asin <filename>
            Windows     : asin.exe <filename>
    """
    asin()
    print(guide)
elif arglen == 2:
    '''
    If a file (as an argument) is entered into the command line interface after the asin.exe
    interpreter executable, and only one file, parse and perform the instructions as compliant
    with the syntax of Asin.
    '''
    try:
        '''
        Run the program through the Asin interpreter
        '''
        source = open(sys.argv[1], 'r')
        sourceCode = source.read()
        sourceLines = source.readlines()

        parser = buildParser()
        program = parser.parse(sourceCode)

        for grain in program.grains:
            grain.pinch()

        source.close()
    except FileNotFoundError:
        '''
        If file does not existent
        '''
        raise MaalatAtNawawalangFile(sys.argv[1])
    except Exception as alat:
        '''
        If some other error occurs
        '''
        print(alat.__class__.__name__ + ' ' + str(alat), file=sys.stderr)
else:
    '''
    If more than one argument file is passed after the asin.exe interpreter executable,
    and only one file, print a guiding message
    '''
    guide = """
        Paumanhin, sapagka't hindi alam ng Asin ang gagawin sa {}
        na mga ipinasang argumento pagkalampas sa \"{}\".

        Sundin ang panuto:
            ./asin <filename>
    """.format(arglen - 1, sys.argv[1])
    print(guide)