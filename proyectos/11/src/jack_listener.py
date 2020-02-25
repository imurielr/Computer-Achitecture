""" Module containing Listener class which inherit from the JackListener class generated  by Antlr """

from JackListener import JackListener
from JackParser import JackParser

class Listener(JackListener):

    keyword = ["class","constructor","function","method","field","static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
    symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def __init__(self, parser, vm_writer, symbol_table):
        """ Set the parser and use the VM writer to write into the output file """
        self.parser = parser
        self.vm_writer = vm_writer
        self.symbol_table = symbol_table
        self.current_class = ''
        self.current_subroutine_name = ''
        self.current_subroutine_local = ''

    def enterClassNT(self, ctx):
        self.current_class = ctx.getChild(1).getText()
        
        return super().enterClassNT(ctx)
    
    def enterClassVarDecNT(self, ctx):
        num_variables = ctx.getChildCount()
        kind = ctx.getChild(0).getText()
        symbol_type = ctx.getChild(1).getText()
        name = ctx.getChild(2).getText()
        self.symbol_table.define(name, symbol_type, kind.upper())

        # If 'num_variables' is greater than 4 means there are more than one variables being declared
        if num_variables > 4:
            for i in range((num_variables - 4) // 2):
                name = ctx.getChild(2+(i*2+2)).getText()
                self.symbol_table.define(name, symbol_type, kind.upper())

        return super().enterClassVarDecNT(ctx)

    def enterSubroutineDecNT(self, ctx):
        self.symbol_table.start_subroutine()

        subroutine_type = ctx.getChild(0).getText()
        self.current_subroutine_name = ctx.getChild(2).getText()

        if subroutine_type == "method":
           # First argument of the method is a referece to the object 
            self.symbol_table.define("this", subroutine_type, "ARG")

        if ctx.getChild(4) == '':
            self.parameterList(ctx.getChild(4))  # Child 4 represents the parameter list

        self.subroutineBody(ctx.getChild(6))  # Child 6 represents the subroutine body

        return super().enterSubroutineDecNT(ctx)

    def parameterList(self, ctx):
        num_variables = ctx.getChildCount()

        var_type = ctx.getChild(0).getText()
        var_name = ctx.getChild(1).getText()
        self.symbol_table.define(var_name, var_type, 'ARG')

        if num_variables > 2:
            for i in range((num_variables - 2) // 3):
                var_type = ctx.getChild(0+(i*3+3)).getText()
                var_name = ctx.getChild(1+(i*3+3)).getText()
                self.symbol_table.define(var_name, var_type, 'ARG')

    def subroutineBody(self, ctx):
        num_locals = 0
        while ctx.getChild(num_locals+1).getText()[0:3] == 'var':
            self.varDec(ctx.getChild(num_locals+1))
            num_locals += 1
        
        # Write function in vm output file
        function_name = "{}.{}".format(self.current_class, self.current_subroutine_name)
        self.vm_writer.write_function(function_name, num_locals)

    
    def varDec(self, ctx):
        pass
        
    

    # def enterEveryRule(self, ctx):
    #     """ Enter each rule and write the open tag if the rule name is in the non-terminals list """
    #     open_tag = "{}<{}>\n".format(self.get_current_ident(), self.parser.ruleNames[ctx.getRuleIndex()][:-2])  # Remove the last 2 letters from the rule name (NT)
    #     if self.parser.ruleNames[ctx.getRuleIndex()][:-2] in Listener.non_terminals:
    #         self.output_file.write(open_tag)
    #         self.increase_ident()
    #     return super().enterEveryRule(ctx)

    # def exitEveryRule(self, ctx):
    #     """ Exit each rule and write the closing tag if the rule name is in the non-terminals list """
    #     close_tag = "{}</{}>\n".format(self.get_current_ident(), self.parser.ruleNames[ctx.getRuleIndex()][:-2])  # Remove the last 2 letters from the rule name (NT)
    #     if self.parser.ruleNames[ctx.getRuleIndex()][:-2] in Listener.non_terminals:
    #         self.decrease_ident()
    #         self.output_file.write(close_tag)
    #     return super().exitEveryRule(ctx)

    # def visitTerminal(self, node):
    #     """ Get the value for each terminal and check if it is a keyword, symbol, interge constant, string constant or identifier """
        
    #     terminal_value = node.getText()

    #     if terminal_value in Listener.keyword:
    #         terminal = "keyword"
    #     elif terminal_value in Listener.symbol:
    #         terminal = "symbol"
    #         # If the symbol is '<', '>', '"' or '&' change its value so that the xml file doesn't have syntax errors
    #         if terminal_value == '<':
    #             terminal_value = "&lt;"
    #         elif terminal_value == '>':
    #             terminal_value = "&gt;"
    #         elif terminal_value == '"':
    #             terminal_value = "&quot;"
    #         elif terminal_value == '&':
    #             terminal_value = "&amp;"
    #     elif terminal_value.isdigit():
    #         terminal = "integerConstant"
    #     elif '"' in terminal_value:
    #         terminal = "stringConstant"
    #         terminal_value = terminal_value.strip('"')  # Remove the quotes from the string
    #     else:
    #         terminal  = "identifier"

    #     # Write the tag on the output file depending on the terminal value and its class
    #     self.output_file.write("{}<{}> {} </{}>\n".format(self.get_current_ident(), terminal, terminal_value, terminal))
    #     return super().visitTerminal(node)