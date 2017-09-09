import networkx as nx
import matplotlib.pyplot as plt

def BFS(**kwargs):
	graph = kwargs["graph"]
	source = kwargs["sourceNode"]
	q=[]
	q.append(source)
	G.node[source]["distance"] = 0
	while len(q):
		current_node = q.pop(0)
		for node in graph.neighbors(current_node):
			if len(G.node[node]) == 0 and not None:
				G.node[node]["distance"] = G.node[current_node]["distance"] + 1
				q.append(node)

	if kwargs["humanOutput"] is True:
		print("NODE\tDISTANCE FROM " + source)
		print("--------------------------")
		for node in G.nodes():
			print (str(node) + "\t" + str(G.node[node]["distance"]))
	else:
		distancesArray = []
		for node in G.node:
			distancesArray.append(G.node[node]["distance"])
		return distancesArray

def pairwiseDistancesToDistanceDistrobution(**kwargs):
	graph = kwargs["graph"]
	nodesList = graph.nodes()
	visitedNodes = []
	uniqueDistances = []
	sp = nx.all_pairs_shortest_path_length(graph)
	for sourceNode in nodesList:
		source = sourceNode
		for targetNode in nodesList:
			target = targetNode
			if target != source and target not in visitedNodes:
				distance = sp[source][target]
				uniqueDistances.append(distance)
		visitedNodes.append(source)
	counts = {}
	for distance in uniqueDistances:
		if distance in counts:
			counts[distance] = counts[distance] + 1
		else:
			##make new key
			counts[distance] = 1
			

	plt.bar(range(len(counts)), counts.values(), align="center")
	plt.xticks(range(len(counts)), counts.keys())
	plt.xlabel("Distances")
	plt.ylabel("Counts")
	plt.title("Distance Distrobution for Arpanet")
	plt.show()




		



if __name__ == "__main__":
	
	## create the graph
	G = nx.Graph()
	## add the arpanet edges
	edgeList = [("USCB", "SRI"), ("USCB", "UCLA"),
				("SRI", "STAN"), ("SRI", "UTAH"), ("SRI", "UCLA"),
				("UCLA", "STAN"), ("UCLA", "RAND"),
				("RAND", "SDC"), ("RAND", "BBN"),
				("UTAH", "SDC"), ("UTAH", "MIT"),
				("MIT", "LINC"), ("MIT", "BBN"),
				("BBN", "HARV"),
				("LINC", "CASE"),
				("HARV", "CARN"),
				("CARN", "CASE")]

	G.add_edges_from(edgeList)
	##print(BFS(graph=G, sourceNode="CASE", humanOutput=False))
	pairwiseDistancesToDistanceDistrobution(graph=G)
	



	## push read nodes to an array
	## BFS for each starting node. If the ending node is in array, stop