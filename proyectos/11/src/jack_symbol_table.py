""" Module containing the symbol table for the Jack compiler """

class JackSymbolTable:
    """ The symbol table associates names with information needed for Jack compilation: 
        type, kind, and running index. 
        The symbol table has 2 nested scopes (class/subroutine). """
    
    def __init__(self):
        """ Creates a new empty symbol table 
            The structure for the symbol table is two dictionaries, one for the class scope and one for the method scope.
            Each dictionary is a dictionary of lists, where the name of the class or method is the key and 
            the values for type, kind and # are in the list """

        self.symbol_table = {
                                'class': {},
                                'subroutine': {}
                            }
        
        self.count_static = 0
        self.count_field = 0
        self.count_arg = 0
        self.count_var = 0
        

    def start_subroutine(self):
        """ Starts a new subroutine scope --> Erases all names in the previous subroutine’s scope. """
        self.symbol_table['subroutine'] = {}
        self.count_arg = 0
        self.count_var = 0


    def define(self, name, symbol_type, kind):
        """ Defines a new identifier of a given name, type, and kind and assigns it a running index. 
            STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope. """
        
        if kind == "STATIC":
            self.symbol_table['class'][name] = [symbol_type, kind, self.count_static]
            self.count_static += 1
        elif kind == "FIELD":
            self.symbol_table['class'][name] = [symbol_type, kind, self.count_field]
            self.count_field += 1
        elif kind == "ARG":
            self.symbol_table['subroutine'][name] = [symbol_type, kind, self.count_arg]
            self.count_arg += 1
        elif kind == "VAR":
            self.symbol_table['subroutine'][name] = [symbol_type, kind, self.count_var]
            self.count_var += 1

    def var_count(self, kind):
        """ Returns the number of variables of the given kind already defined in the current scope. """

        if kind == "STATIC":
            return self.count_static
        elif kind == "FIELD":
            return self.count_field
        elif kind == "ARG":
            return self.count_arg
        elif kind == "VAR":
            return self.count_var

    def kind_of(self, name):
        """ Returns the kind of the named identifier in the current scope. 
            Returns NONE if the identifier is unknown in the current scope. """
        
        if name in self.symbol_table['subroutine']:
            return self.symbol_table['subroutine'][name][1]
        elif name in self.symbol_table['class']:
            return self.symbol_table['class'][name][1]
        else:
            return None
        
    def type_of(self, name):
        """ Returns the type of the named identifier in the current scope. """

        if name in self.symbol_table['subroutine']:
            return self.symbol_table['subroutine'][name][0]
        elif name in self.symbol_table['class']:
            return self.symbol_table['class'][name][0]
        else:
            return None

    def index_of(self, name):
        """ Returns the index assigned to named identifier. """

        if name in self.symbol_table['subroutine']:
            return self.symbol_table['subroutine'][name][2]
        elif name in self.symbol_table['class']:
            return self.symbol_table['class'][name][2]
        else:
            return None       