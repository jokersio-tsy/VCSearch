from z3 import *
from collections import deque
import re
from VCSearch_utils import *
from collections import Counter
from template import Z3_impossible_TEMPLATE

def get_ans(variable,constains,aim):        
    
    code_lst = get_code_format(variable=variable,constrains=constains,aim=aim)

    try:
        ans = execude_code(code_lst)
    except:
        ans = "Error"

    print("###ans",ans)
    return ans


def get_initial_stage(ask_question,chat_model):
    System_prompt_str = Z3_impossible_TEMPLATE['system']
    question_prompt_str = Z3_impossible_TEMPLATE['prompt'].format(question=ask_question)

    System_prompt = {'role':"system","content":System_prompt_str}
    question_prompt = {'role':"user","content":question_prompt_str}

    message = [System_prompt,question_prompt]

    reply = chat_model.chat(message)
    print("###initial###",reply)

    variable,constrains,returns = break_down_response(reply,initial=True)

    return variable,constrains,returns,reply

def get_nxt_action_prompt(question,head,existing_con,constrain_head):
    System_prompt = {'role':"system","content":get_nxt_action_prompt_TWMPLATE['system']}
    user_prompt = {'role':"user","content":get_nxt_action_prompt_TWMPLATE['prompt'].format\
                   (question = question, head= head , constrain = existing_con, constrain_head=constrain_head)}
    message = [System_prompt,user_prompt]
    return message

def judge(question,head,cons1,cons2,chat_model,cans1,cans2):
    System_prompt = {'role':"system","content":LLM_judge_TEMPLATE['system']}
    user_prompt = {'role':"user","content":LLM_judge_TEMPLATE['prompt'].format\
                     (question = question, head = head, cons1 = cons1 ,cons2 = cons2,\
                        cans1 = cans1, cans2 = cans2)}
    message = [System_prompt,user_prompt]
    
    reply = chat_model.chat(message)
    # print("@@@ judge reply")
    # print(reply)

    if "set2 is better" in reply.lower():
        return True
    elif "set1 is better" in reply.lower():
        return False
    else:
        print("con't judge")
        return False

def search(ask_question,variants,aim,chat_model,constrains):
    
    queue = deque(variants)

    visited_variable = set()
    existing_variable = set(variants)
    existing_con = set(constrains)
    candidate_ans = get_ans(variable=variants,constains=existing_con,aim=aim)
    ans_lst = [candidate_ans]
    if candidate_ans == "Error":
        candidate_ans = "Multi"
        existing_con = set()

    while queue:
        head_node = queue.popleft()  

        if head_node in visited_variable:
            continue

        visited_variable.add(head_node)
        head_constrains = my_filter(cons=existing_con,head_variable =head_node)
        message = get_nxt_action_prompt(question=ask_question,head=head_node,existing_con=lst2str(existing_con),\
                                        constrain_head=lst2str(head_constrains))
        reply = chat_model.chat(message)
        add_var,add_con = break_down_response(reply)
        print("@@@nxt reply",reply)
        print("@@@addvar",add_var)
        print("@@@addcon",add_con)

        candidate_cons,candidate_vars = update_con_and_var(existing_cons=existing_con,existing_vars=existing_variable,head_cons=head_constrains,add_var=add_var,add_cons=add_con)

        ans = get_ans(variable=variants,constains=candidate_cons,aim=aim)
        
        if ans == "Error":
            continue
        ans_lst.append(ans)
        if candidate_ans != ans:
            valid_result = judge(question=ask_question,head = head_node,chat_model=chat_model,\
                                 cons1=lst2str(my_filter(cons=existing_con,head_variable =head_node)), cans1=candidate_ans,\
                                    cons2=lst2str(my_filter(cons=candidate_cons,head_variable =head_node)), cans2=ans)
            print("###Judge results:",valid_result)
            if valid_result == True: # tihuan
                print("!!!ans update!")
                existing_con = candidate_cons
                existing_variable = candidate_vars
                candidate_ans = ans
                for var in add_var:
                    queue.append(var)
            else:
                pass

    return candidate_ans,ans_lst

def solve_VCSearch_each(ask_question,chat_model):
    variable,constrains,returns,initial_reply = get_initial_stage(ask_question,chat_model=chat_model)
    print("variable:",variable)
    try:
        aim = returns[0]
        print("aims",aim)
    except:
        return {'ans':"ERROR","question":ask_question}
    

    ans,ans_lst = search(ask_question=ask_question,variants=variable,chat_model=chat_model,aim=aim,constrains=constrains)

    count = Counter(ans_lst)  
    most_common_ans = count.most_common(1)[0][0]

    record = {'ans':ans,'most_ans':most_common_ans,'ans_lst':ans_lst,'question':ask_question}
    return record


# prompt

get_nxt_action_prompt_TWMPLATE ={
    'system':"You are a helpful assistant that can write Python code and Z3 library that solves mathematical reasoning questions.\
        Please note that the syntax of Z3 is NOT exactly the same as that of Python. There are NO like “//”, min, max, IF etc. in Z3 constraints.",
    "prompt": '''
    I have previously asked you to write Z3 constraints for a problem. However, the current set of constraints for the variable may have omissions or errors. \
    I would like you to review it from the following two aspects and make appropriate modifications if necessary:
    1. Based on the problem description, consider whether the current constraints accurately capture the problem.
    2. Add constraints based on real-world knowledge, considering whether there are any missing modeling statements, such as the quantity of items should be >= 0, or the relationships between the sides of a triangle. 
    Please note that you only need to add constraints to the CURRENT HEAD VARIABLE; in other words, the new constraints MUST include the head variable! 
    You can first provide your thought process, and then write the new constraints that include the head variable after the identifier <SOS>

    You can follow the example:
    Question: Josh decides to try flipping a house. He buys a house for $80,000 and then puts in $50,000 in repairs. This increased the value of the house by 150%, but the market value of the house after repairs is only $100,000. How much profit did he make?
    Existing Constraints: 
    solver.add(initial_cost == 80000)  
    solver.add(total_investment == initial_cost + repair_cost)   
    solver.add(repair_cost == 50000)
    solver.add(increased_value_percentage == 0.5)  # 150% increase
    solver.add(expected_value == initial_cost * (100 + increased_value_percentage))   
    solver.add(market_value_after_repairs == 100000)
    solver.add(total_investment >= 0)
    solver.add(profit == market_value_after_repairs - total_investment)
    solver.add(profit >= 0)       
    solver.add(expected_value >= 0)
    Now head variable: expected_value
    Now existing constrains with head variable:
    solver.add(expected_value == initial_cost * (100 + increased_value_percentage))  
    solver.add(expected_value >= 0)
    Answer:
    
    1. For the constraint expected_value == initial_cost * (100 + increased_value_percentage), the equation for expected_value in the problem should be initial_cost * (1 + increased_value_percentage). Therefore, this constraint should be modified to solver.add(expected_value == initial_cost * (1 + increased_value_percentage)).

    2. For the constraint solver.add(expected_value >= 0) aligns with real-world requirements. Additionally, since expected_value is an unknown variable, it is appropriate to add real-world constraints, so this should be retained.

    3. Furthermore, expected_value and market_value_after_repairs refer to the same entity in the problem, so a constraint should be added: market_value_after_repairs == expected_value.

    <SOS>
    So, new Constraints with head variable is 
    solver.add(expected_value == initial_cost * (1 + increased_value_percentage))
    solver.add(expected_value >= 0)
    solver.add(expected_value == market_value_after_repairs)

    
    
    Question:{question}
    Existing Constraints:{constrain}
    Now head variable:{head}
    Now existing constrains with head variable:{constrain_head}
    Answer:
'''
}


LLM_judge_TEMPLATE = {
    'system': "You are a helpful assistant that can write Python code and Z3 library that solves mathematical reasoning questions.",
    "prompt": '''Please judge which set of constraints is better for the given problem, including all constraints of variable "X".
    Problem: {question}
    variable:{head}
    Constrains set1:{cons1}
    Constrains set1 ans:{cans1}
    Constrains set2:{cons2}
    Constrains set2 ans:{cans1}
    Please write down your thinking process first, and finally output, "I think Constrains set1 is better", or "I think Constrains set2 is better"
'''    
}