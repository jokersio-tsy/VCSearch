Z3_impossible_TEMPLATE = {
    "system": "You are a helpful assistant that can write Python code and Z3 library that solves mathematical reasoning questions similarly to the examples that you will be provided.\
        You only need to write a function named solution() with two return values: a variable representing the answer and the Z3 solver\
        please write as the giving example",
    "expr": "solution()",
    "prompt": '''Q: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?

def solution():
    solver = Solver()

    """Olivia has $23. She bought five bagels for $3 each. How much money does she have left?"""
    initial_money = Real('initial_money')
    total_cost = Real('total_cost')
    money_left = Real('money_left')
    bagels = Int('bagels')
    bagel_cost = Real('bagel_cost')

    """Olivia has $23. She bought five bagels for $3 each. How much money does she have left?"""
    solver.add(bagels == 5)
    solver.add(bagel_cost == 3)
    solver.add(initial_money == 23)
    solver.add(total_cost == bagels * bagel_cost)
    solver.add(money_left == initial_money - total_cost)

    """How much money does she have left?"""
    return money_left, solver



Q: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?

def solution():
    solver = Solver()
    
    """Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?"""
    initial_golf_balls = Int('initial_golf_balls')
    lost_on_tuesday = Int('lost_on_tuesday')
    lost_on_wednesday = Int('lost_on_wednesday')
    total_golf_balls = Int('total_golf_balls')
    
    """Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?"""
    solver.add(initial_golf_balls == 58)
    solver.add(lost_on_tuesday == 23)
    solver.add(lost_on_wednesday == 2)
    solver.add(total_golf_balls == initial_golf_balls - lost_on_tuesday - lost_on_wednesday)
    
    """How many golf balls did he have at the end of wednesday?"""
    return total_golf_balls, solver





Q: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?

def solution():
    solver = Solver()
    
    """There were nine computers in the server room. Some more computers were installed each day, from monday to thursday. How many computers are now in the server room?"""
    initial_computers = Int('initial_computers')
    daily_installed = Int('daily_installed')
    total_days = Int('total_days')
    total_computers = Int('total_computers')

    """There were nine computers in the server room. Some more computers were installed each day, from monday to thursday. How many computers are now in the server room?"""
    solver.add(initial_computers == 9)
    solver.add(daily_installed >= 0) # no detailed information, give a loose constraint
    solver.add(total_days == 0)  # from Monday to Thursday
    solver.add(total_computers == initial_computers + daily_installed * total_days)

    """How many computers are now in the server room?"""
    return total_computers, solver





Q: Shawn has five toys. For Christmas, he got some toys each from his mom and dad. How many toys does he have now?

def solution():
    solver = Solver()
    
    """Shawn has five toys. For Christmas, he got some toys each from his mom and dad. How many toys does he have now?"""
    initial_toys = Int('initial_toys')
    toys_from_mom = Int('toys_from_mom')
    toys_from_dad = Int('toys_from_dad')
    total_toys = Int('total_toys')

    """Shawn has five toys. For Christmas, he got some toys each from his mom and dad. How many toys does he have now?"""
    solver.add(initial_toys == 5)
    solver.add(toys_from_mom >= 0)   # no detailed information, give a loose constraint
    solver.add(toys_from_mom >= 0)   # no detailed information, give a loose constraint
    solver.add(total_toys == initial_toys + toys_from_mom + toys_from_dad)

    """How many toys does he have now?"""
    return total_toys, solver





Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?

def solution():
    solver = Solver()
    
    """Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?"""
    initial_lollipops = Int('initial_lollipops')
    lollipops_left = Int('lollipops_left')
    lollipops_given = Int('lollipops_given')

    """Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?"""
    solver.add(initial_lollipops == 20)
    solver.add(lollipops_left == 12)
    solver.add(lollipops_given == initial_lollipops - lollipops_left)

    """How many lollipops did Jason give to Denny?"""
    return lollipops_given, solver





Q: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?

def solution():
    solver = Solver()
    
    """Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?"""
    chocolates_leah = Int('chocolates_leah')
    chocolates_sister = Int('chocolates_sister')
    chocolates_eaten = Int('chocolates_eaten')
    chocolates_left = Int('chocolates_left')

    """Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?"""
    solver.add(chocolates_leah == 32)
    solver.add(chocolates_sister == 42)
    solver.add(chocolates_eaten == 35)
    solver.add(chocolates_left == chocolates_leah + chocolates_sister - chocolates_eaten)

    """How many pieces do they have left in total?"""
    return chocolates_left, solver


Q: {question}
# solution in Python:
from z3 import *
'''.strip() + '\n\n\n'
}

    # At last, conclude all the constraints with 'All refine related constraints:'\
SMT_align_TEMPLATE = {
    "system": "You are a helpful assistant that can write Python code and Z3 library that solves mathematical reasoning questions.\
        Now I will provide you with the already written variables ,constraints, questions and some similar examples. Please improve them to ensure that the variables conform to real-world regulations.\
    I hope you can perform the following two actions for each of the previously defined variables:\
    1. Check for any missing knowledge that has not been extracted.\
    2. Verify that the existing constraints are accurate and comprehensive.\
    new constraints should not contains new variables!\
    Please answer like given example format.",
    "expr": "solution()",
    "prompt": '''    
    Q: Josh decides to try flipping a house. He buys a house for $80,000 and then puts in $50,000 in repairs. This increased the value of the house by 150%, but the market value of the house after repairs is only $100,000. How much profit did he make?
    variables: 
    initial_cost = Real('initial_cost')
    repair_cost = Real('repair_cost')
    increased_value_percentage = Real('increased_value_percentage')
    market_value_after_repairs = Real('market_value_after_repairs')
    total_investment = Real('total_investment')
    expected_value = Real('expected_value')
    profit = Real('profit')
    Constrains:
    solver.add(initial_cost == 80000)
    solver.add(repair_cost == 50000)
    solver.add(increased_value_percentage == 1.5)  # 150% increase
    solver.add(market_value_after_repairs == 100000)
    solver.add(total_investment == initial_cost + repair_cost)
    solver.add(expected_value == initial_cost * (1 + increased_value_percentage))
    solver.add(profit == market_value_after_repairs - total_investment)
    A:
    Let's consider the problem again.
    For "initial_cost":
    existing constraint - 
    solver.add(initial_cost == 80000)  
    solver.add(total_investment == initial_cost + repair_cost)
    1. there is no misssing knowledge.
    2. there is no missing constrants.
    Refine related constrains:
    solver.add(initial_cost == 80000)  
    solver.add(total_investment == initial_cost + repair_cost)    

    For "repair_cost":
    existing constraint - 
    solver.add(repair_cost == 50000)
    solver.add(total_investment == initial_cost + repair_cost)
    1. there is no misssing knowledge.
    2. there is no missing constrants.
    Refine related constrains:
    solver.add(repair_cost == 50000)
    solver.add(total_investment == initial_cost + repair_cost)
    
    For "increased_value_percentage":
    existing constraint
    solver.add(increased_value_percentage == 1.5)  # 150% increase
    solver.add(expected_value == initial_cost * (1 + increased_value_percentage))
    1. there is no misssing knowledge.
    2. in this case the increased_value_percentage should be adjust to 0.5 as the expected_value == initial_cost * (1 + increased_value_percentage)
    Refine related constrains:
    solver.add(increased_value_percentage == 0.5)  # 150% increase
    solver.add(expected_value == initial_cost * (1 + increased_value_percentage))   


    For "market_value_after_repairs":
    existing constraint - 
    solver.add(market_value_after_repairs == 100000)
    solver.add(profit == market_value_after_repairs - total_investment)
    1. there is no misssing knowledge.
    2. there is no missing constrants.
    Refine related constrains:
    solver.add(market_value_after_repairs == 100000)
    solver.add(profit == market_value_after_repairs - total_investment)

    For "total_investment":
    existing constraint - 
    solver.add(total_investment == initial_cost + repair_cost)
    solver.add(profit == market_value_after_repairs - total_investment)
    1. the total_investment should be a positve number, as align with the real world. we can add:
    solver.add(total_investment >= 0)
    2. there is no missing constrants.
    Refine related constrains:
    solver.add(total_investment == initial_cost + repair_cost)
    solver.add(profit == market_value_after_repairs - total_investment)
    solver.add(total_investment >= 0)


    For "expected_value":
    existing constraint - 
    solver.add(expected_value == initial_cost * (1 + increased_value_percentage))
    1. the expected_value should be a positve number, as align with the real world. we can add:
    solver.add(expected_value >= 0)
    2. in this problem expected_value and market_value_after_repairs is the same thing, we can add
    solver.add(expected_value == market_value_after_repairs)
    Refine related constrains:
    solver.add(expected_value == initial_cost * (1 + increased_value_percentage))
    solver.add(expected_value >= 0)
    solver.add(expected_value == market_value_after_repairs)

    For "profit":
    existing constraint:
    solver.add(profit == market_value_after_repairs - total_investment)
    1. the profit should be a positve number, as align with the real world. we can add:
    solver.add(profit >= 0)
    2. there is no missing constrants. 
    Refine related constrains:
    solver.add(profit == market_value_after_repairs - total_investment)
    solver.add(profit >= 0)
    
    All refine related constraints:
    solver.add(initial_cost == 80000)  
    solver.add(total_investment == initial_cost + repair_cost)   
    solver.add(repair_cost == 50000)
    solver.add(total_investment == initial_cost + repair_cost)
    solver.add(increased_value_percentage == 0.5)  # 150% increase
    solver.add(expected_value == initial_cost * (1 + increased_value_percentage))   
    solver.add(market_value_after_repairs == 100000)
    solver.add(profit == market_value_after_repairs - total_investment)
    solver.add(total_investment == initial_cost + repair_cost)
    solver.add(profit == market_value_after_repairs - total_investment)
    solver.add(total_investment >= 0)
    solver.add(expected_value == initial_cost * (1 + increased_value_percentage))
    solver.add(expected_value >= 0)
    solver.add(expected_value == market_value_after_repairs)
    solver.add(profit == market_value_after_repairs - total_investment)
    solver.add(profit >= 0)



    Q: {question}
    variables: 
    {variables}
    Constrains:
    {constrains}
    A:Let's consider the problem again.
    '''

}

def get_answer_number(msg: str):
    msg = msg.replace(",", "").strip()
    msg = msg.split("The answer is")[-1]
    msg = [s.replace(",", "") for s in re.findall(r'-?\d+/?\.?\d*', msg)]
    ans = []
    for x in msg:
        try:
            parts = x.strip().split(".")
            if len(parts) == 1:
                ans.append(int(parts[0]))
            else:
                if parts[1] == "".join(['0'] * len(parts[1])):
                    ans.append(int(parts[0]))
                else:
                    ans.append(float(x))
        except: pass
    if len(ans) == 0: return None
    return ans[-1]

CoT_MATH_TEMPLATE = {
    "system": "You're an experienced elementary school teacher, and I'm now expecting you to solve some math problems. \
        If you find these problems unsolvable, please output “this is unsolvable”. If not, follow the given examples and answer the question.",
    "expr": get_answer_number,
    "prompt": '''Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?
A: There are 15 trees originally. Then there were 21 trees after the Grove workers planted some more. So there must have been 21 - 15 = 6 trees that were planted. The answer is 6.

Q: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?
A: There are originally 3 cars. Then 2 more cars arrive. Now 3 + 2 = 5 cars are in the parking lot. The answer is 5.

Q: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?
A: Originally, Leah had 32 chocolates and her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39 pieces left in total. The answer is 39.

Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?
A: Jason had 20 lollipops originally. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8 lollipops. The answer is 8.

Q: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?
A: Shawn started with 5 toys. He then got 2 toys each from his mom and dad. So he got 2 * 2 = 4 more toys. Now he has 5 + 4 = 9 toys. The answer is 9.

Q: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?
A: There were originally 9 computers. For each day from monday to thursday, 5 more computers were installed. So 4 * 5 = 20 computers were added. Now 9 + 20 = 29 computers are now in the server room. The answer is 29.

Q: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?
A: Michael started with 58 golf balls. He lost 23 on Tuesday, and lost 2 more on wednesday. So he had 58 - 23 = 35 at the end of Tuesday, and 35 - 2 = 33 at the end of wednesday. The answer is 33.

Q: Olivia has $23. She bought five bagels for $3 each. How much money does she have left? 
A: Olivia had 23 dollars. She bought 5 bagels for 3 dollars each. So she spent 5 * 3 = 15 dollars. Now she has 23 - 15 = 8 dollars left. The answer is 8.

Q: {question}\nA:
'''.strip(),
}