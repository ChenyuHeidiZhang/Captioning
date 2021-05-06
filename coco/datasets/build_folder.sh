#!/usr/bin/env bash

#$ -wd /export/b02/czhan105/coco/datasets
#$ -N coco-download
#$ -j y -o $JOB_NAME-$JOB_ID.out
#$ -M czhan105@jhu.edu
#$ -m e

conda activate MIC
python build_dataset_folder.py
