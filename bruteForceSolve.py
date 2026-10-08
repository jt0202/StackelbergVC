import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint
from more_itertools import powerset

# Should be higher than the sum of weights of all neighbors
# for any priceable vertex
INFINITY = 1000

# Joins a list of dictionaries with values by summing values associated with the same key
# We don't use Counter because we want to keep zero elements
def joinDicts(l):
    res = {}
    for d in l:
        for k, v in d.items():
            if k in res:
                res[k] += v
            else:
                res[k] = v
    return res

# Transform the graph so that the priceable vertices (which are identified by weight 0)
# occur always at the start. This is assumed for the later algorithms to work.
# Additionally functions to transform the graph into the new format and out of it are provided.
def canonicalize(weights, edges):
    vertices = sorted(weights)
    mapping = {v: i for i, v in enumerate(vertices)}
    inv_mapping = {v : k for (k, v) in mapping.items()}
    
    canonical_edges = [[mapping[u] for u in edge] for edge in edges]
    canonical_weights = [weights[v] for v in vertices]

    return canonical_weights, canonical_edges, mapping, inv_mapping

# Find the minimum weight vertex cover for a general graph with an ILP approach.
def vertex_cover_cost(weights, edges):
    A = np.zeros((len(edges), len(weights)))
    for row,e in enumerate(edges):
        A[row, e[0]] = 1
        A[row, e[1]] = 1
    res = milp(c=np.array(weights), constraints=LinearConstraint(A, 1, np.inf), integrality=np.full_like(weights, True))
    return res.fun

# Creates the large LP to compute the optimal prices. If a specific selection is given, then
# the optimal prices when selling exactly the selection are computed.
def find_optimal_prices(weights, edges, selection=None):
    priceable_vertices = []
    for i in range(len(weights)):
        if weights[i] == 0:
            priceable_vertices.append(i)

    subsets = list(powerset(priceable_vertices))
    costs = {}

    for bought_elements in subsets:
        costs[bought_elements] = vertex_cover_cost(
            [INFINITY if i in priceable_vertices and i not in bought_elements else x for i, x in enumerate(weights)], edges)
    best_selection = ()
    best_price = []
    best_revenue = -100

    if selection is None:
        subsets.remove(())
    else:
        subsets = [selection]
    for bought_elements in subsets:
        A = []
        b = []
        for subset in powerset(bought_elements):
            b.append(costs[subset] - costs[bought_elements])
            A.append([0 if x in subset else 1 for x in bought_elements])
        res = linprog(np.array([-1]*len(bought_elements)), np.array(A), np.array(b))

        if -res.fun >= best_revenue:
            best_selection = bought_elements
            best_price = res.x
            best_revenue = - res.fun

    return (best_selection, best_price, best_revenue)

def solve(weights, edges, selection=None):
    weights, edges, mapping, inverse_mapping = canonicalize(weights, edges)

    if selection is not None:
        selection = tuple(mapping[v] for v in selection)

    selection, prices, revenue = find_optimal_prices(
        weights, edges, selection
    )

    selection = tuple(inverse_mapping[v] for v in selection)

    return selection, prices, revenue
