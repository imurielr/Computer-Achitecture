""" Module containing the class that translates from Jack to Virtual Matchine language """

class JackVMWriter:
    """ This class writes VM commands into a file. It encapsulates the VM command syntax. """

    def __init__(self, output_file):
        """ Creates a new file and prepares it for writing VM commands """
        self.output_file = open(output_file, 'w')

    def __del__(self):
        """ Closes the output file """
        self.output_file.close()

    def write_push(self, segment, index):
        """ Writes a VM push command.
            Segment can be: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER or TEMP """

        segment = segment.lower()

        if segment == "const":
            segment = "constant"

        elif segment == "arg":
            segment = "argument"

        self.output_file.write("push {} {}\n".format(segment, index))

    def write_pop(self, segment, index):
        """ Writes a VM pop command.
            'segment' can be: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER or TEMP """

        segment = segment.lower()

        if segment == "const":
            segment = "constant"

        elif segment == "arg":
            segment = "argument"

        self.output_file.write("pop {} {}\n".format(segment, index))

    def write_arithmetic(self, command):
        """ Writes a VM arithmetic command.
            'command' can be ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT """

        self.output_file.write("{}\n".format(command.lower()))

    def write_label(self, label):
        """ Writes a VM label command """
        self.output_file.write("label {}\n".format(label))

    def write_goto(self, label):
        """ Writes a VM goto command """
        self.output_file.write("goto {}\n".format(label))

    def write_if(self, label):
        """ Writes a VM If-goto command """
        self.output_file.write("if-goto {}\n".format(label))

    def write_call(self, name, n_arg):
        """ Writes a VM call command """
        self.output_file.write("call {} {}\n".format(name, n_arg))

    def write_function(self, name, n_locals):
        """ Writes a VM function command """
        self.output_file.write("function {} {}\n".format(name, n_locals))

    def write_return(self):
        """ Writes a VM return command """
        self.output_file.write("return\n")