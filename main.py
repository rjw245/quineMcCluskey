__author__ = 'Riley'

# Implementing: https://trunk.tufts.edu/access/content/attachment/d975cd4d-a3cb-4383-9807-0bfc295b7d20/Assignments/3e271133-863e-4468-8436-8f94184262e0/26nt12QMproject.rtf

import QuineMcCluskey
import SolutionPrinter
import sys
from inputParser import InputParser
import time

if __name__ == "__main__":

    #Get and parse input
    try:
        inputPath = sys.argv[1]
    except IndexError:
        inputPath = None
    functions = InputParser.extractFunctions(inputPath)
    parsedFuncs = InputParser.getMintermsAndDCs(functions)

    #Solve each function
    for f in parsedFuncs:
        start_time = time.time()
        fMaxterms = f.flipMinterms() #Kinda hacky, not proud of this solution
        fMaxterms.overrideNumInputs(f.numInputs())
        #print "Calculating SOP"
        solutionSOP = QuineMcCluskey.solve(f)
        #print "Calculating POS"
        solutionPOS = QuineMcCluskey.solve(fMaxterms)
        print f
        print "=",
        SolutionPrinter.printSolution(f,solutionSOP,"SOP")
        print "=",
        SolutionPrinter.printSolution(fMaxterms,solutionPOS,"POS")
        print "Took "+str((time.time()-start_time))+" seconds"
        print "----------------------------------------------------------"