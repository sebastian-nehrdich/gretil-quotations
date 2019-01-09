import sys
import re
import string
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm as tqdm
import os
import multiprocessing
from collections import Counter
# this script works on the raw, unsplitted output data that is created by the script calculate_sanskrit2sanskrit.py (just put that data into a seperate folder and run this script on the folder in order to get the graph)
g = nx.MultiDiGraph()
namedic = {}
omit_dic = []
threshold = 0.05

def populate_namedic(namedic):
    f = open("../data/skt-gretil-filenames-for-graph.tab",'r')
    c = 0 
    for line in f:
        m = re.search("^([^\t]+)\t(.+)", line) 
        if m:
            namedic[m.group(1)] = m.group(2) + "\n (" + m.group(1) + ")"
            c += 1
populate_namedic(namedic)

def process_folder(path):
    global list_of_nodes
    list_of_nodes = {}
    list_of_total_counts = {}
    filelist = []
    for file in os.listdir(path):
        filename = os.fsdecode(file)
        filelist.append(path+filename)
    global pool
    pool = multiprocessing.Pool(processes=40)
    results = pool.map(collect_stats_from_file,filelist)
    total_count = 0
    for local_nodes,count,main_file_counts in results:
        print(len(local_nodes))
        total_count += count
        for key in local_nodes:
            if not key in list_of_nodes.keys():
                list_of_nodes[key] = local_nodes[key]
            else:
                list_of_nodes[key] = list_of_nodes[key] + local_nodes[key]
        for key in main_file_counts:
            if not key in list_of_total_counts.keys():
                list_of_total_counts[key] = main_file_counts[key]
            else:
                list_of_total_counts[key] += main_file_counts[key]                
    pool.close()
    create_graph(list_of_nodes,total_count,list_of_total_counts)


def collect_stats_from_file(current_file):
    print(current_file)
    master_filename = current_file
    current_file = open(current_file,"r")
    main_file_name = ""
    list_of_local_nodes = {}
    main_file_count = {}
    local_count = 0
    c = 0
    for line in current_file:
        current_list = line.split("\t")
        current_file_name = []
        m = re.search("^(.*)\.r",current_list[0][:25])
        if m:
            filename = m.group(1)
            if filename in namedic.keys():
                main_file_name = namedic[filename].replace("\n"," ")
            else:
                main_file_name = filename
        else:
            m = re.search("^(.*)\.o",current_list[0][:25])
            if m:
                filename = m.group(1)
                if filename in namedic.keys():
                    main_file_name = namedic[filename].replace("\n"," ")
                else:
                    main_file_name = filename
        if "#" in main_file_name:
            print("MAIN FILE: ")
            print(main_file_name)
            print("ENTRY:")
            print(current_list[0])

        if not main_file_name in list_of_local_nodes.keys():
            list_of_local_nodes[main_file_name] = []
            main_file_count[main_file_name] = 1
        else:
            main_file_count[main_file_name] += 1
        for entry in current_list[1:]: 
            quoted_file = ""
            m = re.search("\#(\d+\.\d+)\#",entry)
            if m:
                current_score = float(m.group(1))
                if float(m.group(1)) < threshold:
                    m = re.search("^(.*)\.r",entry[:25])
                    if m:
                        if m.group(1) in namedic.keys():
                            quoted_file = namedic[m.group(1)].replace("\n"," ")
                        else:
                            quoted_file = m.group(1)
                    else:
                        m = re.search("^(.*)\.o",entry[:25])
                        if m:
                            if m.group(1) in namedic.keys():
                                quoted_file = namedic[m.group(1)].replace("\n"," ")
                            else:
                                quoted_file = m.group(1)
                            if "#" in quoted_file:
                                print("QUOTED FILE: ")
                                print(quoted_file)
                                print("ENTRY:")
                                print(entry)
            # print("MAIN FILE: " + main_file_name)                
            # print("QUOTED FILE: " + quoted_file)
            if not main_file_name == "" and not quoted_file == "" and not main_file_name in omit_dic and not quoted_file in omit_dic:
                list_of_local_nodes[main_file_name].append(quoted_file)
                local_count += 1
    print(main_file_count)
    print("DONE: " + master_filename)
    print(c)
    print(local_count)
    print(len(list_of_local_nodes))
    return [list_of_local_nodes,local_count,main_file_count]

def create_graph(list_of_nodes,total_count,list_of_total_counts):
    idcount = 0
    for entry in list_of_nodes:
        g.add_node(entry)
        counts = (Counter(list_of_nodes[entry]))
        counts = counts.most_common()
        for count in counts:
            if count[1] > 1:
                quoted_file = count[0]
                g.add_node(quoted_file)
                # Oliver Hellwig's formula: number_of_quotes / (total_len_source * total_len_target)
                # My current metric is much simpler: edge weight = number_of_quotes / total_number_of_quotes
                edge_weight = count[1] / list_of_total_counts[entry]
                #edge_weight = count[1] #/ total_count
                g.add_edge(entry,quoted_file,weight=edge_weight,key=idcount)
                # print(entry)
                # print(quoted_file)
                # print(edge_weight)
            idcount += 1
    print(list_of_total_counts)
    nx.write_graphml(g, "../graph/gretil.graphml")         
                
process_folder("../raw")


