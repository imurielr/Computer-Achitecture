""" 
Contains class that translate hack language into binary code
"""

class Code:
    """ 
    Translates the Hack assembly language mnemonics into binary codes
    """

    """ Table with binary codes for each dest mnemonic. """
    dest_table = { 
            None : "000",
            "M" : "001",
            "D" : "010",
            "MD" : "011",
            "A" : "100",
            "AM" : "101",
            "AD" : "110",
            "AMD" : "111"
            }

    """ Table with binary codes for each jump mnemonic. """
    jump_table = {
            None : "000",
            "JGT" : "001",
            "JEQ" : "010",
            "JGE" : "011",
            "JLT" : "100",
            "JNE" : "101",
            "JLE" : "110",
            "JMP" : "111"
            }

    """ Table with binary codes for each comp mnemonic, it adds the 'a' mnemonic """
    comp_table = {
                "0" : "0101010",
                "1" : "0111111",
                "-1" : "0111010",
                "D" : "0001100",
                "A" : "0110000",
                "!D" : "0001101",
                "!A" : "0110001",
                "-D" : "0001111",
                "-A" : "0110011",
                "D+1" : "0011111",
                "A+1" : "0110111",
                "D-1" : "0001110",
                "A-1" : "0110010",
                "D+A" : "0000010",
                "D-A" : "0010011",
                "A-D" : "0000111",
                "D&A" : "0000000",
                "D|A" : "0010101",
                "M" : "1110000",
                "!M" : "1110001",
                "-M" : "1110011",
                "M+1" : "1110111",
                "M-1" : "1110010",
                "D+M" : "1000010",
                "D-M" : "1010011",
                "M-D" : "1000111",
                "D&M" : "1000000",
                "D|M" : "1010101"
                }

    def dest(self, dest_mnemonic):
        """ Returns the binary code of the dest mnemonic """

        # Checks if the dest table contains the mnemonic, if it does returns its binary code, otherwise the program stops
        if dest_mnemonic in Code.dest_table:
            return Code.dest_table[dest_mnemonic]
        else:
            print("ERROR: The dest mnemonic " + dest_mnemonic + " is not valid")
            exit(1)   

    def comp(self, comp_mnemonic):
        """ Returns the binary code of the comp mnemonic """

        # Checks if the comp table contains the mnemonic, if it does returns its binary code, otherwise the program stops
        if comp_mnemonic in Code.comp_table:
            return Code.comp_table[comp_mnemonic]
        else:
            print("ERROR: The comp mnemonic " + comp_mnemonic + " is not valid")
            exit(1)

    def jump(self, jump_mnemonic):
        """ Returns the binary code of the jump mnemonic """

        # Checks if the jump table contains the mnemonic, if it does returns its binary code otherwise the program stops
        if jump_mnemonic in Code.jump_table:
            return Code.jump_table[jump_mnemonic]
        else:
            print("ERROR: The jump mnemonic " + jump_mnemonic + " is not valid")
            exit(1)

    