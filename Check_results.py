import json
import random
import argparse
import os
import re
from fractions import Fraction
from collections import Counter
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Process some arguments.")
    
    parser.add_argument('--log', type=str, default="")
    parser.add_argument('--category', action="store_true")
    
    args = parser.parse_args()
    
    return args


def convert_to_float(value):
    if type(value) != str:
        return value
    try:
        # 处理字符串为浮点数
        if '/' in value:
            # 如果是分数形式，使用 Fraction 转换
            return float(Fraction(value))
        else:
            # 否则直接转换为浮点数
            return float(value)
    except ValueError:
        return None  # 如果转换失败，返回 None

class CHECKER:
    def __init__(self,algo,log):
        self.cor = 0 
        self.sum = 0
        # self.data_type = data_type
        self.algo = algo
        self.log = log
    
    def print_results(self):
        # print("{} dataset".format(self.data_type))
        print("##### log ",self.log)
        print("cor",self.cor)
        print("sum",self.sum)
        print("acc",self.cor/self.sum)

    def evaluate_each(self,candidate_ans,candidate_target,line):
        # print(candidate_ans)
        self.sum += 1
        if candidate_target == None:
            target = "Reject"
        else:
            target = convert_to_float(candidate_target)

        if "smt_search_refine" in self.algo:
            try:
            # print(type(line['ans_lst']))
            # print(line)
                if candidate_ans == "UnSAT" or candidate_ans == "Multi" or (len(line['ans_lst']) == 1 and line['ans_lst'][0] == "Error"):
                    ans = "Reject"
                else:
                    ans = convert_to_float(candidate_ans)
            except:
                ans = None

        elif "smt" in self.algo or "logic" in self.algo:
            if candidate_ans == "UnSAT" or candidate_ans == "Multi":
                ans = "Reject"
            else:
                ans = convert_to_float(candidate_ans)
            
        elif "pal" in self.algo:
            # print(candidate_ans)
            if type(candidate_ans) == str and "unsolvable" in candidate_ans:
                ans = "Reject"
            else:
                ans = convert_to_float(candidate_ans)
        
        else:
            if candidate_ans==None or candidate_ans == "Reject":
                ans = "Reject"
            else:
                ans = convert_to_float(candidate_ans)

        # try: 
        if ans == target:
            self.cor += 1
        # except:
        #     pass


def get_belong(input_string):
    pattern = r"([a-zA-Z]+)\d+$"

    # 使用 re.search 查找匹配
    match = re.search(pattern, input_string)

    return match.group(1)

def check_results(filename,args):
    print(filename)

    if "contra" in filename.lower() or "missing" in filename.lower() or "trap" in filename.lower():
        print("OOD dataset")
    else:
        print("ID dataset")

    main_checker = CHECKER(algo=filename,log="main")
    detail_checker = {}

    data =[]
    with open(filename, 'r') as jsonl_file:
        for line in jsonl_file:
            data.append(json.loads(line.strip())) 


    for line in data:
        if 'ans' in line:
            reply_ans = line['ans']
        else:
            raise KeyError

        target  = line['target']
        id = line['id']

        main_checker.evaluate_each(candidate_ans=reply_ans,candidate_target=target,line =line)

        if type(id) == str:
            belong = get_belong(id)
            if belong in detail_checker.keys():
                detail_checker[belong].evaluate_each(candidate_ans=reply_ans,candidate_target=target,line=line)
            else:
                new_checker = CHECKER(algo=filename,log = belong)
                detail_checker[belong] = new_checker
                detail_checker[belong].evaluate_each(candidate_ans=reply_ans,candidate_target=target,line=line)

    main_checker.print_results()
    for k in detail_checker.keys():
        detail_checker[k].print_results()


if __name__ == "__main__":

    args = get_args()

    directory = "results_sample120/debugv3/deepseek"

    for root, dirs, files in os.walk(directory):
        for file in files:
            file = os.path.join(root, file)
            if args.log in file.lower():
                try:
                    check_results(file,args)
                except:
                    pass