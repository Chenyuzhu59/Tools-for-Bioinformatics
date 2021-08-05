# Author: Yuzhu Chen
# When users download sequencing data from qiita, the sequencing data of different samples are distributed in different files.
# We can use this script to split them and generate a new sequence data file that named by its sample name
# Usage: python3 split_to_sample_for_qiita.py inputfile_name
# Notes: Because I often use FASTA files, the fourteenth line is 2. If you use fastq, you can modify it appropriately.
import os
import sys

result = {}
file_name = sys.argv[1]

with open(file_name,"r") as fr:
    lines=fr.readlines()
    for i in range(0, len(lines), 2):
        line = lines[i]
        seq_id = line.rstrip()
        id = seq_id.split("_")[0][1:]
        if id not in result:
            result[id] = {}
        result[id][seq_id] = lines[i+1]
        
for id in result:
    with open(id + ".fna", "w") as fw:
        for seq_id in result[id]:
            fw.write(seq_id + "\n")
            fw.write(result[id][seq_id])
