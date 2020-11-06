import networkx as nx
import matplotlib.pyplot as plt
import unittest
from typing import Union


class GraphError(Exception):
	pass


class Graph:
	def __init__(self, vertices: list, edges: list):
		self.vertices = vertices
		self.edges = edges

	def get_neighbour_edges(self, cur: Union[str, int]) -> list:
		"""
		Returns a list of neighbouring edges that are adjacent to cur
		"""
		return [edge for edge in self.edges if cur in edge]

	def get_neighbour_vertices(self, cur: Union[str, int]) -> list:
		"""
		Returns a list of neighbouring vertices that are adjacent to cur
		"""
		vertices = [edge[0] if edge[1] == cur else edge[1] for edge in self.get_neighbour_edges(cur)]
		return vertices

	def is_connected(self, start: Union[str, int], end: Union[str, int]) -> bool:
		"""
		Returns a duplicate of the current graph
		"""
		if start not in self.vertices or end not in self.vertices:
			raise GraphError("Start or end not found in graph")

		visited = dict(zip(self.vertices, [False] * len(self.vertices)))
		queue = []
		queue.append(start)
		visited[start] = True

		while queue:
			cur = queue.pop(0)

			if cur == end:
				return True

			neighbours = self.get_neighbour_vertices(cur)
			for neighbour in neighbours:
				if not visited[neighbour]:
					queue.append(neighbour)
					visited[neighbour] = True

		return False

	def duplicate(self):
		"""
		Returns a duplicate of the current graph
		"""
		return Graph(self.vertices[:], self.edges[:])

	def draw(self):
		"""
		Draws the graph using networkx and matplotlib
		"""
		nx_graph = self.parse_graph()
		pos = nx.spring_layout(nx_graph, k=0.15, iterations=20) # to spread out the nodes

		nx.draw(nx_graph, pos, edge_color="black", width=1, linewidths=1, node_size=500, node_color="pink", alpha=0.9, with_labels=True)

		edge_labels = {(edge[0], edge[1]):edge[2] for edge in self.edges}
		nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_color='red')

		plt.show()

	def parse_graph(self):
		"""
		Converts the existing graph to networkx format
		"""
		nx_graph = nx.Graph()
		for node in self.vertices:
			nx_graph.add_node(node)

		for edge in self.edges:
			node1, node2, weight = edge
			nx_graph.add_edge(node1, node2, weight=weight)

		return nx_graph

	def __str__(self):
		print("Vertices:\t", self.vertices)
		print("Edges:\t", self.edges)


class Minimum_Spanning_Tree:
	def __init__(self, graph):
		self.graph = graph

	def kruskal_solve(self):
		"""Obtain a minimum spanning tree from the connected graph using Kruskal's Algorithm"""

		min_span_tree = Graph(self.graph.vertices, [])
		edges = sorted(self.graph.edges[:], key=lambda x: x[2])
		count = 0

		while count < len(self.graph.vertices) - 1:
			cur_edge = edges[0]
			edges = edges[1:]
			
			node1, node2, weight = cur_edge
			if not min_span_tree.is_connected(node1, node2):
				min_span_tree.edges.append(cur_edge)
				count = count + 1

		return min_span_tree

	def prim_solve(self):
		"""Obtain a minimum spanning tree from the connected graph using Prim's Algorithm"""

		min_span_tree = Graph([self.graph.vertices[0]], [])
		dup_graph = self.graph.duplicate()

		for i in range(len(self.graph.vertices) - 1):
			neighbour_edges = []
			for cur in min_span_tree.vertices:
				neighbour_edges += dup_graph.get_neighbour_edges(cur)

			neighbour_edges.sort(key=lambda x: x[2])
			shortest_edge = neighbour_edges[0]
			new_node = shortest_edge[0] if shortest_edge[1] in min_span_tree.vertices else shortest_edge[1]

			min_span_tree.edges.append(shortest_edge)
			min_span_tree.vertices.append(new_node)
			dup_graph.edges.remove(shortest_edge)

		return min_span_tree

	def draw_min_span_tree(self):
		"""
		Draws the before and after result of applying the minimum spanning tree algorithm
		"""
		self.graph.draw()

		min_span_tree = self.kruskal_solve()
		min_span_tree.draw()


class Test_Minimum_Spanning_Tree(unittest.TestCase):
	def setUp(self):
		# Test graph 1
		vertices = ["Minneapolis", "Milwaukee", "Chicago", "St. Louis", "Detroit", "Cincinnati", "Louisville", "Nashville"]
		edges = [
			["Minneapolis", "Chicago", 355],
			["Minneapolis", "Nashville", 695],
			["Milwaukee", "Chicago", 74],
			["Milwaukee", "Louisville", 348],
			["Chicago", "Louisville", 269],
			["Chicago", "St. Louis", 262],
			["St. Louis", "Louisville", 242],
			["Nashville", "Louisville", 151],
			["Louisville", "Cincinnati", 83],
			["Louisville", "Detroit", 306],
			["Cincinnati", "Detroit", 230]
		]
		self.test_graph_1 = Graph(vertices, edges)
		self.test_min_spanning_tree_1 = Minimum_Spanning_Tree(self.test_graph_1)

	def test_graph_connected(self):
		self.assertTrue(self.test_graph_1.is_connected("Minneapolis", "Milwaukee"))

	def test_kruskal_solve(self):
		result_1 = self.test_min_spanning_tree_1.kruskal_solve()

		# Checks that n vertices have n - 1 edges
		self.assertTrue(len(result_1.vertices) == len(result_1.edges) + 1)

		# Checks that all the edges are still connected
		start = result_1.vertices[0]
		for end in result_1.vertices[1:]:
			self.assertTrue(result_1.is_connected(start, end))

	def test_prim_solve(self):
		result_1 = self.test_min_spanning_tree_1.prim_solve()

		# Checks that n vertices have n - 1 edges
		self.assertTrue(len(result_1.vertices) == len(result_1.edges) + 1)

		# Checks that all the edges are still connected
		start = result_1.vertices[0]
		for end in result_1.vertices[1:]:
			self.assertTrue(result_1.is_connected(start, end))

	def test_kruskal_prim_solve(self):
		result_1_kruskal = self.test_min_spanning_tree_1.kruskal_solve()
		result_1_prim = self.test_min_spanning_tree_1.prim_solve()
		# print(result_1_kruskal)
		# print(result_1_prim)

		self.assertCountEqual(result_1_kruskal.vertices, result_1_prim.vertices)
		self.assertCountEqual(result_1_kruskal.edges, result_1_prim.edges)


def main():
	# Test graph 1
	test = Test_Minimum_Spanning_Tree()
	test.setUp()
	test_graph_1 = test.test_graph_1
	test_min_spanning_tree_1 = Minimum_Spanning_Tree(test_graph_1)
	test_min_spanning_tree_1.draw_min_span_tree()


if __name__ == '__main__':
	# unittest.main(verbosity=2)
	main()
