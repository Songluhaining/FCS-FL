import networkx as nx

from util.FileManager import list_dir, join_path

failed_graph_nodes = "/home/whn/codes/Static_Slicing-master/Static_Slicing-master/output/node"

def conductDAG(buggy_system_path):
    buggy_system_path = join_path(buggy_system_path, "variants")#"/home/whn/Desktop/BankAccountTP/4wise-BankAccountTP-1BUG-Full/_MultipleBugs_.NOB_1.ID_160/variants"
    list_failed_graph = list_dir(failed_graph_nodes)

    for nodeName in list_failed_graph:
        product_path = join_path(buggy_system_path, nodeName.split('.')[0])
        #get a causal dot
        dot = nx.DiGraph()

        nodePath = "/home/whn/codes/Static_Slicing-master/Static_Slicing-master/output/node/" + nodeName.split('.')[0] + ".txt"

        nodes = []
        with open(nodePath, 'r') as f:
            content = f.read()
            nodes = content.split(",")

        # for node in nodes:
        #     dot.node(node)
        dot.add_nodes_from(nodes)

        edges = []
        edgePath = "/home/whn/codes/Static_Slicing-master/Static_Slicing-master/output/edge/" + nodeName.split('.')[0] + ".txt"
        with open(edgePath, 'r') as f:
            for line in f:
                edges = list(line.rstrip().split("->"))
                dot.add_edge(edges[0], edges[1])

        while nx.is_directed_acyclic_graph(dot) == False:
            cycle_nodes = nx.find_cycle(dot)
            min_out_degree_node = min(cycle_nodes, key=lambda x: dot.out_degree(x[0]))
            min_out_degree_node = min_out_degree_node[0]
            successors = list(dot.successors(min_out_degree_node))
            for successor in successors:
                dot.remove_edge(min_out_degree_node, successor)

        #dot.add_edges_from(edges)

        # cycle_nodes = nx.find_cycle(dot)
        # min_out_degree_node = min(cycle_nodes, key=lambda x: dot.out_degree(x[0]))
        # min_out_degree_node = min_out_degree_node[0]
        # successors = list(dot.successors(min_out_degree_node))
        # for successor in successors:
        #     dot.remove_edge(min_out_degree_node, successor)



        # for node in topological_order:
        #     for successor in dot.successors(node):
        #         if successor in  topological_order:
        #             G_without_cycles.add_edge(node, successor)

        # cycles = list(nx.simple_cycles(dot))
        #
        # for cycle in cycles:
        #     print(cycle)
        #     cedges = list((cycle[i], cycle[i+1]) for i in range(len(cycle)-1))
        #     cedges.append((cycle[-1], cycle[0]))
        #     print("cycles: ", cedges)

        # if nx.is_directed_acyclic_graph(dot):
        #     print("Directed acyclic graph")
        # else:
        #     print("Undirected acyclic graph")
        #
        save_path = "/home/whn/Desktop/VARCOP-gh-pages_v4/VARCOP-gh-pages_v4/VARCOP-gh-pages/node_graph_dot/" + nodeName.split('.')[0] + ".dot"
        nx.nx_agraph.write_dot(dot, save_path)

        # import matplotlib.pyplot as plt
        # nx.draw(dot, node_color='lightblue', node_size=40)
        # plt.show()

def computePred_copy(productName):
    dot = nx.DiGraph()

    nodePath = "/home/whn/codes/Static_Slicing-master/Static_Slicing-master/output/node/" + productName + ".txt"

    nodes = []
    with open(nodePath, 'r') as f:
        content = f.read()
        nodes = content.split(",")

    # for node in nodes:
    #     dot.node(node)
    dot.add_nodes_from(nodes)
    # dot.add_node()

    edges = []
    edgePath = "/home/whn/codes/Static_Slicing-master/Static_Slicing-master/output/edge/" + productName + ".txt"
    with open(edgePath, 'r') as f:
        for line in f:
            edges = list(line.rstrip().split("->"))
            dot.add_edge(edges[0], edges[1])

    while nx.is_directed_acyclic_graph(dot) == False:
        cycle_nodes = nx.find_cycle(dot)
        min_out_degree_node = min(cycle_nodes, key=lambda x: dot.out_degree(x[0]))
        min_out_degree_node = min_out_degree_node[0]
        successors = list(dot.successors(min_out_degree_node))
        for successor in successors:
            dot.remove_edge(min_out_degree_node, successor)

    return dot, nodes

def computePred_copy1(node, productName):
    dot = nx.DiGraph()
    nodes = set()
    edges = []
    edgePath = "/home/whn/codes/Static_Slicing-master/Static_Slicing-master/output/edge/" + productName + ".txt"
    with open(edgePath, 'r') as f:
        for line in f:
            edges = list(line.rstrip().split("->"))
            if edges[1] == node:
                if edges[0] not in nodes and edges[0] != "Results":
                    nodes.add(edges[0])
                    dot.add_edge(edges[0], edges[1])
                    dot.add_edge(edges[0], "Results")
                    # nodes.add(edges[0])
            # expriment 3
            # elif edges[0] == node:
            #     if edges[1] not in nodes and edges[1] != "Results":
            #         nodes.add(edges[1])
            #         dot.add_edge(edges[0], edges[1])
            #         dot.add_edge(edges[1], "Results")
            #         if nx.is_directed_acyclic_graph(dot) == False:
            #             dot.remove_edge(edges[0], edges[1])
            #             dot.remove_edge(edges[1], "Results")
            #             nodes.remove(edges[1])

    dot.add_edge(node, "Results")
    nodes.add(node)
    nodes.add("Results")
    return dot, nodes
def computePred(node, productName):
    dot = nx.DiGraph()

    # nodePath = "/home/whn/codes/Static_Slicing-master/Static_Slicing-master/output/node/" + productName + ".txt"
    #
    # nodes = []
    # with open(nodePath, 'r') as f:
    #     content = f.read()
    #     nodes = content.split(",")
    #
    # # for node in nodes:
    # #     dot.node(node)
    # dot.add_nodes_from(nodes)

    nodes = set()
    edges = []
    edgePath = "/home/whn/codes/Static_Slicing-master/Static_Slicing-master/output/edge/" + productName + ".txt"
    with open(edgePath, 'r') as f:
        for line in f:
            edges = list(line.rstrip().split("->"))
            if edges[1] == node:
                if edges[0] not in nodes and edges[0] != "Results":
                    nodes.add(edges[0])
                    dot.add_edge(edges[0], edges[1])
                    dot.add_edge(edges[0], "Results")
                    # nodes.add(edges[0])
            # expriment 3
            elif edges[0] == node:
                if edges[1] not in nodes and edges[1] != "Results":
                    nodes.add(edges[1])
                    dot.add_edge(edges[0], edges[1])
                    dot.add_edge(edges[1], "Results")
                    if nx.is_directed_acyclic_graph(dot) == False:
                        dot.remove_edge(edges[0], edges[1])
                        dot.remove_edge(edges[1], "Results")
                        nodes.remove(edges[1])


    dot.add_edge(node, "Results")
    nodes.add(node)
    nodes.add("Results")
    return dot, nodes