""" Module containing Listener class which inherit from the JackListener class generated  by Antlr """

from JackListener import JackListener
from JackParser import JackParser

class Listener(JackListener):

    keyword = ["class","constructor","function","method","field","static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
    symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
    non_terminals = ['class', 'classVarDec', 'subroutineDec', 'parameterList', 'subroutineBody', 'varDec', 'statements', 'whileStatement', 'ifStatement', 'returnStatement', 'letStatement', 'doStatement', 'expression', 'term', 'expressionList']

    def __init__(self, parser, output_file):
        """ Set the parser and the output file. Count the ident for each line """
        self.parser = parser
        self.output_file = open(output_file, 'w')
        self.ident = "   "
        self.num_ident = 0

    def __del__(self):
        """ Closes the output file """
        self.output_file.close()

    def enterEveryRule(self, ctx):
        """ Enter each rule and write the open tag if the rule name is in the non-terminals list """
        open_tag = "{}<{}>\n".format(self.get_current_ident(), self.parser.ruleNames[ctx.getRuleIndex()][:-2])  # Remove the last 2 letters from the rule name (NT)
        if self.parser.ruleNames[ctx.getRuleIndex()][:-2] in Listener.non_terminals:
            self.output_file.write(open_tag)
            self.increase_ident()
        return super().enterEveryRule(ctx)

    def exitEveryRule(self, ctx):
        """ Exit each rule and write the closing tag if the rule name is in the non-terminals list """
        close_tag = "{}</{}>\n".format(self.get_current_ident(), self.parser.ruleNames[ctx.getRuleIndex()][:-2])  # Remove the last 2 letters from the rule name (NT)
        if self.parser.ruleNames[ctx.getRuleIndex()][:-2] in Listener.non_terminals:
            self.decrease_ident()
            self.output_file.write(close_tag)
        return super().exitEveryRule(ctx)

    def visitTerminal(self, node):
        """ Get the value for each terminal and check if it is a keyword, symbol, interge constant, string constant or identifier """
        
        terminal_value = node.getText()

        if terminal_value in Listener.keyword:
            terminal = "keyword"
        elif terminal_value in Listener.symbol:
            terminal = "symbol"
            # If the symbol is '<', '>', '"' or '&' change its value so that the xml file doesn't have syntax errors
            if terminal_value == '<':
                terminal_value = "&lt;"
            elif terminal_value == '>':
                terminal_value = "&gt;"
            elif terminal_value == '"':
                terminal_value = "&quot;"
            elif terminal_value == '&':
                terminal_value = "&amp;"
        elif terminal_value.isdigit():
            terminal = "integerConstant"
        elif '"' in terminal_value:
            terminal = "stringConstant"
            terminal_value = terminal_value.strip('"')  # Remove the quotes from the string
        else:
            terminal  = "identifier"

        # Write the tag on the output file depending on the terminal value and its class
        self.output_file.write("{}<{}> {} </{}>\n".format(self.get_current_ident(), terminal, terminal_value, terminal))
        return super().visitTerminal(node)

    def get_current_ident(self):
        """ Get the ident for the current line in the xml file """
        return self.num_ident * self.ident

    def increase_ident(self):
        """ Increase the ident in the xml file """
        self.num_ident += 1

    def decrease_ident(self):
        """ Decrease the ident in the xml file """
        self.num_ident -= 1