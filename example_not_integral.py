from bruteForceSolve import solve, joinDicts

G1_weights = {
    0: 0,
    1: 1,
    2: 0,
    3: 1,
    4: 0,
    5: 1,
}

G1_edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 0),
]


G2_weights = {
    0: 0,
    2: 0,
    4: 0,
    6: 2,
    7: 2,
    8: 2,
}

G2_edges = [
    (0, 6),
    (2, 8),
    (4, 7),
    (6, 7),
    (7, 8),
    (6, 8),
]

G3_weights = {
    0: 0,
    2: 0,
    4: 0,
    9: 2,
    10: 2,
    11: 2,
}

G3_edges = [
    (0, 9),
    (2, 11),
    (4, 10),
    (9, 10),
    (9, 11),
    (10, 11),
]


combined_weights = joinDicts([G1_weights, G2_weights])
combined_edges = G1_edges + G2_edges

selection, prices, revenue = solve(combined_weights, combined_edges)

print("Combined:", selection, prices, revenue)
print("G1:", solve(G1_weights, G1_edges, selection))
print("G2:", solve(G2_weights, G2_edges, selection))

combined_weights = joinDicts([G1_weights, G2_weights, G3_weights])
combined_edges = G1_edges + G2_edges + G3_edges

selection, prices, revenue = solve(combined_weights, combined_edges)

print("Combined:", selection, prices, revenue)
print("G1:", solve(G1_weights, G1_edges, selection))
print("G2:", solve(G2_weights, G2_edges, selection))
print("G3:", solve(G3_weights, G3_edges, selection))