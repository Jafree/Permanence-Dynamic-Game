'''
Created on 2014/10/11

@author: free
'''
import igraph
from random import randint
"This function is used for drawing graph with community membership"
"The input parameters are an igraph instance, a membership list which denote the community belongings"
"Format is a file path with extension format, which is denoted by a string"
def my_igraph_plot(g, membership=None,format=None):
    if membership is not None:
        gcopy = g.copy()
        edges = []
        edges_colors = []
        for edge in g.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                edges_colors.append("gray")
            else:
                edges_colors.append("black")
        gcopy.delete_edges(edges)
        layout = gcopy.layout("kk")
        g.es["color"] = edges_colors
    else:
        layout = g.layout("kk")
        g.es["color"] = "gray"
    visual_style = {}
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_shape"] = "circle"
    visual_style["edge_color"] = g.es["color"]
    #visual_style["bbox"] = (4000, 2500)
    #visual_style["bbox"] = (1024, 768)
    #visual_style["bbox"] = (960,720)
    visual_style["vertex_size"] = 30
    visual_style["layout"] = layout
    visual_style["margin"] = 40
    #visual_style["edge_label"] = g.es["weight"]
    for vertex in g.vs():
        vertex["label"] = vertex.index
    if membership is not None:
        colors = []
        for i in range(0, max(membership)+1):
            colors.append('%06X' % randint(0, 0xFFFFFF))
        for vertex in g.vs():
            vertex["color"] = str('#') + colors[membership[vertex.index]]
        visual_style["vertex_color"] = g.vs["color"]
    if format != None:
        igraph.plot(g,target=format,**visual_style)
    else:
        igraph.plot(g, **visual_style)
if __name__ == "__main__":
    g = igraph.Graph.Famous("Zachary")
    cl = g.community_infomap()
    membership = cl.membership
    my_igraph_plot(g, membership)