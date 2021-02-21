# I am pretty sure that the code could to be make shorter and simpler, but my purpose this time was just to create my first python script to upload. 
# I am aware of the very basic concepts of programming (variables, loops, statements, data types & structures...) which is the lowest level in
# programming. My aim with python is just the same as with bash: to be able to make solutions for automation...


import random
user_input = input("Let's play, (R)ock || (P)aper || (S)cissors: ")
rock = ""
paper = ""
scissors = ""
m_rock = ""                 # machine_rock
m_paper = ""                # machine_paper
m_scissors = ""             # machine_scissors

random = random.randint(1, 3)

if user_input.lower() == "r":
    rock = 1
elif user_input.lower() == "p":
    paper = 2
elif user_input.lower() == "s":
    scissors = 3
else:
    print("You mistyped!")

if random == 1:
    m_rock = 1
elif random == 2:
    m_paper = 2
else:
    m_scissors = 3


def result():
    if rock and m_rock or paper and m_paper or scissors and m_scissors:
        print("50-50!")
    elif rock and m_paper or paper and m_scissors or scissors and m_rock:
        print("You lose!")
    elif rock and m_scissors or paper and m_rock or scissors and m_paper:
        print("You win!")


result()
