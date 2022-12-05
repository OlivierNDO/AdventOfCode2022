"""
--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?


stack_dict = {1 : ['N', 'Z'],
              2 : ['D', 'C', 'M'],
              3 : ['P']}

stack_dict

instr = ['move 1 from 2 to 1', 'move 3 from 1 to 3', 'move 2 from 2 to 1', 'move 1 from 1 to 2']



--- Part Two ---
As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?

"""
# Import packages

import re

# Read input data
with open('D:/aoc/crates.txt') as f:
    d = [x.replace('\n', '') for x in f.readlines()]
    
    
# Define functions
def split_string_into_chunks(instr : str, n : int):
    return [instr[i:i+n] for i in range(0, len(instr), n)]
    

def get_digits_from_instructions(instructions : str,
                                 regex = r"move\s+(\d*\.*?\d+)\s+from\s+(\d*\.*?\d+)\s+to\s+(\d*\.*?\d+)"):
    return [int(x) for x in re.findall(regex, instructions)[0]]


def change_stacks(stacks : dict, n : int, from_x : int, to_y : int, crate_mover = 9000):
    """Change stack dictionary by moving <n> items from <from_x> key to <to_y> key"""
    # Identify crates to move
    move_crates = stacks[from_x][:n]
    
    # Add new new position
    if crate_mover == 9000:
        for mc in move_crates:
            stacks[to_y] = [mc] + stacks[to_y]
    else:
        stacks[to_y] = move_crates + stacks[to_y]
        
        
    # Remove from old position
    stacks[from_x] = stacks[from_x][n:]
    return stacks


### Part 1

# Create initial stack dictionary
crates = d[0:9]   
    
stack_nums = [int(x[:-1].replace(' ', '')) for x in split_string_into_chunks(instr = d[8], n = 4)]
stack_dict = dict(zip(stack_nums, [[] for _ in range(len(stack_nums))]))
for i, sn in enumerate(stack_nums):
    crates_i = [x[:-1].replace('[', '').replace(']', '') for x in split_string_into_chunks(instr = crates[i], n = 4)]
    for j, ci in enumerate(crates_i):
        stack_dict[stack_nums[j]].append(ci)
        
for sn in stack_nums:
    stack_dict[sn] = stack_dict[sn][:-1]
    stack_dict[sn] = [x for x in stack_dict[sn] if len(x.replace(' ', '')) > 0]


# Create instruction set and move crates
instr = d[10:]
instr_dicts = []
for move_instr in instr:
    n, from_x, to_y = get_digits_from_instructions(move_instr)
    stack_dict = change_stacks(stack_dict, n, from_x, to_y, crate_mover = 9000)
    
top_of_stacks = ''.join([stack_dict[k][0] for k in list(stack_dict.keys())])

print(f'Part 1 answer: {top_of_stacks}')



### Part 2
# Create initial stack dictionary
crates = d[0:9]   
    
stack_nums = [int(x[:-1].replace(' ', '')) for x in split_string_into_chunks(instr = d[8], n = 4)]
stack_dict = dict(zip(stack_nums, [[] for _ in range(len(stack_nums))]))
for i, sn in enumerate(stack_nums):
    crates_i = [x[:-1].replace('[', '').replace(']', '') for x in split_string_into_chunks(instr = crates[i], n = 4)]
    for j, ci in enumerate(crates_i):
        stack_dict[stack_nums[j]].append(ci)
        
for sn in stack_nums:
    stack_dict[sn] = stack_dict[sn][:-1]
    stack_dict[sn] = [x for x in stack_dict[sn] if len(x.replace(' ', '')) > 0]


# Create instruction set and move crates
instr = d[10:]
instr_dicts = []
for move_instr in instr:
    n, from_x, to_y = get_digits_from_instructions(move_instr)
    stack_dict = change_stacks(stack_dict, n, from_x, to_y, crate_mover = 9001)
    
top_of_stacks = ''.join([stack_dict[k][0] for k in list(stack_dict.keys())])

print(f'Part 2 answer: {top_of_stacks}')


