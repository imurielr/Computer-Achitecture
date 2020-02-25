""" 
Contains class that manages the symbol table
"""

class SymbolTable:
    """ Keeps a correspondance between symbolic labels and numeric addresses """

    def __init__(self):
        """ Initializes the symbol table with the predefined symbols """
        self.symbol_table = { 
                            "SP" : 0,
                            "LCL" : 1,
                            "ARG" : 2,
                            "THIS" : 3,
                            "THAT" : 4,
                            "R0" : 0,
                            "R1" : 1,
                            "R2" : 2,
                            "R3" : 3,
                            "R4" : 4,
                            "R5" : 5,
                            "R6" : 6,
                            "R7" : 7,
                            "R8" : 8,
                            "R9" : 9,
                            "R10" : 10,
                            "R11" : 11,
                            "R12" : 12,
                            "R13" : 13,
                            "R14" : 14,
                            "R15" : 15,
                            "SCREEN" : 16384,
                            "KBD" : 24576
                            }
        
    def add_entry(self, symbol, address):
        """ Adds the pair (symbol, address) to the symbol table """
        self.symbol_table[symbol] = address

    def contains(self, symbol):
        """ Returns true if the table contains the symbol, otherwise return false """
        return symbol in self.symbol_table

    def get_address(self, symbol):
        """ Returns the address associated with the symbol """
        return self.symbol_table[symbol]