__author__ = 'Riley'

import math
from Minterm import Minterm

class NCube:
    def __init__(self,minterms=[]):
        if len(minterms) == 0 or ((len(minterms) & (len(minterms) - 1)) != 0):
            raise NCubeException("Error: Number of minterms supplied must be a power of two")
        self.N = int(math.log(len(minterms),2))
        self.minterms = set(minterms)
        if not self.isValid():
            raise NCubeException("Error: NCube is invalid. Nodes are non-neighboring.")
        #Holds the base-two digit place, no order, want uniqueness, thus used sets
        self.dontCareLocs = self.populateDontCareLocs()

    @classmethod
    def fromNCubes(cls, ncube1, ncube2):
        """
        Alternative constructor which combines two other NCubes of the same dimension
        :param ncube1: 1st NCube
        :param ncube2: 2nd NCube
        """
        if ncube1.N != ncube2.N:
            raise ValueError("Error: NCubes must be of same dimension")
        return cls(ncube1.minterms.union(ncube2.minterms))

    def populateDontCareLocs(self):
        newDontCareLocs = set()
        for m in self.minterms:
            diff = (list(self.minterms)[0].num ^ m.num)
            if diff>0: newDontCareLocs.add(diff.bit_length()-1)
        return newDontCareLocs

    def covers(self,minterm):
        """
        Used to check if this NCube covers a particular minterm
        :param minterm: The minterm to check
        :return: True if minterm input covered by this NCube
        """
        return (minterm in self.minterms)


    def isValid(self):
        """
        Used to check if this N-Cube is allowed to be formed
        The idea is that the maximum hamming distance between the minterms in an n-cube should equal the dimension
        of the cube
        :return: True if minterms form a cube of some dimension, false otherwise
        """
        maxHammingDistance = max([m.hammingDistance(list(self.minterms)[0]) for m in self.minterms])

        return (maxHammingDistance == self.N)

    def isNeighbor(self,otherNCube):
        """
        Returns true if this NCube can be combined with otherNCube to form a larger NCube
        First check that they share the same don't care locations
        Second, check that max hamming distance of combined cube is equal to its dimension
        :param otherNCube:
        :return:
        """
        if self.dontCareLocs != otherNCube.dontCareLocs:
            return False

        combinedMinterms = self.minterms.union(otherNCube.minterms)
        maxHammingDistance = min(combinedMinterms).hammingDistance(max(combinedMinterms))
        if maxHammingDistance!=self.N+1:
            return False

        return True

    def getDontCareLocs(self):
        return self.dontCareLocs

    def __str__(self):
        sortedMinterms = sorted(list(self.minterms), key=lambda x: x.num, reverse=False)
        if len(self.dontCareLocs)>0:
            return ", ".join(str(m) for m in sortedMinterms)+" ("+", ".join(str(2**dcLoc) for dcLoc in self.dontCareLocs)+")"
        else: return ", ".join(str(m) for m in sortedMinterms) #Don't print don't care locs if single minterm


    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return (self.minterms == other.minterms)

    def __contains__(self, item):
        return (item in self.minterms)

    def __add__(self, other):
        return other + self.N

    def __radd__(self, other):
        return other + self.N

class NCubeException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)