import re
import copy
from z3 import *

def extract_solver_add_content(text):
    # 正则表达式匹配 solver.add(
    pattern = r'solver\.add\('
    start_match = re.search(pattern, text)
    
    if not start_match:
        return None
    
    start_index = start_match.end()  # 获取开始位置
    depth = 1  # 初始化括号深度
    end_index = start_index  # 初始化结束位置

    # 遍历字符串，查找括号
    while end_index < len(text):
        if text[end_index] == '(':
            depth += 1
        elif text[end_index] == ')':
            depth -= 1
        
        if depth == 0:  # 如果深度回到0，表示找到匹配的括号
            break
        
        end_index += 1

    if depth == 0:
        return text[start_index:end_index]
    else:
        return None  # 如果没有找到匹配的括号


def break_down_response(reply,initial = False):
    reply_lst = reply.split("\n")
    con_code = set()
    var_code = set()
    return_code = []    

    for con in reply_lst:
        if "solver.add" in con.lower():
            con = extract_solver_add_content(con)
            if con!= None and "int" in con.lower():
                continue
            con_code.add("solver.add({})".format(con))
        elif "Real(" in con:
            con_tmp = re.search(r"(\w+\s*=\s*Real\('\w+'\))", con)
            if con_tmp != None:
                con_var = re.search(r"(\w+)\s*=", con)
                var_code.add(con_var.group(1))
        elif "Int(" in con:
            con_tmp = re.search(r"(\w+\s*=\s*Int\('\w+'\))", con)
            if con_tmp != None:
                con_var = re.search(r"(\w+)\s*=", con)
                var_code.add(con_var.group(1))
    con_code = list(con_code)
    var_code = list(var_code)

    if initial == True:
        return_find = False
        for idx,con in enumerate(reply_lst):
            if(return_find == True):
                break
            for j in range(idx,len(reply_lst)):
                con_tmp = reply_lst[j]
                if "return " in con_tmp:
                    print(con_tmp)
                    pattern = r"return\s+`?(\w+[\w_]*?)`?"
                    match = re.search(pattern, con_tmp)
                    if match == None:
                        continue
                    return_code = [match.group(1)]
                    return_find = True
                    break
        if(return_find == False):
            return_code = ""       
        print("return",return_code)
        return var_code,con_code,return_code
        
    return var_code,con_code

def update_con_and_var(existing_cons,existing_vars,add_var,add_cons,head_cons):
        candidate_cons = copy.deepcopy(existing_cons)
        candidate_vars = copy.deepcopy(existing_vars)
        for con in head_cons:
            candidate_cons.discard(con)
        for con in add_cons:
            candidate_cons.add(con)
        for var in add_var:
            candidate_vars.add(var)
        return candidate_cons,candidate_vars

def get_variable_from_constrains(input_str):
    match = re.search(r'solver\.add\(([^)]+)\)', input_str)
    if match:
        expression = match.group(1)  # 获取括号内的内容
        # 提取变量
        variables = re.findall(r'\b[a-zA-Z_]\w*\b', expression)
        return variables
    return None

def break_refine_response(reply,tag = "<SOS>"):
    tag_index = reply.find("<SOS>")

    if tag_index != -1:
        reply = reply[tag_index + len("<SOS>"):].strip()

    reply_lst = reply.split("\n")
    con_code = set()
    var_code = set()   

    for con in reply_lst:
        if "solver.add" in con.lower():
            con = extract_solver_add_content(con)
            if con!= None and "int" in con.lower():
                continue
            con_code.add("solver.add({})".format(con))
            new_var = get_variable_from_constrains("solver.add({})".format(con))
            for var in new_var:
                var_code.add(var)
    con_code = list(con_code)
    var_code = list(var_code)


def candidate_reply2node(head,reply):
    reply_lst = reply.split("\n")
    son_lst = []

    for rep in reply_lst:
        match = re.search(r'<SOS>(.*?)<EOS>', rep)
        if match:
            new_var = match.group(1).strip()
            if new_var in head.visited_variable:
                continue
            son = copy.deepcopy(head)
            son.update_son(new_var)
            son_lst.append(son)
    return son_lst

def get_code_format(variable,constrains,aim):
    variable = list(variable)
    constrains = list(constrains)

    final_code_lst = []
    for var in variable:
        final_code_lst.append("    {} = Real('{}')".format(var.strip(),var.strip()))
    for con in constrains:
        final_code_lst.append("    {}".format(con.strip()))
    try:
        final_code_lst.append("    return {},solver".format(aim))
    except:
        pass # returns = none

    return ["from z3 import *",'def solution():','    solver = Solver()'] + final_code_lst + ["ans, solver = solution()", "result = solver.check()"] 

def execude_code(code):
    # print(code)
    envs = {}
    solve_code = []
    for c in code:
        if c.strip() == "```python": continue
        if c.strip() == "```": continue
        solve_code.append(c)
    # print(solve_code)
    exec('\n'.join(solve_code), envs)
    # sat_check = eval("solver.check()", envs) 
    # print(sat_check)
    if eval("solver.check()", envs) != sat: 
        return "UnSAT"
    
    solve_code.append("model = solver.model()")
    exec('\n'.join(solve_code), envs)
    ans = eval("model[ans]", envs)
    # print(ans)
    exec(f'solver.add({ans} != ans)', envs)
    if eval("solver.check()", envs) == sat: 
        return "Multi"
    return float(ans.as_fraction())

def lst2str(l):
    l = list(l)
    return "\n".join(l)

def my_filter(cons,head_variable):
    cons = list(cons)
    new_cons = []

    for con in cons:
        if head_variable in con:
            new_cons.append(con)
    return new_cons


def replace_return(code_list):
    last_real_var = None
    for line in code_list:
        if " = Real(" in line:
            last_real_var = line.split('=')[0].strip()

    # 替换return语句
    for i in range(len(code_list)):
        if code_list[i].startswith('    return'):
            code_list[i] = f'    return {last_real_var},solver'

    return code_list