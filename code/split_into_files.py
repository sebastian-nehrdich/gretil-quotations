import sys
import re
import string
from tqdm import tqdm as tqdm
import os
import multiprocessing

path = "../work/"
cores=80

def process_folder():
    global list_of_nodes
    list_of_nodes = {}
    filelist = []
    for file in os.listdir(path):
        filename = os.fsdecode(file)
        filelist.append(path+filename)
    pool = multiprocessing.Pool(processes=cores)
    pool.map(turn_file_into_files,filelist)
    pool.close()


def turn_file_into_files(current_file):
    filename = current_file
    current_file = open(current_file,"r")
    last_file_name = ""
    current_file_string = ""
    result_string = ""
    count = 0 
    for line in current_file:
        current_list = line.split("\t")
        head_tag = current_list[0].split('#')[0]
        current_file_name = re.sub(".combined.*",".tab",head_tag)
        if last_file_name != "":
            if current_file_name != last_file_name:
                # if the file already exists we just append; note: this requires a line-sort afterwards, because we cannot be sure of the order. 
                with open(path + last_file_name,"a+") as text_file:
                    text_file.write(result_string)
                os.system("sort -o " + path + last_file_name + " " + path + last_file_name) # we should sort afterwards
                result_string = ""
        last_file_name = current_file_name
        result_string = result_string + line
    with open(path + last_file_name,"a+") as text_file:
        text_file.write(result_string)
    os.system("sort -o " + path + last_file_name + " " + path + last_file_name) # we should sort afterwards


    return 1
process_folder()

