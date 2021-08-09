#!/bin/sh
for files in `ls *_seqs.f*`
do
	python3 split_to_sample_for_qiita.py ${files}
	mv ${files} original_data/
done
