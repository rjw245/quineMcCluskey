__author__ = 'Riley'

from Minterm import Minterm
import string

class Function:
    def __init__(self,minterms=[],dontcares=[]):
        self.minterms = set(minterms)
        self.dontcares = set(dontcares)
        self.numInputsOverride = None

    def numInputs(self):
        if self.numInputsOverride is not None:
            return self.numInputsOverride
        else:
            try:
                x = max(self.minterms.union(self.dontcares)).num.bit_length()
            except ValueError:
                return 0 #If no minterms in function, avoid error
            if x<1: x = 1 #If only minterm is zero, bit length is 0, but numInputs cannot be less than 1
            return x

    def overrideNumInputs(self,n):
        self.numInputsOverride=n

    def flipMinterms(self):
        """
        Returns a new function where the minterms are inverted.
        This is basically converting the function to maxterms
        """
        newMinterms = set([Minterm(i) for i in range(0,2**self.numInputs()) if i not in [m.num for m in self.minterms.union(self.dontcares)]])
        return Function(list(newMinterms),list(self.dontcares))


    def __contains__(self, item):
        if item.isDontCare():
            return (item in self.dontcares)
        else:
            return (item in self.minterms)

    def __str__(self):
        sortedMinterms = sorted(list(self.minterms), key=lambda x: x.num, reverse=False)
        sortedDontCares = sorted(list(self.dontcares), key=lambda x: x.num, reverse=False)
        numInputs = self.numInputs()
        inputStr = ""
        alphabet = list(string.ascii_uppercase)
        for i in range(0,numInputs):
            if i!=0:
                inputStr+=","
            inputStr += alphabet[i]
        return "F("+inputStr+") = m("+",".join(str(m) for m in sortedMinterms)+") + d("+",".join(str(dc) for dc in sortedDontCares)+")"