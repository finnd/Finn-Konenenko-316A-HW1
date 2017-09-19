import os
import sys
import networkx as nx


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

def generateSubGraph(**kwargs):
	source = kwargs['graph']
	actorMap = kwargs['actorMap']
	bacon = actorMap["3257"]
	
	subGraph = nx.Graph()

	graphInfo = source[bacon]

	neighborsArray = G.neighbors(bacon)

	for node in neighborsArray:
		assoc = source[node]

		for key, value in assoc.iteritems():
			actor1 = node
			actor2 = key
			weight = value['weight']
			subGraph.add_edge(actor1, actor2, weight=weight)

	return subGraph

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

	return bc

def printTop20(c_dic):
	sorted_closeness = OrderedDict(sorted(c_dic.items(), key=operator.itemgetter(1), reverse=True))
	for x in range(0, 20):
		print("%d \t %s \t %d\n" % (x+1, (sorted_closeness.items()[x])[0], (sorted_closeness.items()[x])[1]))


if __name__ == "__main__":
	idToActorMap = parseActors(file=str(sys.argv[1]))
	edgeArray = parseEdges(file=str(sys.argv[2]))
	G = generateGraph(actorMap = idToActorMap, edgeList = edgeArray)
	sub = generateSubGraph(graph=G, actorMap = idToActorMap)
	bc = findBetweenessCentrailityAndPrint(graph=sub)
	printTop20(bc)
