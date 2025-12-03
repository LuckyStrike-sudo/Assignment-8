#Caedmon Boutwell 1001988638
import numpy as np

def read_file(file):
    arr = []
    f = open(file, 'r')
    for i in f:
        temp = i.split(",")
        arr.append(temp)

    return arr

def eta(N):
    return 20/(19+N)

def f_function(Q, N, Ne, s):
    x, y = s
    max_action = None
    val_up, val_down, val_left, val_right = 0
    if (s, "up") in Q:
        if N[s, "up"] < Ne:
            val_up = 1
        else:
            val_up = Q[s, "up"]

    if (s, "down") in Q:
        if N[s, "down"] < Ne:
            val_down = 1
        else:
            val_val_downup = Q[s, "down"]

    if (s, "left") in Q:
        if N[s, "left"] < Ne:
            val_left = 1
        else:
            val_left = Q[s, "left"]

    if (s, "right") in Q:
        if N[s, "right"] < Ne:
            val_right = 1
        else:
            val_right = Q[s, "right"]
            
    move = max(val_up, val_down, val_left, val_right)
    if move == val_up:
        return "up"
        s_prime = (x, y-1)
    elif move == val_down:
        return "down"
        s_prime = (x, y+1)
    elif move == val_left:
        return "left"
        s_prime = (x+1, y)
    else:
        return "right"
        s_prime = (x-1, y)


def ExecuteAction(a, s):
    



def maxQ():
    
    return 


"""
This should be correct
I need to make sure that the maxQ() function works with the current code. I can test this when I finish the main loop
"""

def Q_Learning_Update(s, r, a, s_prime, r_prime, gamma, eta, Q, N, terminals):
    if s_prime in terminals:
        Q[(s_prime, None)] = r_prime
    if s is not None:
        if (s,a) in N:
            N[(s,a)] += 1
        else:
            N[(s,a)] = 1
        
        c = eta(N[(s,a)])

    if (s,a) not in Q[(s,a)]:
        Q[(s,a)] = 0.0

    Q[(s, a)] = (1-c)*Q[(s,a)] + c(r + gamma*maxQ(Q, s_prime, terminals))
    return

def AgentModel_Q_Learning(environment_file, non_terminal_reward, gamma, number_of_moves, Ne):
    S = np.array(read_file(environment_file))
    print(S)

    world = {}
    Q = {}
    terminals = {}
    N = {}
    #Implements the world
    for i, r in enumerate(S):
        for j, c in enumerate(r):
            c = c.replace(" ", "")
            if c == "I":
                world[(i,j)] = c
            elif c != "." and c != "X":
                world[(i,j)] = float(c)
                terminals[(i,j)] = float(c)
            elif c == ".":
                world[(i,j)] = 0.0
            else:
                world[(i,j)] = c

            N[(i,j), None] = 0

    print(N)

    #Initial values
    s_prime = next(k for k, v in world.items() if v=="I")
    s = None
    r = None
    a = None
    Ne = None

    #Runs until num moves is done
    """
        Need to finish implementing this
        I am unsure what N is and I still need to add the f function
        I also need to adjust the termination criterion and probably the loop
        Make sure we apss the correct number of variables to the Q_Learning_Update function
    """
        
    for i in range(1, number_of_moves):
        r_prime = non_terminal_reward
        Q_Learning_Update(s, r, a, s_prime, r_prime, gamma, )
        if i == 5:
            Ne = N[s, a]
        if s_prime in terminals:
            s_prime = next(k for k, v in world.items() if v=="I")
            s = None
            r = None
            a = None
            Ne = None
        a = f_function(Q, N, Ne)

        

    print(terminals)

    return 