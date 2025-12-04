#Caedmon Boutwell 1001988638
import numpy as np

def read_file(file):
    arr = []
    f = open(file, 'r')
    for i in f:
        temp = i.split(",")
        arr.append(temp)

    return arr

def print_utilites(Q, S):
    for i, r in enumerate(S):
        for j, c in enumerate(r):
            if c == "X":
                print(" 0.000", end= " ")
            else:
                max_utility = max(Q[(i,j), "up"], Q[(i,j), "down"], Q[(i,j), "left"], Q[(i,j), "right"])
                print("%6.3f" % max_utility, end=" ")

def eta(N):
    return 20/(19+N)

def f_function(Q, N, Ne, s):
    x, y = s
    max_action = None
    val_up = 0
    val_down = 0
    val_left = 0
    val_right = 0
    if (s, "up") in Q:
        if (s, "up") in N and N[s, "up"] < Ne:
            val_up = 1
        else:
            val_up = Q[s, "up"]
    else:
        Q[s, "up"] = 0

    if (s, "down") in Q:
        if (s, "down") in N and N[s, "down"] < Ne:
            val_down = 1
        else:
            val_down = Q[s, "down"]
    else:
        Q[s, "down"] = 0

    if (s, "left") in Q:
        if (s, "left") in N and N[s, "left"] < Ne:
            val_left = 1
        else:
            val_left = Q[s, "left"]
    else:
        Q[s, "left"] = 0

    if (s, "right") in Q:
        if (s, "right") in N and N[s, "right"] < Ne:
            val_right = 1
        else:
            val_right = Q[s, "right"]
    else:
        Q[s, "right"] = 0
            
    move = max(val_up, val_down, val_left, val_right)
    if move == val_up:
        return "up"
    elif move == val_down:
        return "down"
    elif move == val_left:
        return "left"
    elif move == val_right:
        return "right"
    else:
        print("ERROR IN F FUNCTION")
        return -1

def ExecuteAction(a, s):
    x, y = s
    match a:
        case "up":
            return (x, y-1)
        case "down":
            return (x, y+1)
        case "left":
            return (x+1, y)
        case "right:":
            return (x-1, y)
        case _:
            print("ERROR EXECUTE ACTION")
            return -1

def maxQ(Q, s, terminals):
    x, y = s
    if ((x-1, y), "up") not in Q:
        Q[(x-1, y), "up"] = 0.0
    if ((x+1, y), "down") not in Q:
        Q[(x+1, y), "down"] = 0.0
    if ((x, y-1), "left") not in Q:
        Q[((x, y-1), "left")] = 0.0
    if ((x, y+1), "right") not in Q:
        Q[((x, y+1), "right")] = 0.0
    
    #Utiltiy of the space to the up
    if ((x-1, y), "up") in Q:
        if Q[(x-1, y), "up"] != "X":
            if (x-1, y) in terminals:
                u_up = terminals[(x-1,y)]
            else:
                u_up = Q[(x-1, y), "up"]
        else:
            u_up = Q[s, "up"]
    else:
        u_up = Q[s, "up"]

    #utility of the sapce left
    if ((x, y-1), "left") in Q:
        if Q[(x, y-1), "left"] != "X":
            if (x, y-1) in terminals:
                u_left = terminals[(x, y-1)]
            else:
                u_left = Q[(x, y-1), "left"]
        else:
            u_left = Q[s, "left"]
    else:
        u_left = Q[s, "left"]
    
    #Utility of the space to the down
    if ((x+1, y), "down") in Q:
        if Q[(x+1, y), "down"] != "X":
            if (x+1, y) in terminals:
                u_down = terminals[(x+1,y)]
            else:
                u_down = Q[(x+1, y), "down"]
        else:
            u_down = Q[s, "down"]
    else:
        u_down = Q[s, "down"]

    #utility of the space right
    if ((x, y+1), "right") in Q:
        if Q[(x, y+1), "right"] != "X":
            if (x, y+1) in terminals:
                u_right = terminals[(x, y-1)]
            else:
                u_right = Q[(x, y+1), "right"]
        else:
            u_right = Q[s, "right"]
    else:
        u_right = Q[s, "right"]

    move_up = .8*u_up + .1*u_left + .1*u_right
    move_left = .8*u_left + .1*u_up + .1*u_down
    move_right = .8*u_right + .1*u_up + .1*u_down
    move_down = .8*u_down + .1*u_right + .1*u_right
    move = max(move_up, move_left, move_down, move_right)
    if move == move_up:
        val = Q[(x-1, y), "up"]
    elif move == move_down:
        val = Q[(x+1, y), "down"]
    elif move == move_left:
        val = Q[(x, y-1), "left"]
    elif move == move_right:
        val = Q[(x, y+1), "right"]
    else:
        print("ERROR IN MAX Q")
        return -1
    return val

"""
This should be correct
I need to make sure that the maxQ() function works with the current code. I can test this when I finish the main loop
"""

def Q_Learning_Update(s, r, a, s_prime, r_prime, gamma, Q, N, terminals):
    if s_prime in terminals:
        Q[(s_prime, None)] = r_prime
    if s is not None:
        if (s,a) in N:
            N[(s,a)] += 1
        else:
            N[(s,a)] = 1
        
        c = eta(N[(s,a)])

        if (s,a) not in Q:
            Q[(s,a)] = 0.0

        Q[(s, a)] = (1-c)*Q[(s,a)] + c*(r + gamma*maxQ(Q, s_prime, terminals))
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
        Q_Learning_Update(s, r, a, s_prime, r_prime, gamma, Q, N, terminals)
        if i == 5:
            Ne = N[s, a]
        if s_prime in terminals:
            s_prime = next(k for k, v in world.items() if v=="I")
            s = None
            r = None
            a = None
            Ne = None
        a = f_function(Q, N, Ne, s_prime)
        new_s = ExecuteAction(a, s_prime)
        s = s_prime
        s_prime = new_s
        r = r_prime

    
    print_utilites(Q, S)


    return 