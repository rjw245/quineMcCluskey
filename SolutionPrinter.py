__author__ = 'Riley'

import string
import math

def printSolution(function,closeCover,format="SOP"):
    """
    Used to finally print the function and its minimal close cover
    in the form F = ABC + A'BC + AB'
    :param function: The function to print
    :param closeCover: The close cover solution for the function
    :param format: SOP => Print sum of products (default). POS => Print product of sums
    :return:
    """

    numInputs = function.numInputs()
    alphabet = list(string.ascii_uppercase)

    if(numInputs>26):
        raise LookupError("Error: Too many inputs (>26) to represent with letters.")

    output=""

    if format=="SOP":
        if 2**numInputs==len(function.minterms.union(function.dontcares)):
            output += "1"
        else:
            for ncubeIdx,ncube in enumerate(closeCover):
                #print [str(m) for m in ncube.getDontCareLocs()]
                for input in reversed(range(0,numInputs)): #Count down so we can print A (MSB) first
                    if input not in ncube.getDontCareLocs(): #We want to print this input. Now decide whether to complement
                        if (2**input & list(ncube.minterms)[0].num)!=0:
                            output += alphabet[numInputs-input-1]
                        else:
                            output += str(alphabet[numInputs-input-1])+"'"
                if ncubeIdx < len(closeCover)-1: output += " + "
    elif format=="POS":
        if len(function.minterms)==0:
            output += "1"
        else:
            #print [str(ncube) for ncube in closeCover]
            for ncubeIdx,ncube in enumerate(closeCover):
                if ncubeIdx!=0:
                    output += ' '
                firstInputPrinted = False
                #print [str(m) for m in ncube.getDontCareLocs()]
                output += "("
                for inputIdx, input in enumerate(reversed(range(0,numInputs))): #Count down so we can print A (MSB) first
                    if input not in ncube.getDontCareLocs(): #We want to print this input. Now decide whether to complement
                        if firstInputPrinted:
                            output += "+"
                        firstInputPrinted = True
                        if (2**input & list(ncube.minterms)[0].num)!=0:
                            output += str(alphabet[numInputs-input-1])+"'"
                        else:
                            output += alphabet[numInputs-input-1]
                output += ")"
    print output
        #TODO: POS doesn't print correctly yet. Must make sure I invert the minterms.