""" Module containing the main for the Jack compiler """

from antlr4 import *

from JackLexer import JackLexer
from JackListener import JackListener
from JackParser import JackParser
from jack_listener import Listener
from jack_symbol_table import JackSymbolTable
from jack_vm_writer import JackVMWriter

from catch_error import CatchError

import sys
import os

def main(argv):

    # If there is an invalid number of arguments the program stops.
    if len(sys.argv) != 2:
        print("ERROR: Invalid number of arguments. Expected: file_name.jack or directory ")
        exit(1)
    # The Jack translator accepts directories or jack files to be translated into XML files.
    elif not os.path.isdir(sys.argv[1]) and sys.argv[1][-5:] != ".jack":
        print("ERROR: Invalid argument. Expected: directory or jack file")   
        exit(1)

    # Get the name of the file to be parsed from the arguments.
    file_name = sys.argv[1]

    # Check if the given argument is a directory or a file and read it
    if os.path.isdir(file_name):
        read_directory(file_name)
    else:
        input_stream = FileStream(file_name)
        read_file(file_name, input_stream)

def read_directory(input_directory):
    """ Reads each jack file in directory and translates them into XML output files """

    jack_files = []  # List to store all the jack files found in the given directory

    # Go through the entire directiry and store each jack file in the jack_files list
    for root, _, files in os.walk(input_directory):
        for file_name in files:
            if file_name.endswith(".jack"):
                jack_files.append(file_name)

    # If there is only one file in the directory, take the input file, create the file stream and read the file
    if len(jack_files) == 1:
        input_file = os.path.join(root, jack_files[0])
        input_stream = FileStream(input_file)
        read_file(input_file, input_stream)
    # If there are more than one files in the directory, take each file and create the file stream to read it.
    elif len(jack_files) > 1:
        for file_name in jack_files:
            input_file = os.path.join(root, file_name)
            input_stream = FileStream(input_file)
            read_file(input_file, input_stream)
    # If there are no jack file in the directory stop the program
    else:
        print("ERROR: Missing jack files")
        exit(1)

def read_file(file_name, input_stream):
    """ Read the given file using the input_stream to parse it """

    output_file = "{}.vm".format(file_name[:-5])  # Create the output xml file 

    try:
        lexer = JackLexer(input_stream)  # Create the lexer using the input stream
        stream = CommonTokenStream(lexer)  # Create the stream to have access to each token 
        parser = JackParser(stream)  # Create the parse using the created stream
        parser.removeErrorListeners()
        parser.addErrorListener(CatchError())
        tree = parser.classNT()  # Parse starting from the classNT rule
    except SyntaxError as error:
        print(error)
        exit(1)
    vm_writer = JackVMWriter(output_file)
    symbol_table = JackSymbolTable()
    listener = Listener(parser, vm_writer, symbol_table)   # Create a new listener to parse the jack file into the output file
    ParseTreeWalker.DEFAULT.walk(listener, tree)  # Use the created listener and tree to parse the entire file using the Jack grammar
     # Delete all the created objects
    del lexer, stream, parser, tree, listener
    
if __name__ == '__main__':
    main(sys.argv)
