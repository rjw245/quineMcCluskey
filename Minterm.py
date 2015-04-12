__author__ = 'Riley'

class Minterm:
    def __init__(self,num):
        """
        :param num: What number minterm this is
        """
        self.num = num

    def numOnes(self):
        """
        Count the number of ones in the binary representation of this minterm
        :return: Number of ones in binary representation of minterm
        """
        count=0
        x = self.num
        while(x!=0):
            x = x&(x-1)
            count+=1
        return count

    def isNeighbor(self,otherMinterm):
        """
        Returns true if minterms differ by only one bit
        :param otherMinterm: The minterm to compare with self
        :return: True if neighbors, false otherwise
        """
        return (self.hammingDistance(otherMinterm)==1)

    def hammingDistance(self,otherMinterm):
        bitsThatDiffer = self.num ^ otherMinterm.num #Bits that differ are ones
        return Minterm(bitsThatDiffer).numOnes() #Only made a Minterm to use the numOnes function

    def __str__(self):
        return str(self.num)

    def __eq__(self, other):
        return (self.num == other.num)

    def __hash__(self):
        return hash(str(self))

    def __int__(self):
        return self.num

    def __cmp__(self, other):
        return self.num - other.num