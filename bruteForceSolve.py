import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint
from more_itertools import powerset

infinity = 1000

    
def canonicalize(weights, edges):
    vertices = sorted(weights)
    mapping = {v: i for i, v in enumerate(vertices)}
    inv_mapping = {v : k for (k, v) in mapping.items()}
    
    canonical_edges = [
        [mapping[u] for u in edge]
        for edge in edges
    ]
    canonical_weights = [weights[v] for v in vertices]

    return canonical_weights, canonical_edges, mapping, inv_mapping

def findMinVCCost(weights, edges):
    A = []
    for e in edges:
        line = [0]*len(weights)
        line[e[0]] = 1
        line[e[1]] = 1
        A.append(line)
    A = np.array(A)
    b = np.array([1]*len(edges))
    c = np.array(weights)
    integrality = np.full_like(c, True)
    constraints = LinearConstraint(A, b)

    res = milp(c=c, constraints=constraints, integrality=integrality)

    return res.fun


def findOptimalPrices(weights, edges, selection=None):
    priceableVertices = []
    for i in range(len(weights)):
        if weights[i] == 0:
            priceableVertices.append(i)

    subsets = list(powerset(priceableVertices))
    costs = {}

    for boughtElements in subsets:
        for x in priceableVertices:
            if x in boughtElements:
                continue
            weights[x] = infinity
        costs[boughtElements] = findMinVCCost(weights, edges)
        for x in priceableVertices:
            weights[x] = 0
    bestSelection = ()
    bestPrice = []
    bestRevenue = -100

    if selection is None:
        subsets.remove(())
    else:
        subsets =[selection]
    for boughtElements in subsets:
        A = []
        b = []
        c = [1]*len(boughtElements)

        for subset in powerset(boughtElements):
            line = [0]*len(boughtElements)
            for i, x in enumerate(boughtElements):
                if x not in subset:
                    line[i] = 1
            b.append(costs[subset] - costs[boughtElements])
            A.append(line)
        c = np.array([-1]*len(boughtElements))
        A = np.array(A)
        b = np.array(b)

        res = linprog(c, A, b)

        if -res.fun >= bestRevenue:
            bestSelection = boughtElements
            bestPrice = res.x
            bestRevenue = - res.fun

    return (bestSelection, bestPrice, bestRevenue)

v1 = {
    0 : 0,
    1 : 1,
    2 : 0,
    3 : 1,
    4 : 0,
    5 : 1
}

e1 = [[0,1], [1,2], [2, 3], [3, 4], [4, 5], [5, 0]]

v2 = {
    0 : 0,
    2 : 0,
    4 : 0,
    6 : 2,
    7 : 2,
    8 : 2
}

e2 = [[0, 6], [2, 8], [4, 7], [6, 7], [7, 8], [6, 8]]

weights, edges, _, inv_mapping = canonicalize({**v1, **v2}, e1 + e2)
selection, prizes, revenue = findOptimalPrices(weights, edges)
selection = [inv_mapping[x] for x in selection]
print((selection, prizes, revenue))

weights, edges, mapping, _ = canonicalize(v1, e1)
_, prizes, revenue = findOptimalPrices(weights, edges, tuple([mapping[x] for x in selection]))
print((selection, prizes, revenue))

weights, edges, mapping, _ = canonicalize(v2, e2)
_, prizes, revenue = findOptimalPrices(weights, edges, tuple([mapping[x] for x in selection]))
print((selection, prizes, revenue))