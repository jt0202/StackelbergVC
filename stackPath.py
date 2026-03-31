def selectAll(path):
    indices = []

    for i in range(0, len(path)):
        if path[i] < 0:
            indices.append(i)
            path[i] = 0

    # Cost[i] : Cost of minimum vertex cover up to position i
    # constCost[i] : Cost without the price of the current active vertex
    # rev [i] : Revenue without the current active vertex.
    cost, constCost, rev = dict(), dict(), dict()

    # No cost or revenue to obtain on an empty graph.
    cost[0] = 0
    constCost [0] = 0
    rev[0] = 0

    # Similarly for a leaf.
    cost[1] = 0
    constCost [1] = 0
    rev[1] = 0

    if 0 in indices:
        activeVertex = 0
    else:
        activeVertex = None

    for i in range(1, len(path)):
        # We have not reached the first priceable vertex
        # and only compute the minimum vertex cover cost for
        # each subpath
        if activeVertex is None and i not in indices:
            cost[i+1] = min(path[i] + cost[i], path[i-1] + cost[i-1])
            constCost[i+1] = cost[i+1]
            rev[i+1] = 0
        elif i in indices:
            # We have to close the previous vertex.
            activeVertex = i
            # Cost when choosing i and minimum Vertex cover of before
            cost1 = cost[i]

            #Cost when choosing i and i-1 and minimum Vertex cover of before
            #Here the priceable vertex has a price of zero
            cost2 = path[i-1] + cost[i-1]

            minCost = min(cost1, cost2)
            constCost[i+1] = minCost
            # We assign as a price for the current active vertex the difference between both costs
            cost[i+1] = max(cost1, cost2)

            rev[i+1] = 0
        elif i-1 in indices:
            # We again have to close the previous vertex.
            pass
        else:
            pass

    for i in range(0, len(path) + 1):
        if i < len(path):
            print(f"Vertex: {i} with weight {path[i]}")
        else:
            print("Complete path")
        print(cost[i])
        print(constCost[i])
        print(rev[i])
        print(" --- ")


def solve(path):
    priceableIndices = []

    for i in range(0, len(path)):
        if path[i] < 0:
            priceableIndices.append(i)

    selectAll(path)

# We encode priceable vertices by negative values. We do not allow
# any negative weights as these vertices would always be bought.
#path = [1, 5, -1, 9, 8, -1, 3, 2, 6]
path = [1, 5, 0, 9, 8, 0, 3, 2, 6]

solve(path)