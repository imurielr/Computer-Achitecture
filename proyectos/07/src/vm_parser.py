"""
Parser module for the virtual matchine 
"""

class Parser:
    """ Handles the parsing of a single .vm file, and encapsulates access to the input code.
        It reads VM commands, parses them, and provides convenient access to their components. """
    
    # Static list containing all the arthmetic commands
    arithmetic_commads = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

    segments = ["argument", "local", "static", "constant", "this", "that", "pointer", "temp"]

    def __init__(self, input_file):
        """ Opens the input file and gets ready to parse it. """
        self.file = open(input_file, "r")
        self.current_command = None

    def __del__(self):
        """ Closes the file previouly opened. """
        self.file.close()

    def has_more_commands(self):
        """ Checks if there are more commands in the input file.
            Returns true if there are more commands, returns false otherwise. """

        # Peeks next line
        next_line = self.peek_line()

        # While the next line is a comment  or is a new line ignore it.
        while next_line.strip()[0:2] == "//" or next_line == "\n":
            # Reads line to ignore comment or empty line.
            self.file.readline()
            next_line = self.peek_line()
        # If next line is not empty return true
        if next_line is not "":
            return True
        else:
            return False

    def advance(self):
        """ Reads the next command from the input file and makes it the current command. """
        self.current_command = self.file.readline().strip()

    def command_type(self):
        """ Returns the type of the current VM command (C_ARITHMETIC, C_PUSH, C_POP). """

        current_command = self.current_command

        # Checks if there is a comment after the command and returns its index.
        # Returns -1 if // is not found.
        comment_index = current_command.find("//")
        # If there is a comment ignores it and removes it from the current command.
        if comment_index != -1:
            current_command = current_command[0:comment_index].strip()
            self.current_command = current_command
        
        # Splits the currents command
        arguments = current_command.split(" ")
        # if the first component of the current command is in the list of arithmetic commands it is type is arithmetic.
        if arguments[0] in Parser.arithmetic_commads:
            return "C_ARITHMETIC"
        # if the command starts with push it is type C_PUSH
        elif arguments[0] == "push":
            return "C_PUSH"
        # if the command starts with pop it is type C_POP
        elif arguments[0] == "pop":
            return "C_POP"
        else:
            print("ERROR: The command " + current_command + " is not valid")
            exit(1)

    def peek_line(self):
        """ Returns the content of the next line keeping the current position. """
        
        # Stores current file pointer.
        current_position = self.file.tell()
        # Reads next line and stores it.
        line_peeked = self.file.readline()
        # Gets back to the previous file pointer.
        self.file.seek(current_position)
        return line_peeked

    def arg1(self):
        """ Returns the first argument of the current command. """

        # Get the current command
        current_command = self.current_command
        # Splits the command into arguments
        arguments = current_command.split(" ")
        # Gets the type of the current command
        command_type = self.command_type()
        # If the command is type C_PUSH or C_POP returns the first argument 
        if command_type == "C_PUSH" or command_type == "C_POP": 
            try:
                # Checks if the argument is valid for this command
                if arguments[1] in Parser.segments:
                    return arguments[1]
                else:
                    print("ERROR: {} is an invalid argument".format(arguments[1]))
                    exit(1)
            # Checks if there are no arguments to be returned
            except IndexError:
                print("ERROR: missing argument in command " + current_command)
                exit(1)
        # If the command is C_ARITHMETIC returns the operation
        elif command_type == "C_ARITHMETIC":
            return arguments[0]

    def arg2(self):
        """ Returns the second argument of the current command """

        # Get the current command
        current_command = self.current_command
        # Splits the command into arguments
        arguments = current_command.split(" ")
        try:
            # Checks if the second argument is a number and returns it
            if arguments[2].isnumeric():
                return int(arguments[2])
            else:
                print("ERROR: {} is an invalid argument".format(arguments[2]))
        # Checks if there are no arguments to be returned
        except IndexError:
            print("ERROR: missing argument in command " + current_command)