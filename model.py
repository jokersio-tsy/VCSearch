import tqdm
import json
from openai import OpenAI
import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM
from zhipuai import ZhipuAI
import torch
import requests
import os

class DeepSeek_API():
    """
    A class to interact with the ChatGLM4 API.
    """
    def __init__(self, model="deepseekv3"):
        self.apikey =  "" # your API
        if model == "deepseekv3":
            self.model = "deepseek-chat"
        elif model == "deepseekr1":
            self.model = "deepseek-reasoner"
        self.client = OpenAI(api_key=self.apikey, base_url="https://api.deepseek.com/v1")

    def chat(self, my_prompt):
        """
        Send a prompt to the ChatGLM4 API and return the response.
        """
        response = self.client.chat.completions.create(
        model=self.model,
        messages=my_prompt,
        temperature=0
    )

        return response.choices[0].message.content

class deepcoder():
    def __init__(self):
        path = "" # your path
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.bfloat16).cuda()

    def chat(self, my_prompt):
        inputs = self.tokenizer.apply_chat_template(my_prompt, add_generation_prompt=True, return_tensors="pt").to(self.model.device)
        
        attention_mask = inputs.ne(self.tokenizer.pad_token_id).long()
        # tokenizer.eos_token_id is the id of <|EOT|> token
        outputs = self.model.generate(inputs, max_new_tokens=512, do_sample=False, top_k=50, top_p=0.95, num_return_sequences=1, eos_token_id=self.tokenizer.eos_token_id,pad_token_id=self.tokenizer.eos_token_id,attention_mask=attention_mask)
        response = self.tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
        return response

class Qwen():
    def __init__(self, model):
        # /data1/tiansy/model_download/Qwen/Qwen2___5-Coder-7B-Instruct/
        if model == "Qwen7b":
            self.model_name = "" # your path
        elif model == "Qwen3b":
            self.model_name = "" # your path
        elif model == "Qwen1.5b":
            self.model_name = "" # your path
        else:
            raise ValueError
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def chat(self, my_prompt):
        
        text = self.tokenizer.apply_chat_template(
            my_prompt,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_length = 3000,
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        # print(type(response.choices[0].message))
        return response

class Zhipu():
    def __init__(self):
        self.api = "" # your API
        self.client = ZhipuAI(api_key=self.api)
        self.model = "glm-4-plus"


    def chat(self, my_prompt):
        """
        Send a prompt to the ChatGLM4 API and return the response.
        """
        response = self.client.chat.completions.create(
        model=self.model,
        messages=my_prompt,
        do_sample=False
    )
        
        # print(type(response.choices[0].message))
        return response.choices[0].message.content
    
class Doubao():
    def __init__(self):
        self.api = "" # your API
        self.client = OpenAI(
            api_key = self.api,
            base_url = "https://ark.cn-beijing.volces.com/api/v3",
        )
        self.model = "ep-20250109204609-srtr5"


    def chat(self, my_prompt):
        """
        Send a prompt to the ChatGLM4 API and return the response.
        """
        response = self.client.chat.completions.create(
        model=self.model,
        messages=my_prompt
    )
        return response.choices[0].message.content
    
