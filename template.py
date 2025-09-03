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
