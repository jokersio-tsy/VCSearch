import argparse
import json
from model import DeepSeek_API,Qwen,Zhipu,Doubao,deepcoder,GPT4
from Solve_VCSearch import solve_zero_each
import tqdm
import random
import datetime
import signal
import time

class TimeoutError(Exception):
    pass

# 超时处理函数
def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out")

# 设置超时
def set_timeout(seconds):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)

import os
os.environ["http_proxy"] = 'http://114.212.22.109:7890'
os.environ["https_proxy"] = 'http://114.212.22.109:7890'
os.environ['all_proxy'] = 'socks5://114.212.22.109:7891'

def get_args():
    parser = argparse.ArgumentParser(description="Process some arguments.")
    
    parser.add_argument('--model', type=str, default="deepseek")
    parser.add_argument('--dataset', type=str, default='gsm8k')
    parser.add_argument('--algo', type = str, default='VCSearch')
    parser.add_argument('--template', type = str, default='Math')
    parser.add_argument('--gpu', type = str, default='0')
    parser.add_argument('--sample',type = int, default=-1,help="only test 200 sample on each dataset to fast reason")
    parser.add_argument('--final',action="store_true",help="final results")
    parser.add_argument('--log',type= str,default="NONELOG",help= "results log")
    
    args = parser.parse_args()
    
    return args

def solve(args,ask_question,chat_model):
    print(args.algo)
    if args.algo == "zero":
        record = solve_zero_each(ask_question=ask_question,chat_model=chat_model)
    else:
        raise ValueError
    
    return record

if __name__ == "__main__":
    args = get_args()
    print(args)

    import datetime

    # 获取当前时间
    current_time = datetime.datetime.now()

    args.time = current_time.strftime("%m%d-%H:%M")
    print("格式化后的当前时间:", args.time)

    os.environ["CUDA_VISIBLE_DEVICES"]=args.gpu

    if "deepseek" in args.model:
        chat_model = DeepSeek_API(model=args.model)
    elif "Qwen" in args.model: 
        chat_model = Qwen(model=args.model) 
    elif args.model == "zhipu":
        chat_model = Zhipu()
    elif args.model == "doubao":
        chat_model = Doubao()
    elif args.model == "deepcoder":
        chat_model = deepcoder()
    else:
        raise ValueError

    input_list = [args.dataset]
    for file_name in input_list:
        input_file = 'new_datasets/' + file_name + ".jsonl"
        output_file = "results_Arrmay_Rebuttal/" +args.model + "/" +args.algo + "/"+ file_name + "_"+ args.log + "_(sam)" + str(args.sample) + "_" + args.time +".jsonl"
        # if args.sample == True:

        # if args.final == True:
        #     output_file = "results_final/" +args.model + "/" +args.algo + "/"+ file_name + "_"+ args.algo + "_"+ args.time +".jsonl"
        # elif args.sample == False and "trap" not in args.dataset.lower():
        #     output_file = "results120/" +args.model + "/" +args.algo + "/" + file_name + "_"+ args.algo + "_"+ args.time +".jsonl"
        # else:
        #     if args.log !=None:
        #         output_file = "results_sample120/"+ args.log + "/" +args.model + "/" +args.algo + "/"+ file_name + "_"+ args.algo + "_"+ args.time +".jsonl"
        #     else:
        #         output_file = "results_sample120/" +args.model + "/" +args.algo + "/"+ file_name + "_"+ args.algo + "_"+ args.time +".jsonl"

        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        f_out = open(output_file, 'w')
        data = []
        # print(file_name)
        with open(input_file, 'r') as jsonl_file:
            for line in jsonl_file:
                data.append(json.loads(line.strip()))

        if args.sample != -1 and len(data) > args.sample:
            sampled_data = random.sample(data,args.sample)
        else:
            sampled_data = data

        ans=[]
        # print(data)
        for idx, line in tqdm.tqdm(enumerate(sampled_data), total=len(sampled_data)):
            if "contra" in file_name:
                ask_question = line['New']
                target = None
            elif "mathtrap" in file_name.lower() or "missing" in file_name:
                ask_question = line['Question']
                target = None
            else: #ID
                ask_question = line['Question']
                target = line['target']
            try:

                set_timeout(300)
                record = solve(args,ask_question,chat_model=chat_model)

                try:
                    record['id'] = line['id']
                except:
                    record['id'] = idx
                record['question'] = ask_question
                record['target'] = target
                if "mathtrap" in file_name.lower():
                    record['category'] = line['category']
            except TimeoutError as e:
                print(e)
            finally:
                signal.alarm(0)

            print(record)
            try:
                f_out.write(json.dumps(record, ensure_ascii=False) + '\n')
            except:
                pass
