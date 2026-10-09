This repository holds scripts that are useful to verify small examples for the Stackelberg Vertex Cover problem.

|File|Content|
|----|-------|
|bruteForceSolve.py|This file presents a function that can compute the optimal prices for a given graph with weights. Priceable vertices are denoted by a weight of zero. The algorithm takes exponential time, because it uses an ILP to find minimum weight vertex covers and creates an exponential sized linear program to compute the optimal prices|
|example_not_integral.py|This file contains a graph that shows that optimal prices are not integral and additionally that the split join lemma does not hold as the combination of two graphs does give more revenue then selling the same vertices in both graphs|
|example_not_half_integral.py|This holds a function to generate a family of graphs where the optimal prices are 1/(k-1) and in contrast to the previous example the optimal prices are not of the form k*1/2|
