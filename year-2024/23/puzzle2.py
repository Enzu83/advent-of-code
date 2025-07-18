# Custom input
input_data = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

connections = {}
pairs = set()

for line in input_data:
    computer1, computer2 = line.split('-')

    pairs.add((computer1, computer2))

    if computer1 not in connections:
        connections[computer1] = {computer2}
    else:
        connections[computer1].add(computer2)
    
    if computer2 not in connections:
        connections[computer2] = {computer1}
    else:
        connections[computer2].add(computer1)


# Functions

def getOneMoreTuples(connections, tuples):
    one_more_tuples = set()

    for computer, linked_computers in connections.items():
        for connection_tuple in tuples:
            if all(computer != tuple_computer and tuple_computer in linked_computers for tuple_computer in connection_tuple):
                one_more_tuple = [computer] + list(connection_tuple)
                one_more_tuples.add(tuple(sorted(one_more_tuple)))
    
    return one_more_tuples

def getMaximumClique(connections, pairs):
    tuples = getOneMoreTuples(connections, pairs)

    while len(tuples) > 1:
        tuples = getOneMoreTuples(connections, tuples)
    
    return sorted(list(tuples.pop()))


# Code

maximum_clique = getMaximumClique(connections, pairs)

print(",".join(maximum_clique))