"""
Contains the Parser class for the assembler
"""

class Parser:
    """ Class that reads an assembly language command, parses it and provides access to the command's components (fields and symbols).
    It also removes white space and comments. """

    def __init__(self, input_file):
        """ Recives the input file and opens it to get ready to parse it. 
            Initializes the current command in None. """
        self.file = open(input_file, "r")
        self.current_command = None

    def __del__(self):
        self.file.close()
    
    def has_more_commands(self):
        """ Returns true if there are more commands, returns false otherwise.
            It also returns the next command to be parsed. """
    
        # Peeks next line.
        next_line = self.peek_line()
        
        # While the next line is a comment  or is a new line ignore it.
        while next_line.strip()[0:2] == "//" or next_line == "\n":
            # Reads line to ignore comment.
            self.file.readline()
            next_line = self.peek_line()
        # If next line is not empty return true
        if next_line is not "":
            return True
        else:
            return False

    def advance(self):
        """ Reads the next command from the file and makes it the current command. """
        self.current_command = self.file.readline().strip()

    def command_type(self):
        """ Returns the type of the current command (A_COMMAND, C_COMMAND, L_COMMAND). """

        current_command = self.current_command

        # Checks of there is a comment after the command and returns it's index.
        comment_index = current_command.find("//")
        # If there is a comment ignores it and removes it from the actual command.
        if comment_index != -1:
            current_command = current_command[0:comment_index].strip()
            self.current_command = current_command.strip()

        # If the current command starts with a '@' it is type A.
        if current_command[0] == "@" and current_command[1:] != "":
            return "A_COMMAND"
        # If the current command contains a '=' or ';' it is type C.
        elif "=" in current_command or ";" in current_command:
            return "C_COMMAND"
        # If the current command starts with a '(' and ends with a ')' it is type L.
        elif current_command[0] == "(" and current_command[-1] == ")" and self.current_command[1:-1].strip() != "":
            return "L_COMMAND"
        else:
            print("ERROR: The command " + current_command + " is not valid")
            exit(1)

    def symbol(self):
        """ Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx). """
        current_command = self.current_command
        if current_command[0] == "@":
            return self.current_command[1:]
        elif current_command[0] == "(" and current_command[-1] == ")":
            return self.current_command[1:-1]
    
    def dest(self):
        """ Returns the dest mnemonic from the current command. """
        current_command = self.current_command
        if "=" in current_command:
            index = current_command.find("=")
            return current_command[0:index]
        else:
            return None

    def comp(self):
        """ Returns the comp mnemonic from the current command. """
        current_command = self.current_command
        # If the current command has dest and jump ignores them and only returns comp.
        if "=" in current_command and ";" in current_command:
            equal_index = current_command.find("=")
            colon_index = current_command.find(";")
            return current_command[equal_index + 1 : colon_index]
        # If the current command only has dest returns comp and ignores dest.
        elif "=" in current_command:
            equal_index = current_command.find("=")
            return current_command[equal_index + 1:]
        # If the current command only has jump returns comp and ignores jump.
        elif ";" in current_command:
            colon_index = current_command.find(";")
            return current_command[0:colon_index]

    def jump(self):
        """ Returns the jump mnemonic from the current command. """
        current_command = self.current_command
        colon_index = current_command.find(";")
        if colon_index != -1:
            return current_command[colon_index + 1:]
        else:
            return None

    def peek_line(self):
        """ Returns content of the next line keeping the current position. """
        # Stores current file pointer.
        current_position = self.file.tell()
        # Reads next line and stores it.
        line_peeked = self.file.readline()
        # Gets back to the previous file pointer.
        self.file.seek(current_position)
        return line_peeked