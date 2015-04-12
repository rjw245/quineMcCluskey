__author__ = 'Riley'

import re
from Function import Function
from Minterm import Minterm

class InputParser:
    funcRegex = r"m\((?P<m>(\d+,\s*)*\s*\d+)\)(\s*\+\s*d\((?P<dc>(\d+,\s*)*\s*\d+)\))*"
    func_pattern = re.compile(funcRegex,re.VERBOSE)

    def __init__(self):
        pass

    @staticmethod
    def extractFunctions(filePath=None):
        """

        :param filePath: Path to the input file, if loading input from a file
        :return: A list of the function strings.
        """
        functions = []

        #If no file supplied, get functions from the user via the command line
        if filePath is None:
            func = ""
            print "Enter functions one by one. Enter 'done' when all have been entered."


            while True:
                func = raw_input("Enter your function in the form m(1,2,3) + d(4,5,6): ")
                if func == "done": break

                if not InputParser.func_pattern.match(func):
                    print "Invalid function, try again"
                    continue
                else:
                    functions.append(func)

        else:
            inputFile = open(filePath)
            for i,line in enumerate(inputFile):
                if not InputParser.func_pattern.match(line):
                    print "Invalid function on line", i+1
                else:
                    functions.append(line.strip())

        return functions

    @staticmethod
    def getMintermsAndDCs(functions):
        """

        :param functions: A list of strings in the format "m(1,2,3) + d(4,5,6)". Generally gotten from extractFunctions.
        :return: Returns a list of Function objects
        """
        parsed = []
        for fStr in functions:
            mString = InputParser.func_pattern.match(fStr).group("m")
            dcString = InputParser.func_pattern.match(fStr).group("dc")
            mList = [m.strip() for m in mString.split(",")]
            if dcString is not None:
                dcList = [dc.strip() for dc in dcString.split(",")]
            else:
                dcList = []

            if not (all([m.isdigit() for m in mList]) and all([dc.isdigit() for dc in dcList])):
                print "At least one invalid minterm entered. Check that all are comma-separated integers."
                continue

            mList = [Minterm(int(m)) for m in mList]
            dcList = [Minterm(int(dc)) for dc in dcList]

            f = Function(mList,dcList)

            parsed.append(f)

        return parsed