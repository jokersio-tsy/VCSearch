#!/bin/bash

# available_datasets=("merge_contra" "merge_missing" "merge_mathtrap_cat" "merge_ID" "GSM-ICm_2k" "robustmath")
available_datasets=("merge_ID" "GSM-ICm_2k" "robustmath" "aftvalid_merge_missing")

for dataset in "${available_datasets[@]}"; do
    echo "working on dataset: $dataset"
    
    python main.py --dataset "$dataset" --algo smt_search_refine --model Qwen3b --gpu 3
    
done