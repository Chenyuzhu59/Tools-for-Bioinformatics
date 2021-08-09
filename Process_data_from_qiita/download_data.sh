#!/bin/sh
# Author: Yuzhu Chen
# Usage: sh download_data.sh study_id
# For example, sh download_data.sh 1038
# You only need to add the study_id by your own, then this script will help you download raw data from qiita
# It is recommended to use on the remote server, the download will be faster.

study_id=$1

wget --no-check-certificate 'https://qiita.ucsd.edu/public_download/?data=raw&study_id='$1'&study_type=16S'