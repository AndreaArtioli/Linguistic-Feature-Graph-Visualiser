import pandas as pd
import networkx as nx
from pyvis.network import Network

"############################ INIT SECTION ############################"
CIRCULAR_LAYOUT = False

"############################ CODE SECTION ############################"
df = pd.read_csv("TableA.xlsx - TABLE A.csv", )
df.drop(["Unnamed: 0"], axis=1, inplace=True)
df.drop(df.tail(1).index,inplace=True)
# print(df)

G = nx.MultiDiGraph()
G.add_nodes_from(df["Label"])

# Your implications as a list of strings
implications = df["Implication(s)"]

# Create an empty directed graph
G = nx.DiGraph()

# Add nodes and edges based on implications
for node, imp in zip(df["Label"], implications):
    if not pd.notna(imp):
        continue

    imp = imp.translate({ord(k):" " for k in "()+-¬,−"})
    imp = imp.replace("or", " ")
    imp = imp.split()
    # print(imp)
    for n in imp:
        G.add_edge(n, node)

if CIRCULAR_LAYOUT == True:
    pos = nx.circular_layout(G, scale=500)

leaf_nodes_color = "red" # es: "#79651f" -> dark brown
root_nodes_color = "green" # es: "#5a4c1a" -> yellow
other_nodes_color= "blue" # es: "#8f8877" -> clear gray

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

# print(len(G.nodes()))
# print(G.nodes())

# print(nx.is_directed_acyclic_graph(G))
nt = Network(   directed=True,   
                cdn_resources = "remote",
                select_menu = True,
                filter_menu = True,
                # layout="barnesHut", # ocio che questo cambia un sacco di cose
                )

nt.toggle_physics(False)
nt.show_buttons(filter_=['physics'])
nt.from_nx(G)
nt.show('nx.html', notebook=False)
