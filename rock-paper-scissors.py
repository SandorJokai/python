# I am pretty sure that the code could be make shorter and more simpler, but my purpose this time was just create my first python script to upload. 
# I am aware of the very basic concepts of programming (variables, loops, statements, data types & structures...) which is the lowest level in
# programming. My aim with python is just the same as with bash: to be able to make solutions for automation...


import random
user_input = input("Let's play, rock || paper || scissors: ")
rock = ""
paper = ""
scissors = ""
m_rock = ""                 # machine_rock
m_paper = ""                # machine_paper
m_scissors = ""             # machine_scissors

random = random.randint(1, 3)

if user_input == "rock":
    rock = 1
elif user_input == "paper":
    paper = 2
elif user_input == "scissors":
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
    if rock and m_rock:
        print("50-50!")
    elif rock and m_paper:
        print("You lose!")
    elif rock and m_scissors:
        print("You win!")
    elif paper and m_rock:
        print("You win!")
    elif paper and m_paper:
        print("50-50!")
    elif paper and m_scissors:
        print("You lose!")
    elif scissors and m_rock:
        print("You lose!")
    elif scissors and m_paper:
        print("You win!")
    elif scissors and m_scissors:
        print("50-50!")


result()
