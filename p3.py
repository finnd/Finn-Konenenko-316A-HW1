import networkx as nx
import os
import sys
import operator
from collections import OrderedDict
import itertools
from multiprocessing import Pool

def parseActors(**kwargs):
	input_file_path = kwargs['file']
	idToActorMap = {}
	with open(input_file_path) as file:
		for line in file:
			parsedLine = line.split("\t")
			idToActorMap[parsedLine[0]] = parsedLine[1]

	return idToActorMap

def parseEdges(**kwargs):
	input_file_path = kwargs['file']
	edgeArray = []
	with open(input_file_path) as file:
		for line in file:
			line.replace("\n", "")
			tabSeperatedLine = line.split("\t")
			edgeArray.append((tabSeperatedLine[0], tabSeperatedLine[1], tabSeperatedLine[2]))

	return edgeArray

def generateGraph(**kwargs):
	idToActorMap = kwargs['actorMap']
	edgeList = kwargs['edgeList']
	G = nx.Graph()

	for edge in edgeList:
		actor1 = idToActorMap[(edge[0]).replace("\r", "")]
		actor2 = idToActorMap[(edge[1]).replace("\r", "")]
		weight = edge[2]

		G.add_edge(str(actor1), str(actor2), weight=weight)

	return G

def returnLargestConnectedComponent(**kwargs):
	G = kwargs['graph']
	LCC = max(nx.connected_component_subgraphs(G), key=len)
	return LCC

def findDegreeCentralityAndPrint(**kwargs):
	G = kwargs['graph']
	returnNumber = kwargs['n']
	degree_centrality = nx.degree(G)
	sorted_degrees = OrderedDict(sorted(degree_centrality.items(), key=operator.itemgetter(1), reverse=True))
	for x in range(0, returnNumber):
		print("%d \t %s \t %d\n" % (x+1, (sorted_degrees.items()[x])[0], (sorted_degrees.items()[x])[1]))
		##print((sorted_degrees.items()[x])[0])

def findBetweenessCentrailityAndPrint(**kwargs):
	G = kwargs['graph']
	list_of_nodes = G.nodes()
	number_of_nodes = G.number_of_nodes()

	bc = {}
	for i in range(number_of_nodes-1):
		for j in range(i+1, number_of_nodes):
			print("Processing %d \t %d" % (i,j))
			paths = nx.all_shortest_paths(G, source=list_of_nodes[i], target=list_of_nodes[j])

			count = 0.0
			path_dis = {}
			for p in paths:
				count+=1.0
				for n in p[1:-1]:
					if not path_dis.has_key(n):
						path_dis[n] = 0.0
					path_dis[n]+=1.0
			for n in path_dis.keys():
				path_dis[n] = path_dis[n] / count
				if not bc.has_key(n):
					bc[n] = 0.0
				bc[n]+=path_dis[n]

	print(bc)


def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    print("Dividng Nodes")
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


def _betmap(G_normalized_weight_sources_tuple):
    """Pool for multiprocess only accepts functions with one argument.
    This function uses a tuple as its only argument. We use a named tuple for
    python 3 compatibility, and then unpack it when we send it to
    `betweenness_centrality_source`
    """
    return nx.betweenness_centrality_source(*G_normalized_weight_sources_tuple)


def betweenness_centrality_parallel(G, processes=4):
    """Parallel betweenness centrality  function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool)*4
    node_chunks = list(chunks(G.nodes(), int(G.order()/node_divisor)))
    num_chunks = len(node_chunks)
    bt_sc = p.map(_betmap,
                  zip([G]*num_chunks,
                      [False]*num_chunks,
                      ["weight"]*num_chunks,
                      node_chunks))

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c

def printTop20(c_dic):
	sorted_closeness = OrderedDict(sorted(c_dic.items(), key=operator.itemgetter(1), reverse=True))
	for x in range(0, 20):
		print("%d \t %s \t %d\n" % (x+1, (sorted_closeness.items()[x])[0], (sorted_closeness.items()[x])[1]))


if __name__ == '__main__':
	idToActorMap = parseActors(file=str(sys.argv[1]))
	edgeArray = parseEdges(file=str(sys.argv[2]))
	LCC = returnLargestConnectedComponent(graph=G)

	if str(sys.argv[3] == 'par'):
		findDegreeCentralityAndPrint(graph=LCC, n=20)
		bt = betweenness_centrality_parallel(LCC)
		printTop20(bt)
	else:
		findDegreeCentralityAndPrint(graph=LCC, n=20)
		findBetweenessCentrailityAndPrint(graph=LCC)







