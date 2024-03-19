import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pyvis.network import Network

"############################ INIT SECTION ############################"
CIRCULAR_LAYOUT = False
TRIDIMENSIONAL_SPRING_LAYOUT = True

"############################ CODE SECTION ############################"
df = pd.read_csv("TableA.xlsx - TABLE A.csv", )
df.drop(["Unnamed: 0"], axis=1, inplace=True)
df.drop(df.tail(1).index,inplace=True)
# print(df)

G = nx.MultiDiGraph()
G.add_nodes_from(df["Label"])

# Your implications as a list of strings
implications = df["Implication(s)"]

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges based on implications
for node, imp in zip(df["Label"], implications):
    if not pd.notna(imp):
        continue

    imp = imp.translate({ord(k):" " for k in "()+-¬,"})
    imp = imp.replace("or", " ")
    imp = imp.split()
    # print(imp)
    for n in imp:
        G.add_edge(n, node)

if CIRCULAR_LAYOUT == True:
    pos = nx.circular_layout(G, scale=500)

if TRIDIMENSIONAL_SPRING_LAYOUT == True:
    spring_3D = nx.spring_layout(G, dim=3)


# leaf nodes -> #79651f -> dark brown
# roots nodes -> #8f8877 -> clear gray
# all other nodes -> #5a4c1a -> yellow
for node in G.nodes():
    if CIRCULAR_LAYOUT == True:
        G.nodes[node]["x"] =  pos[node][0]
        G.nodes[node]["y"] = -pos[node][1]
    
    if TRIDIMENSIONAL_SPRING_LAYOUT == True:
        G.nodes[node]["x"] =  spring_3D[node][0]
        G.nodes[node]["y"] = -spring_3D[node][1]
        G.nodes[node]["z"] =  spring_3D[node][2]
  
    if G.out_degree(node)==0:
        G.nodes[node]["color"] = "#79651f" 
    elif G.in_degree(node)==0:
        G.nodes[node]["color"] = "#deb926"
    else:
        G.nodes[node]["color"] = "#8f8877"


if TRIDIMENSIONAL_SPRING_LAYOUT == True:
    x_nodes = [spring_3D[i][0] for i in G.nodes()]# x-coordinates of nodes
    y_nodes = [spring_3D[i][1] for i in G.nodes()]# y-coordinates
    z_nodes = [spring_3D[i][2] for i in G.nodes()]# z-coordinates
    edge_list = G.edges()

    #we  need to create lists that contain the starting and ending coordinates of each edge.
    x_edges=[]
    y_edges=[]
    z_edges=[]

    #need to fill these with all of the coordiates
    for edge in edge_list:
        #format: [beginning,ending,None]
        x_coords = [spring_3D[edge[0]][0],spring_3D[edge[1]][0],None]
        x_edges += x_coords

        y_coords = [spring_3D[edge[0]][1],spring_3D[edge[1]][1],None]
        y_edges += y_coords

        z_coords = [spring_3D[edge[0]][2],spring_3D[edge[1]][2],None]
        z_edges += z_coords

    #create a trace for the nodes
    trace_nodes = go.Scatter3d(x=x_nodes,
                            y=y_nodes,
                            z=z_nodes,
                            # mode='markers',
                            # marker=dict(symbol='circle',
                            #             size=10,
                            #             color=community_label, #color the nodes according to their community
                            #             colorscale=['lightgreen','magenta'], #either green or mageneta
                            #             line=dict(color='black', width=0.5)),
                            # text=club_labels,
                            # hoverinfo='text',
                            )
    
    #create a trace for the edges
    trace_edges = go.Scatter3d(x=x_edges,
                            y=y_edges,
                            z=z_edges,
                            # mode='lines',
                            # line=dict(color='black', width=2),
                            # hoverinfo='none',
                            # 
                            )

    #we need to set the axis for the plot 
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title='')
    #also need to create the layout for our plot
    layout = go.Layout(title="Feature graph",
            width=650,
            height=625,
            showlegend=False,
            scene=dict( xaxis=dict(axis),
                        yaxis=dict(axis),
                        zaxis=dict(axis),
                      ),
            margin=dict(t=100),
            hovermode='closest')
    data = [trace_edges, trace_nodes]
    fig = go.Figure(data=data, layout=layout)

    fig.show()
    exit()
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
