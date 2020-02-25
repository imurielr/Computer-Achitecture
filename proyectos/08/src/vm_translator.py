""" 
Module containing the main to run the translation for the virtual matchine.

It uses the Parser and CodeWriter classes to read .vm file and generates a .asm file 
containing the translation to the assembly language.
"""

import sys
import os

from vm_parser import Parser
from code_writer import CodeWriter

def main():

    # If there is an invalid number of arguments the program stops.
    if len(sys.argv) != 2:
        print("ERROR: Invalid number of arguments. Expected: file_name.vm ")
        exit(1)
    # The VM translator accepts directories or vm files to be translated into assembly files.
    elif not os.path.isdir(sys.argv[1]) and sys.argv[1][-3:] != ".vm":
        print("ERROR: Invalid argument. Expected: directory or vm file")   
        exit(1)

    # Get the name of the file to be parsed from the arguments.
    input_file = sys.argv[1]

    if os.path.isdir(input_file):
        # Split the file path
        file_path = input_file.split("/")
        if input_file.endswith("/"):
            # Creates the code writer with the given directory
            code_writer = CodeWriter("{}/{}".format(input_file, file_path[-2]))
            read_directory(input_file, code_writer)
            code_writer.close()
        else:
            # Creates the code writer with the given directory
            code_writer = CodeWriter("{}/{}".format(input_file, file_path[-1]))
            read_directory(input_file, code_writer)
            code_writer.close()
    else:
        # Creates the code writer with the input file excluding the .vm part
        code_writer = CodeWriter(input_file[0:-3])
        read_file(input_file, code_writer)
        code_writer.close()

def read_directory(input_directory, code_writer):
    """ Reads each vm file in directory and translates them using the read_file function """

    vm_files = []
    
    for root, _, files in os.walk(input_directory):
        for file_name in files:
            if file_name.endswith(".vm"):
                vm_files.append(file_name)

    if len(vm_files) == 1:
        read_file(os.path.join(root, vm_files[0]), code_writer)
    elif len(vm_files) > 1:
        code_writer.write_init()
        for file in vm_files:
            read_file(os.path.join(root, file), code_writer)
    else:
        print("ERROR: Missing VM files")
        exit(1)
    
def read_file(input_file, code_writer):
    """ Reads and translates to assembly code a single file """

    # Creates a new parser to parse the file.
    parser = Parser(input_file)

    # Set the current file name to be input file
    code_writer.set_file_name(input_file[0:-3])

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
        # If the command type is C_LABEL parses it to get the label and passes it to the code writer to add to the output file
        elif command_type == "C_LABEL":
            label = parser.arg1()
            code_writer.write_label(label)
        # If the command type is C_GOTO parses it to get the label and passes it to the code writer to add to the output file
        elif command_type == "C_GOTO":
            label = parser.arg1()
            code_writer.write_goto(label)
        # If the command type is C_IF parses it to get the label and passes it to the code writer to add to the output file
        elif command_type == "C_IF":
            label = parser.arg1()
            code_writer.write_if(label)
        elif command_type == "C_CALL":
            function_name = parser.arg1()
            num_args = parser.arg2()
            code_writer.write_call(function_name, num_args)
        # If the command type is C_RETURN passes it to the code writer to add it to the output file.
        elif command_type == "C_RETURN":
            code_writer.write_return()
        # If the command type is C_FUNCTION parses it to get the function name and number of local variables and passes it to the code writer to add to the output file
        elif command_type == "C_FUNCTION":
            function_name = parser.arg1()
            num_locals = parser.arg2()
            code_writer.write_function(function_name, num_locals)
    
    del parser

if __name__ == "__main__":
    main()