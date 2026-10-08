from bruteForceSolve import solve, joinDicts

k = 4

def generateGraphs(k):
    G1_weights = {0 : 1}
    G1_edges = []

    for i in range(k):
        G1_weights[i+1] = 0
        G1_edges.append((0, i+1))

    G2_weights = {}
    G2_edges = []

    for i in range(k):
        G2_weights[i+1] = 0
        G2_weights[i+k+2] = 1

        G2_edges.append((i+1, i+k+2))

        for j in range(k+2, i+k+2):
            G2_edges.append((j, i+k+2))

    return G1_weights, G1_edges, G2_weights, G2_edges


G1_weights, G1_edges, G2_weights, G2_edges = generateGraphs(k)

combined_weights = joinDicts([G1_weights, G2_weights])
combined_edges = G1_edges + G2_edges

selection, prices, revenue = solve(combined_weights, combined_edges)

print("Combined:", selection, prices, revenue)
print("G1:", solve(G1_weights, G1_edges, selection))
print("G2:", solve(G2_weights, G2_edges, selection))

combined_weights = joinDicts([G1_weights, G2_weights])
combined_edges = G1_edges + G2_edges

selection, prices, revenue = solve(combined_weights, combined_edges)

print("Combined:", selection, prices, revenue)
print("G1:", solve(G1_weights, G1_edges, selection))
print("G2:", solve(G2_weights, G2_edges, selection))