## This dir contains some scripts for qiita data
#### 1. split_to_sample.py
* Usage: python3 split_to_sample.py inputfile_name
* If there are many seqs files, you can use it with for.sh.
* This script helps you to split fasta/fastq data from qiita.
* When users download sequencing data from qiita, the sequencing data of different samples are distributed in different files.We can use this script to split them and generate a new sequence data file that named by its sample name.
* Notes: Because I often use FASTA files, the fourteenth line is 2. If you use fastq, you can modify it appropriately.
#### 2. download_data.sh
* Usage: sh download_data.sh study_id
* This script helps you to download qiita data in remote server.
* You only need to input the study_id by your own, then this script will help you download raw data from qiita.
