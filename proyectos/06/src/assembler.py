""" 
Script that contains the main to run the translation for the Hack language.

It uses the Parser, Code and SymbolTable classes.

HOW IT WORKS:
    - First it reads through the assembler language file and looks for the labels to add them to the symbol table.
    - Then reads through the file again and recognizes the type of command in each line (ignoring comments)
        If the command type is "C_COMMAND" it translates the command to its binary code.
        If the command type is "A_COMMAND" and the variable is not in the table, it adds it and translates it to its binary code,
        if the variable exist in the table it translates it to its binary code
"""

import sys

from parser import Parser
from code import Code
from symbol_table import SymbolTable

def main():

    # If there is an invalid number of arguments the program stops.
    if len(sys.argv) != 2:
        print("ERROR: Invalid number of arguments. Expected: file_name.asm ")
        exit(1)
    # The assembler only accepts asm files to be translated into hack files
    elif sys.argv[1][-4:] != ".asm":
        print("ERROR: Invalid file type. Expected: asm file")   
        exit(1)    

    input_file = sys.argv[1]

    # Initialize the symbol table with the predefined symbols.
    symbol_table = SymbolTable()
    translator_c_command = Code()

    # Counters to keep track of the ROM and RAM memory address.
    count_ROM = 0
    count_variable = 16

    # List containing all the translated commands from the file.
    commands_translation = []

    # First pass
    parser = Parser(input_file)
    # Reads the whole file.
    while parser.has_more_commands():
        parser.advance()
        # Checks if the current command is has a label to and adds it to the table.
        if parser.command_type() == "L_COMMAND":
            # Takes the symbol from the label.
            label = parser.symbol()
            # Check if the label does not start with a number and adds the symbol to the table.
            if not label[0].isdigit():
                symbol_table.add_entry(label, count_ROM)
            else:
                print("ERROR: invalid label indentifier")
                exit(1)
        else:
            # If it finds an A_COMMAND or C_COMMAND adds one to the ROM counter.
            count_ROM += 1

    # Reset the parser pointer to read the file
    parser.file.seek(0)

    # Second pass

    #Reads the whole file
    while parser.has_more_commands():
        parser.advance()
        # Checks if the current command is type "A_COMMAND".
        if parser.command_type() == "A_COMMAND":
            # Get the variable
            variable = parser.symbol()
            # Checks the variable starts with a letter.
            if not variable[0].isdigit():
                # If the table does not contain the symbol, adds it to the table, does the translation to binary code, 
                # adds it to the list of translations and ads one to the RAM counter.
                if not symbol_table.contains(variable):
                    symbol_table.add_entry(variable, count_variable)
                    binary_address = "{:016b}".format(count_variable)
                    commands_translation.append(binary_address)
                    count_variable += 1
                # If the table contains the symbol, gets the address associated with the symbol,
                # does the translation to binary code and adds it to the translated list.
                else:
                    address = symbol_table.get_address(variable)
                    binary_address = "{:016b}".format(address)
                    commands_translation.append(binary_address)
            # Check if the variable is a number, translates it to its binary code and adds it to the translated list.
            elif variable.isdigit():
                binary_address = "{:016b}".format(int(variable))
                commands_translation.append(binary_address)
            # If the variable is not a number o starts with a letter theres a mistake in the command and the program stops.
            else:
                print("ERROR: The symbol " + variable + " is invalid")
                exit(1)
        # Check if the current command is type "C_COMMAND".
        elif parser.command_type() == "C_COMMAND":
            # Gets the dest, comp and jump mnemonic.
            command_dest = parser.dest()
            command_comp = parser.comp()
            command_jump = parser.jump()

            # Translates each mnemonic into its binary code.
            binary_dest = translator_c_command.dest(command_dest)
            binary_comp = translator_c_command.comp(command_comp)
            binary_jump = translator_c_command.jump(command_jump)
            # Put together all the binary codes addring three '1's at the beging and adds it to the translated list.
            binary_code = "111" + binary_comp + binary_dest + binary_jump
            commands_translation.append(binary_code)
            
    # Creates the hack file using the input file
    dot_index = input_file.find(".")
    hack_file = input_file[:dot_index] + ".hack"
    # Opens the hack file, if it does not exist creates it
    file = open(hack_file, "w")
    # For each command in the translated list, writes the binary code on the hack file and adds a new line
    for command in commands_translation:
        file.write(command)
        file.write("\n")
    # Close the hack file
    file.close()
    exit(0)

if __name__ == "__main__":
    main()