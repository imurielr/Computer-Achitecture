""" 
Module containing the main to run the translation for the virtual matchine.

It uses the Parser and CodeWriter classes to read .vm file and generates a .asm file 
containing the translation to the assembly language.
"""

import sys

from vm_parser import Parser
from code_writer import CodeWriter

def main():

    # If there is an invalid number of arguments the program stops.
    if len(sys.argv) != 2:
        print("ERROR: Invalid number of arguments. Expected: file_name.vm ")
        exit(1)
    # the VM translator only accepts vm files to be translated into assembly files.
    elif sys.argv[1][-3:] != ".vm":
        print("ERROR: Invalid file type. Expected: vm file")   
        exit(1)

    # Get the name of the file to be parsed from the arguments.
    input_file = sys.argv[1]

    # Creates a new parser to parse the file.
    parser = Parser(input_file)
    # Creates the code writer with the input file excluding the .vm part
    code_writer = CodeWriter(input_file[0:-3])

    # Reads the whole file.
    while parser.has_more_commands():
        parser.advance()
        # Gets the command type from the current command.
        command_type = parser.command_type()
        # If the command type is C_ARITHMETIC parses it to get the command and passes it to the code writer to add it to the output file
        if command_type == "C_ARITHMETIC":
            command = parser.arg1()
            code_writer.write_arithmetic(command)
         # If the command type is C_PUSH or C_POP parses it to get the segment and the index and passes it to the code writer to add it to the output file
        elif command_type == "C_PUSH" or command_type == "C_POP":
            segment = parser.arg1()
            index = parser.arg2()
            code_writer.write_push_pop(command_type, segment, index)
    
    del parser
    code_writer.close()

if __name__ == "__main__":
    main()