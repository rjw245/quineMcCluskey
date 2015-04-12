__author__ = 'Riley'

from NCube import NCube
import itertools
import myitertools
import operator

def solve(function):
    """
    This function runs through all steps of the Quine-McCluskey method for reducing single-output boolean algebra
    functions. Finds the prime implicants, determines which are essential, and then runs Petrick's method if needed.
    :param function: The function to be simplified. Of type Function.
    :return: A set of NCubes representing the minimal close cover POS of the function
    """
    PIs = findPIs(function)
    closeCover = findMinimalCloseCover(function,PIs)
    return closeCover

def findMinimalCloseCover(function,PIs):
    """
    Call once the PIFinder has been initialized with a boolean algebra function.
    This processes the function to come up with the minimal close cover for the function
    :return: A set of NCubes representing the minimal close cover product of sums for the function
    """

    essential_PIs = findEssentialPIs(function,PIs)

    #Now check if essential PIs cover everything. If not, do Petrick's method
    uncoveredMinterms = set()
    for m in function.minterms:
        numAppearances=0
        for PI in essential_PIs:
            if PI.covers(m):
                numAppearances+=1
        if numAppearances==0:       #Means a minterm was not covered and thus we need to do Petrick's method
            uncoveredMinterms.add(m)
    #print "Uncovered by essentials",[str(m) for m in uncoveredMinterms]
    if len(uncoveredMinterms)!=0:
        #Eliminate dominated PIs
        undominatedPIs = PIs.copy()
        for PI in PIs:
            if list(PIs)[0] != PI and (list(PIs)[0].minterms.issubset(PI.minterms) or PI.minterms.issubset(list(PIs)[0].minterms)):
                undominatedPIs.remove(PI)
        PIs = undominatedPIs
        #print "Must do Petrick's Method"
        #print [str(n) for n in uncoveredMinterms]
        petricksNCubes = petricksMethod(function,uncoveredMinterms, PIs.difference(essential_PIs))
        return essential_PIs.union(petricksNCubes)
    else:
        return essential_PIs

def findPIs(function):
    """
    Finds the prime implicants for the current boolean algebra function
    :return: A set of NCubes representing the prime implicants of the function
    """

    allterms = function.minterms.union(function.dontcares)
    allterms_sorted = list(allterms)
    allterms_sorted.sort(key = lambda x: x.numOnes())
    allterms_buckets_sorted = []
    for k, g in itertools.groupby(allterms_sorted,key = lambda x: x.numOnes()):
        allterms_buckets_sorted.append(list(g))
    #for group in allterms_buckets_sorted:
        #print [str(m) for m in group]
    #print
    covered = set()

    #Group cubes first by their dimension and then by the number of ones they have.
    #Of course, really only zero-cubes (minterms) can be grouped by their number of ones
    #But then those groupings will carry forward and make it so only certain higher-order cubes are adjacent
    cubes_by_numOnes = {}
    cubeN = 0 #Dimension of the cubes currently being created and stored. Incremented later
    while True:
        cubes_by_numOnes[cubeN] = [] #Create groups of cubes of the same dimension
        newCubesCreated = False
        if cubeN==0: #Special case, dealing with minterms, this is where we group by number of ones
            #Store minterms appropriately
            lastNumOnes = -1
            for idx,group in enumerate(allterms_buckets_sorted):
                groupset = set()
                for m in group:
                    zerocube = NCube([m])
                    groupset.add(zerocube)
                cubes_by_numOnes[cubeN].append(groupset)

                newCubesCreated=True
        else: #Dealing with higher-dimension cubes (1-cubes or greater)
            for groupIdx,group in enumerate(cubes_by_numOnes[cubeN-1]):
                if groupIdx<len(cubes_by_numOnes[cubeN-1])-1: #Don't do last group
                    newCubeSet = set()
                    for cube in group:
                        can_combine = [cube2 for cube2 in cubes_by_numOnes[cubeN-1][groupIdx+1] if cube.isNeighbor(cube2)]
                        for cube2 in can_combine:
                            newCubeSet.add(NCube.fromNCubes(cube,cube2))
                            covered.add(cube)
                            covered.add(cube2)
                            newCubesCreated=True
                    cubes_by_numOnes[cubeN].append(newCubeSet)

        cubeN+=1
        if not newCubesCreated:
            break

    #print cubes_by_numOnes

    # #One-cubes are created from minterms, cannot be combined into the following loop easily
    # onecubes = set()
    # for m in allterms:
    #     #Can only combine minterms into an NCube if they differ by exactly one bit
    #     neighboring = [m2 for m2 in allterms if m2.hammingDistance(m)==1]
    #     for m2 in neighboring:
    #         onecube = NCube([m,m2])
    #         covered.add(m)
    #         covered.add(m2)
    #         onecubes.add(onecube)
    #
    # ncubesList = [onecubes]
    #
    # #Combine cubes until no longer possible
    # i=1
    # while True:
    #     ncubes = set() #New set of larger cubes
    #     prevcubes = ncubesList[i-1] #Access the most recently created cubes to try and combine them
    #     for cube in prevcubes:
    #         neighboring = [cube2 for cube2 in prevcubes if cube2.isNeighbor(cube)]
    #         for cube2 in neighboring:
    #             ncube = NCube.fromNCubes(cube,cube2)
    #             covered.add(cube)
    #             covered.add(cube2)
    #             ncubes.add(ncube)
    #     if len(ncubes)==0:
    #         #No larger cubes were created, stop
    #         break
    #     ncubesList.append(ncubes)
    #     i+=1

    #ncubesList now contains the set of one-cubes at index 0, two-cubes at index 1, three cubes at index 2, etc
    PIs = set()
    for dim,ncubegroups in cubes_by_numOnes.iteritems():
        for ncubegroup in ncubegroups:
            for ncube in ncubegroup:
                if ncube not in covered:
                    PIs.add(ncube)
    #print "PIs",[str(n) for n in PIs]
    return PIs

def findEssentialPIs(function,PIs):
    """
    Given the function and prime implicants of that function, find and hand back which PIs are essential.
    Essential PIs are PIs that cover at least one minterm that no other PI covers.
    :param function: The function these prime implicants belong to
    :param PIs: The set of prime implicants (NCubes)
    :return: The set of essential prime implicants (which are NCube objects)
    """
    essential_PIs = set()
    minterms = function.minterms.copy()
    PIs = PIs.copy()

    #Find essentials, remove them, find more essentials, remove those... loop until no more essentials can be pulled out
    while True:
        #We no longer care about covering don't-cares, so don't check the PIs for them
        newEssentials = set()
        for m in minterms:
            #print "Check",m
            numAppearances = 0
            potentialEssential = None  # Used to keep track of PI in case it is the only one to cover a minterm => essential
            for PI in PIs:
                if PI.covers(m):
                    #print str(PI),"covers",str(m)
                    numAppearances+=1
                    potentialEssential = PI
            if numAppearances==1:
                newEssentials.add(potentialEssential)

        for e in newEssentials:
            essential_PIs.add(e)

        if len(newEssentials) == 0:
            break

        #Remove essentials
        for e in newEssentials:
            if e in PIs:
                PIs.remove(e)

        #Remove minterms covered by essentials:
        for e in newEssentials:
            for m in e.minterms:
                if m in minterms:
                    #print "Removing",str(m)
                    minterms.remove(m)

    #print "Essential",[str(m) for m in essential_PIs]

    return essential_PIs

def petricksMethod(function,uncoveredMinterms,PIs):
    # Instead, I should do a reduced PI table several times, eliminating the essentials from the previous round each time.
    # If no more essentials can be picked out, only then should I do Petrick's method.

    """
    Returns a set of PI ncubes which minimally cover the uncoveredMinterms input, intended to be ORed
    with the essential PIs

    Function finds a set of minterms that cover each minterm. It then picks one from each grouping,
    eliminating duplicates, choosing the set that is the smallest while still covering all minterms.

    Uses itertools.product to pick a PI from each grouping and get all possible combinations.

    :param uncoveredMinterms: The set of minterms that remain uncovered (Minterm objects)
    :param PIs: The prime implicants of the function (NCubes)
    :return: Set of NCubes representing PIs which cover minterms the essential PIs miss
    """
    #print "Using Petrick's method"
    numInputs = function.numInputs()

    #Sort PIs by minterm
    PIs_by_minterm = [set([PI for PI in PIs if m in PI]) for m in uncoveredMinterms]
    #Look at all possible sets of PIs when choosing one that covers each minterm
    possibleCombos = set([frozenset(combo) for combo in itertools.product(*PIs_by_minterm)])
    #To find least costly, we find the grouping with minimal cost. Cost of single PI = (NUM_INPUTS - PI_DIMENSION)
    #Cost of a grouping is determined by summing all of the PIs' costs
    bestCombo = min(list(possibleCombos),key=lambda s: numInputs*len(s)-sum(s))  # Lambda function calculates PI cost
    return bestCombo




