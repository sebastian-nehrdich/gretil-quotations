from tqdm import tqdm
from main import skt_stop,skt_get_vectors_fast,get_sif_skt
import numpy as np
import pickle
import os
import re
import nmslib
import h5py
import multiprocessing

# main parameters
windowsize = 7 # size of the window, the number of words that we sum up for vector comparision (7 is a good start, lower might work as well)
skip_gap = 1 # this value determines how many words we skip when creating the summarized vectors (a value of two for example will create vectors only for every second word in the collection, 3 only for every third and so on)
cutoff = 0.1 # (cutoff-value for the similarity of the matches)
cores = 80 # adjust this to the number of threads your machine can make use of

def create_weighted_sum_vector(vectorlist,weightlist):
    return np.average(vectorlist,axis=0,weights=weightlist)

def create_data(sktfolder):
    sktwords = []
    sktvectors = []
    sktweights = []
    sumvectors = []
    sktfile_indicies = []
    total_c = 0
    last_sktfile_index = 0
    for file in tqdm(os.listdir(sktfolder)):
        sktfilename = os.fsdecode(file)
        print(sktfilename)
        sktfile = open(sktfolder+sktfilename,"r")
        if "combined" in sktfilename:
            c = 0
            for line in sktfile:
                if len(line.rstrip('\n')) > 1 and "\t" in line:
                    split_line = line.split("\t")
                    if len(split_line) == 2:
                        line_sandhied,line_split = split_line
                        line_split = line_split.replace('\n',' / ')
                        line_split = re.sub("[^a-zA-Z0-9/ ]"," ",line_split)
                        last_line_split = ""
                        while line_split != last_line_split:
                            line_split = line_split.replace("  "," ")
                            last_line_split = line_split
                        current_words = line_split.split()
                        for i in range(0,len(current_words)):
                            if not current_words[i] in skt_stop and re.match(r"[a-zA-Z]", current_words[i]) and not re.match(r"[0-9]", current_words[i]) and len(current_words[i]) > 1:
                                sktwords.append([sktfilename,c,current_words[i],line_sandhied])
                                sktweights.append(get_sif_skt(current_words[i]))
                                sktvectors.append(skt_get_vectors_fast(current_words[i])[0])
                            c += 1
            total_c += c
            sktfile_indicies.append([sktfilename,last_sktfile_index,total_c-1])
            last_sktfile_index = total_c
    print("Adding to index...")
    sumvectors = []
    global list_of_ids
    list_of_ids = []
    for c in tqdm( range(0,len(sktvectors),skip_gap)):
        sumvector = create_weighted_sum_vector(sktvectors[c:c+windowsize],sktweights[c:c+windowsize])
        sumvectors.append(sumvector)
        list_of_ids.append(c)
    with h5py.File('../data/sktvectors.h5', 'w') as hf:
        hf.create_dataset("sktvectors",  data=sktvectors)
    with h5py.File('../data/sktsumvectors.h5', 'w') as hf:
        hf.create_dataset("sumvectors",  data=sumvectors)
    index = nmslib.init(method='hnsw', space='cosinesimil')
    index.addDataPointBatch(sumvectors,list_of_ids)
    print("Creating Index...")
    index.createIndex({'post': 2}, print_progress=True)
    index.saveIndex('../data/skt_all.nms')
    pickle.dump(sktwords, open( "../data/sktwords.p", "wb" ) )
    # these two should match!
    print(len(sktvectors))
    print(len(sumvectors))
    return 1


create_data("../data/etexts-combined/")

#load previously stored data
sktwords = pickle.load( open( "../data/sktwords.p", "rb" ) )
vectordata = h5py.File('../data/sktvectors.h5', 'r')
vectorsumdata = h5py.File('../data/sktsumvectors.h5', 'r')
sumvectors = vectorsumdata.get('sumvectors')
sktvectors = vectordata.get('sktvectors')
print(len(sktvectors))
index = nmslib.init(method='hnsw', space='cosinesimil')
index.loadIndex('../data/skt_all.nms')



def skt_create_data_by_fileindex(fileindex):
    threshold = 0
    len_of_k = 30
    print("FILEINDICIES:")
    print(fileindex[0])
    print(fileindex[1])
    global results,precise_vectors,result_pairs
    results = index.knnQueryBatch(sumvectors[fileindex[0]:fileindex[1]],k=len_of_k,num_threads=80)
    return [fileindex,results]

def process_result(data):
    results,current_main_sentence_position = data
    total_length = len(sktwords)
    
    current_main_sentence = ' '.join([word[2] for word in sktwords[current_main_sentence_position:current_main_sentence_position+windowsize]])  + " # " + sktwords[current_main_sentence_position][3]
    last_line = sktwords[current_main_sentence_position][3]
    for c in range(current_main_sentence_position,current_main_sentence_position+windowsize):
        if c+windowsize < total_length:
            if sktwords[c][3] != last_line:
                current_main_sentence += " / " + sktwords[c][3]
            last_line = sktwords[c][3]
    result_string =  sktwords[current_main_sentence_position][0] + '#' + '{0:10d}'.format(current_main_sentence_position) + "#" + current_main_sentence
    list_of_already_found_parallels = []
    result_pairs = [list(pair) for pair in zip(results[1],results[0])]
    for result in sorted(result_pairs):
        result_position = result[1]
        result_score = result[0]
        if result[1]+windowsize < len(sktwords):
            if result_score < cutoff and (result_position < current_main_sentence_position- 20 or result_position > current_main_sentence_position + 20) and  sktwords[result[1]][0] == sktwords[result[1]+windowsize][0]:
                current_result_sentence = ' '.join([word[2] for word in sktwords[result_position:result_position+windowsize]]) + " # " + sktwords[result_position][3]
                last_line = sktwords[result_position][3]
                for c in range(result_position,result_position+windowsize):
                    if c+windowsize < total_length:         
                        if sktwords[c][3] != last_line:
                            current_result_sentence += " / " + sktwords[c][3]
                        last_line = sktwords[c][3]
                if not current_result_sentence in list_of_already_found_parallels:
                    result_string += "\t" + sktwords[result_position][0] + "#"  + str(result_position) + "#" + str(result_score) + "#" + "#" + current_result_sentence
                    list_of_already_found_parallels.append(current_result_sentence)
    return result_string

def skt_result_turn_to_file(data):
    fileindex, results = data
    result_string = ""
    #print("Now processing: " + str(fileindex[0]))
    #print(abs(fileindex[0]-fileindex[1]))
    pool = multiprocessing.Pool(processes=cores)
    result_strings = pool.map(process_result,zip(results,list(range(fileindex[0],fileindex[1]))))
    pool.close()
    
    result_string = "\n".join(result_strings)
    del result_strings
    with open("../work/" + str(fileindex[0]) + ".parallels", "w") as text_file:
        text_file.write(result_string)

def process_index(fileindex):
    data = (skt_create_data_by_fileindex(fileindex))
    return skt_result_turn_to_file(data)

def create_chunks(end):
    step = 1000000
    list_of_pairs = []
    i = 0
    while i < end:
        if i + step > end:
            list_of_pairs.append([i,end])
            break
        else:
            list_of_pairs.append([i,i+step-1])
            i += step

    return list_of_pairs
        
def skt_all_against_all():
    chunks = create_chunks(len(sktwords))
    stepsize = 1
    for i in tqdm(range(len(chunks))):
        process_index(chunks[i])

skt_all_against_all()

