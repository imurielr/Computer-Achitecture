from antlr4.error.ErrorListener import ErrorListener

class CatchError(ErrorListener):

    def __init__(self):
        super(CatchError, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError('SYNTAX ERROR: {} at line {}, column {}'.format(msg, line, column))
        return super().syntaxError(recognizer, offendingSymbol, line, column, msg, e)