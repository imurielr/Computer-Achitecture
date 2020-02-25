""" Module containg the codeWrite class for the VM translator. """

class CodeWriter:
    """ Translates VM commands into Hack assembly code. """

    def __init__(self, output_file):
        """ Opens the output file and gets ready to write into it. """
        output_file_name = output_file + ".asm"
        self.file = open(output_file_name, "w+")
        self.current_file = None
        self.command_counter = 0

    def set_file_name(self, file_name):
        """ Informs the code writer that the translation of a new VM file is started. """
        self.current_file = file_name

    def write_arithmetic(self, command):
        """ Writes the assembly code that is the translation of the given arithmetic command """
        # Create a list to store all the assembly commands and write them later
        translated_commands = []
        if command == "add":
            translated_commands.append("@SP")
            translated_commands.append("AM=M-1")
            translated_commands.append("D=M")
            translated_commands.append("A=A-1")
            translated_commands.append("M=D+M")
        elif command == "sub":
            translated_commands.append("@SP")
            translated_commands.append("AM=M-1")
            translated_commands.append("D=M")
            translated_commands.append("A=A-1")
            translated_commands.append("M=M-D")
        elif command == "neg":
            translated_commands.append("@SP")
            translated_commands.append("A=M-1")
            translated_commands.append("M=-M")
        elif command == "eq":
            translated_commands.append("@SP")
            translated_commands.append("AM=M-1")
            translated_commands.append("D=M")
            translated_commands.append("A=A-1")
            translated_commands.append("D=M-D")
            translated_commands.append("@TRUE{}".format(self.command_counter))
            translated_commands.append("D;JEQ")
            translated_commands.append("@SP")
            translated_commands.append("A=M-1")
            translated_commands.append("M=0")
            translated_commands.append("@END{}".format(self.command_counter))
            translated_commands.append("0;JMP")
            translated_commands.append("(TRUE{})".format(self.command_counter))
            translated_commands.append("@SP")
            translated_commands.append("A=M-1")
            translated_commands.append("M=-1")
            translated_commands.append("(END{})".format(self.command_counter))
            self.command_counter += 1
        elif command == "gt":
            translated_commands.append("@SP")
            translated_commands.append("AM=M-1")
            translated_commands.append("D=M")
            translated_commands.append("A=A-1")
            translated_commands.append("D=M-D")
            translated_commands.append("@TRUE{}".format(self.command_counter))
            translated_commands.append("D;JGT")
            translated_commands.append("@SP")
            translated_commands.append("A=M-1")
            translated_commands.append("M=0")
            translated_commands.append("@END{}".format(self.command_counter))
            translated_commands.append("0;JMP")
            translated_commands.append("(TRUE{})".format(self.command_counter))
            translated_commands.append("@SP")
            translated_commands.append("A=M-1")
            translated_commands.append("M=-1")
            translated_commands.append("(END{})".format(self.command_counter))
            self.command_counter += 1
        elif command == "lt":
            translated_commands.append("@SP")
            translated_commands.append("AM=M-1")
            translated_commands.append("D=M")
            translated_commands.append("A=A-1")
            translated_commands.append("D=M-D")
            translated_commands.append("@TRUE{}".format(self.command_counter))
            translated_commands.append("D;JLT")
            translated_commands.append("@SP")
            translated_commands.append("A=M-1")
            translated_commands.append("M=0")
            translated_commands.append("@END{}".format(self.command_counter))
            translated_commands.append("0;JMP")
            translated_commands.append("(TRUE{})".format(self.command_counter))
            translated_commands.append("@SP")
            translated_commands.append("A=M-1")
            translated_commands.append("M=-1")
            translated_commands.append("(END{})".format(self.command_counter))
            self.command_counter += 1
        elif command == "and":
            translated_commands.append("@SP")
            translated_commands.append("AM=M-1")
            translated_commands.append("D=M")
            translated_commands.append("A=A-1")
            translated_commands.append("M=D&M")
        elif command == "or":
            translated_commands.append("@SP")
            translated_commands.append("AM=M-1")
            translated_commands.append("D=M")
            translated_commands.append("A=A-1")
            translated_commands.append("M=D|M")
        elif command == "not":
            translated_commands.append("@SP")
            translated_commands.append("A=M-1")
            translated_commands.append("M=!M")

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.file.write(line + "\n")
    
    def write_push_pop(self, command_type, segment, index):
        """ Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP """

        # Get the segment translation to assembler for the ones that behave similarly
        assembler_segment = None
        if segment == "argument":
            assembler_segment = "ARG"
        elif segment == "local":
            assembler_segment = "LCL"
        elif segment == "this":
            assembler_segment = "THIS"
        elif segment == "that":
            assembler_segment = "THAT"

        # Create a list to store all the assembly commands and write them later
        translated_commands = []
        if segment == "argument" or segment == "local" or segment == "this" or segment == "that":
            if command_type == "C_PUSH":
                translated_commands.append("@{}".format(assembler_segment))
                translated_commands.append("D=M")
                translated_commands.append("@{}".format(index))
                translated_commands.append("A=D+A")
                translated_commands.append("D=M")
                translated_commands.append("@SP")
                translated_commands.append("A=M")
                translated_commands.append("M=D")
                translated_commands.append("@SP")
                translated_commands.append("M=M+1")
            elif command_type == "C_POP":
                translated_commands.append("@{}".format(assembler_segment))
                translated_commands.append("D=M")
                translated_commands.append("@{}".format(index))
                translated_commands.append("D=D+A")
                translated_commands.append("@R13")
                translated_commands.append("M=D")
                translated_commands.append("@SP")
                translated_commands.append("AM=M-1")
                translated_commands.append("D=M")
                translated_commands.append("@R13")
                translated_commands.append("A=M")
                translated_commands.append("M=D")
        elif segment == "static":
            if command_type == "C_PUSH":
                translated_commands.append("@{}".format(16 + index))
                translated_commands.append("D=M")
                translated_commands.append("@SP")
                translated_commands.append("A=M")
                translated_commands.append("M=D")
                translated_commands.append("@SP")
                translated_commands.append("M=M+1")
            elif command_type == "C_POP":
                translated_commands.append("@SP")
                translated_commands.append("AM=M-1")
                translated_commands.append("D=M")
                translated_commands.append("@{}".format(16 + index))
                translated_commands.append("M=D")
        elif segment == "constant":
            if command_type == "C_PUSH":
                translated_commands.append("@{}".format(index))
                translated_commands.append("D=A")
                translated_commands.append("@SP")
                translated_commands.append("A=M")
                translated_commands.append("M=D")
                translated_commands.append("@SP")
                translated_commands.append("M=M+1")
            elif  command_type == "C_POP":
                print("ERROR: illegal command, cannot pop a value into a constant")
                exit(1)
        elif segment == "pointer":
            if command_type == "C_PUSH":
                translated_commands.append("@{}".format(3 + index))
                translated_commands.append("D=M")
                translated_commands.append("@SP")
                translated_commands.append("A=M")
                translated_commands.append("M=D")
                translated_commands.append("@SP")
                translated_commands.append("M=M+1")
            elif command_type == "C_POP":
                translated_commands.append("@SP")
                translated_commands.append("AM=M-1")
                translated_commands.append("D=M")
                translated_commands.append("@{}".format(3 + index))
                translated_commands.append("M=D")
        elif segment == "temp":
            if command_type == "C_PUSH":
                translated_commands.append("@{}".format(5 + index))
                translated_commands.append("D=M")
                translated_commands.append("@SP")
                translated_commands.append("A=M")
                translated_commands.append("M=D")
                translated_commands.append("@SP")
                translated_commands.append("M=M+1")
            elif command_type == "C_POP":
                translated_commands.append("@SP")
                translated_commands.append("AM=M-1")
                translated_commands.append("D=M")
                translated_commands.append("@{}".format(5 + index))
                translated_commands.append("M=D")

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.file.write(line + "\n")

    def close(self):
        """ Closes the file previouly opened. """
        self.file.close()