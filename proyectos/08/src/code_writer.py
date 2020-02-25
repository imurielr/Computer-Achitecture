""" Module containg the codeWrite class for the VM translator. """

class CodeWriter:
    """ Translates VM commands into Hack assembly code. """

    def __init__(self, output_file):
        """ Opens the output file and gets ready to write into it. """
        output_file_name = output_file + ".asm"
        self.file = open(output_file_name, "w+")
        self.current_file = None
        self.current_function = None
        self.command_counter = 0
        self.return_counter = 0

    def write_init(self):
        """ Writes the assembly code that effects the VM initialization. --> Also called bootstrap """
        
        self.set_file_name("Sys")
       
        # SP = 256 ---> Initializa the stack pointer to 0x0100
        self.file.write("@256\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")
        # Call Sys.init --->  Invoke Sys.init
        self.write_call("Sys.init", 0)
    
    def set_file_name(self, path):
        """ Informs the code writer that the translation of a new VM file is started. """

        # Split the file path
        file_path = path.split("/")
        # Take the file name
        file_name = file_path[-1]
        # Update the current file
        self.current_file = file_name

    def set_function_name(self, function_name):
        """ Informs the code writer that the translation of a new VM function is started. """
        self.current_function = function_name

    def write_arithmetic(self, command):
        """ Writes the assembly code that is the translation of the given "arithmetic" command """
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

        # Create a list to store all the assembly commands and write them later
        translated_commands = []
        
        # Get the address for the command and write it into the output file.
        self.get_address(segment, index)

        if command_type == "C_PUSH":
            if segment == "constant":
                translated_commands.append("D=A")
            else:
                translated_commands.append("D=M")
            translated_commands.append("@SP")
            translated_commands.append("A=M")
            translated_commands.append("M=D")
            translated_commands.append("@SP")
            translated_commands.append("M=M+1")
        elif command_type == "C_POP":
            translated_commands.append("D=A")
            translated_commands.append("@R13")
            translated_commands.append("M=D")
            translated_commands.append("@SP")
            translated_commands.append("AM=M-1")
            translated_commands.append("D=M")
            translated_commands.append("@R13")
            translated_commands.append("A=M")
            translated_commands.append("M=D")

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.file.write(line + "\n")

    
    def get_address(self, segment, index):
        """ Get the address for the assembler segment and write it into the output file. """
        
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
            translated_commands.append("@{}".format(assembler_segment))
            translated_commands.append("D=M")
            translated_commands.append("@{}".format(index))
            translated_commands.append("A=D+A")
        elif segment == "constant":
            translated_commands.append("@{}".format(index))
        elif segment == "static":
            translated_commands.append("@{}.{}".format(self.current_file, index))
        elif segment == "pointer":
            translated_commands.append("@R{}".format(3 + index)) 
        elif segment == "temp":
            translated_commands.append("@R{}".format(5 + index)) 

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.file.write(line + "\n")              
    
    def write_label(self, label):
        """ Writes the assembly code that is the translation of the given "label" command """

        # Label declaration.
        self.file.write("({}:{})\n".format(self.current_file.upper(), label.upper()))

    def write_goto(self, label):
        """ Writes the assembly code that is the translation of the given "goto" command """

        # Create a list to store all the assembly commands and write them later
        translated_commands = []

        # Unconditional jump to the VM command following the label.
        translated_commands.append("@{}:{}".format(self.current_file.upper(), label.upper()))
        translated_commands.append("0;JMP")

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.file.write(line + "\n")

    def write_if(self, label):
        """ Writes the assembly code that is the translation of the given "if-goto" command """

        # Create a list to store all the assembly commands and write them later
        translated_commands = []

        # Pops the topmost stack element.
        # If it's not zero, jumps to the VM command following the label
        translated_commands.append("@SP")
        translated_commands.append("AM=M-1")
        translated_commands.append("D=M")
        translated_commands.append("@{}:{}".format(self.current_file.upper(), label.upper()))
        translated_commands.append("D;JNE")

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.file.write(line + "\n")

    def write_call(self, function_name, num_args):
        """ Writes the assembly code that is the translation of the given "call" command """

        # Update the current function.
        self.set_function_name(function_name)

        # Create a list to store all the assembly commands and write them later
        translated_commands = []

        # Store the return address in a local variable to use later.
        return_address = "RETURN_{}{}".format(self.current_function.upper(), self.return_counter)
        self.return_counter += 1
        # Push the return address
        translated_commands.append("@{}".format(return_address))
        translated_commands.append("D=A")
        translated_commands.append("@SP")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        translated_commands.append("@SP")
        translated_commands.append("M=M+1")
        # Push LCL
        translated_commands.append("@LCL")
        translated_commands.append("D=M")
        translated_commands.append("@SP")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        translated_commands.append("@SP")
        translated_commands.append("M=M+1")
        # Push ARG
        translated_commands.append("@ARG")
        translated_commands.append("D=M")
        translated_commands.append("@SP")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        translated_commands.append("@SP")
        translated_commands.append("M=M+1")
        # Push THIS
        translated_commands.append("@THIS")
        translated_commands.append("D=M")
        translated_commands.append("@SP")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        translated_commands.append("@SP")
        translated_commands.append("M=M+1")
        # Push THAT
        translated_commands.append("@THAT")
        translated_commands.append("D=M")
        translated_commands.append("@SP")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        translated_commands.append("@SP")
        translated_commands.append("M=M+1")
        # ARG = SP - n - 5. n being the number of arguments.
        translated_commands.append("@SP")
        translated_commands.append("D=M")
        num = int(num_args) + 5   # n + 5
        translated_commands.append("@{}".format(num))
        translated_commands.append("D=D-A")  # D = SP -(n + 5)
        translated_commands.append("@ARG")
        translated_commands.append("M=D")
        # LCL = SP
        translated_commands.append("@SP")
        translated_commands.append("D=M")
        translated_commands.append("@LCL")
        translated_commands.append("M=D")
        # goto f. f being function_name.
        translated_commands.append("@{}".format(self.current_function.upper()))
        translated_commands.append("0;JMP")
        translated_commands.append("({})".format(return_address))

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.file.write(line + "\n")

    def write_return(self):
        """ Writes the assembly code that is the translation of the given "return" command """

        # Create a list to store all the assembly commands and write them later
        translated_commands = []

        # FRAME = LCL  --> R14
        translated_commands.append("@LCL")
        translated_commands.append("D=M")
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("M=D")
        # RET = *(FRAME-5)  --> R15
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("D=M")  # D = FRAME
        translated_commands.append("@5")
        translated_commands.append("A=D-A")   # A = FRAME - 5
        translated_commands.append("D=M")   # D = *(FRAME - 5)
        translated_commands.append("@R15")  # RET
        translated_commands.append("M=D")
        # *ARG = pop()
        translated_commands.append("@SP")
        translated_commands.append("AM=M-1")
        translated_commands.append("D=M")
        translated_commands.append("@ARG")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        # SP = ARG + 1
        translated_commands.append("@ARG")
        translated_commands.append("D=M")
        translated_commands.append("@SP")
        translated_commands.append("M=D+1")
        # THAT = *(FRAME - 1)
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("D=M")
        translated_commands.append("@1")
        translated_commands.append("A=D-A")  # FRAME - 1
        translated_commands.append("D=M")   # D = *(FRAME - 1)
        translated_commands.append("@THAT")
        translated_commands.append("M=D")   # THAT = *(FRAME - 1)
        # THIS = (FRAME - 2)
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("D=M")
        translated_commands.append("@2")
        translated_commands.append("A=D-A") # FRAME - 2
        translated_commands.append("D=M")   # D = *(FRAME - 2)
        translated_commands.append("@THIS")
        translated_commands.append("M=D")   # THIS = *(FRAME - 2)
        # ARG = (FRAME - 3)
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("D=M")
        translated_commands.append("@3")
        translated_commands.append("A=D-A")  # FRAME - 3
        translated_commands.append("D=M")  # D = *(FRAME - 3)
        translated_commands.append("@ARG")
        translated_commands.append("M=D")   # ARG = *(FRAME - 3)
        # LCL = (FRAME - 4)
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("D=M")
        translated_commands.append("@4")
        translated_commands.append("A=D-A")  # FRAME - 4
        translated_commands.append("D=M")   # D = *(FRAME - 4)
        translated_commands.append("@LCL")
        translated_commands.append("M=D")   # LCL = *(FRAME - 4)
        # goto RET
        translated_commands.append("@R15")  # RET 
        translated_commands.append("A=M")
        translated_commands.append("0;JMP")

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.file.write(line + "\n")

    def write_function(self, function_name, num_locals):
        """ Writes the assembly code that is the translation of the given "Function" command. """   

        # Create a list to store all the assembly commands and write them later
        translated_commands = []
        
        # Declare label for function entry.
        translated_commands.append("({})".format(function_name.upper())) 
        # Allocate a memory address for each local variable initialized in 0.
        for _ in range(num_locals):
            translated_commands.append("@SP")
            translated_commands.append("A=M")
            translated_commands.append("M=0")  
            translated_commands.append("@SP")
            translated_commands.append("M=M+1")   

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.file.write(line + "\n")

    def close(self):
        """ Closes the file previouly opened. """
        self.file.close()