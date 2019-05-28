import sys
import json
from collections import defaultdict 

with open(sys.argv[1]) as file:
    data = json.load(file)

    #initialization
    noOfEntities=len(data["entities"])
    noOfLinks=len(data["links"])

    initialEntity=int(sys.argv[2])

    #collecting all available id's
    entity_id=[]
    for e_id in range(0,noOfEntities):
        entity_id.append(data["entities"][e_id]["entity_id"])
    next_id=max(entity_id)

    #genrating Graph
    graph=defaultdict(list)
    for edges in range (0,noOfLinks):
        graph[data["links"][edges]["from"]].append(data["links"][edges]["to"])

    next_id+=1

    #BFS using queue for cloning the graph
    bfs_queue=[]
    bfs_queue.append(initialEntity)
    clonedBidirectionalGraph=defaultdict(list) #used for no of new nodes is cloned graph
    clonedUnidirectionalGraph=defaultdict(list) #used for no of new links in cloned graph
    visited={} #visited nodes 
    visited[initialEntity]=1
    while bfs_queue:
        top_element=bfs_queue.pop(0)
        for noOfEdges in range (0,len(graph[top_element])):
            clonedBidirectionalGraph[top_element].append(graph[top_element][noOfEdges])
            clonedBidirectionalGraph[graph[top_element][noOfEdges]].append(top_element)
            clonedUnidirectionalGraph[top_element].append(graph[top_element][noOfEdges])
            if(visited.get(graph[top_element][noOfEdges],0)!=1):
                bfs_queue.append(graph[top_element][noOfEdges])
                visited[graph[top_element][noOfEdges]]=1

    # code for adding all new nodes in the old one
    old_new_id_relation={}
    for source,dest in clonedBidirectionalGraph.items():
        old_new_id_relation[source] = next_id
        temp_node={}
        for e_id in range (0,len(data["entities"])):
            if(data["entities"][e_id]["entity_id"]==source):
                temp_node["entity_id"]=next_id
                temp_node["name"]=data["entities"][e_id]["name"]
                if(len(data["entities"][e_id])==3):
                    temp_node["description"]=data["entities"][e_id]["description"]
        data["entities"].append(temp_node)
        next_id+=1

    # code for adding connections between cloned graph using updated id's
    for source,dest in clonedUnidirectionalGraph.items():
        for noOfDest in range(0,len(dest)):
            temp_link={}
            temp_link["from"]=old_new_id_relation[source]
            temp_link["to"]=old_new_id_relation[dest[noOfDest]]
            data["links"].append(temp_link)

    #code for adding connection between intialEntity and cloned graph
    for source,dest in graph.items():
        if(initialEntity in dest):
            temp_link={}
            temp_link["from"]=source
            temp_link["to"]=old_new_id_relation[initialEntity]
            data["links"].append(temp_link)

# writing output to json file            
with open('output.json', 'w') as outfile:  
    json.dump(data, outfile, indent=2)