import pandas as pd
import networkx as nx
from pyvis.network import Network

"############################ INIT SECTION ############################"
CIRCULAR_LAYOUT = True

"############################ CODE SECTION ############################"
# Read language table. Must have columns "Label" and "Implication(s)". Format CSV, separator ";".
df = pd.read_csv("TableA.xlsx - TABLE A(2).csv", sep=";",)

# Your implications as a list of strings
implications = df["Implication(s)"]

# Create an empty directed graph
G = nx.DiGraph()

# Add nodes and edges based on implications
for node, imp in zip(df["Label"], implications):
    if not pd.notna(imp):
        continue

    raw_implications = imp
    imp = imp.replace("or", " ")

    attributes = imp.translate({ord(k):" " for k in "(),"})
    attributes = attributes.split()

    imp = imp.translate({ord(k):" " for k in "()+-¬,−"})
    imp = imp.split()

    for n, attr in zip(imp, attributes):
        G.add_edge(n, node, )
        if "single_implications" not in G[n][node].keys():
            G[n][node]["single_implications"] = list()
            G[n][node]["raw_implications"] = raw_implications

        G[n][node]["single_implications"].append(attr)

# Graphics settings: layout and positions
if CIRCULAR_LAYOUT == True:
    pos = nx.circular_layout(G, scale=500)
    pos = nx.spring_layout(G, scale=500)

# Graphics settings: colors
leaf_nodes_color = "red" # es: "#79651f" -> dark brown
root_nodes_color = "green" # es: "#5a4c1a" -> yellow
other_nodes_color= "blue" # es: "#8f8877" -> clear gray

# Graphics settings: set positions and colors for each node
for node in G.nodes():
    if CIRCULAR_LAYOUT == True:
        G.nodes[node]["x"] =  pos[node][0]
        G.nodes[node]["y"] = -pos[node][1]
  
    if G.out_degree(node)==0:
        G.nodes[node]["color"] = leaf_nodes_color 
    elif G.in_degree(node)==0:
        G.nodes[node]["color"] = root_nodes_color
    else:
        G.nodes[node]["color"] = other_nodes_color

nt = Network(   directed=True,   
                cdn_resources = "remote",
                select_menu = True,
                filter_menu = True,
                # layout="barnesHut", # ocio che questo cambia un sacco di cose
                )
# nt.set_options("""
# {
# "layout": {
#     "hierarchical": {
#     "enabled": true,
#     "levelSeparation": 150,
#     "nodeSpacing": 100,
#     "treeSpacing": 200,
#     "direction": "UD",
#     "sortMethod": "directed"
#     }
# }
# 
# }
# """)

nt.toggle_physics(False)
nt.show_buttons(filter_=['physics'])
nt.from_nx(G)
nt.show('nx.html', notebook=False)
