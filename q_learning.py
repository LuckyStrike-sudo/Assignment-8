#Caedmon Boutwell 1001988638
import numpy as np


def read_file(file):
    arr = []
    f = open(file, 'r')
    for i in f:
        temp = i.split(",")
        arr.append(temp)

    return arr

def value_iteration(environment_file, non_terminal_reward, gamma, K):
    S = read_file(environment_file)
    S = np.array(S)
    valueIteration(S, None, non_terminal_reward, gamma, K)

def print_utilities(dict, S):
    print("utilities:")
    for i, r in enumerate(S):
        for j, c in enumerate(r):
            if c == "X":
                print(" 0.000", end= " ")
            else:
                print("%6.3f" % dict[(i,j)], end=" ")
        print("")

def print_policy(dict, S):
    print("\npolicy:")
    for i, r in enumerate(S):
        for j, c in enumerate(r):
            print("%6s" % dict[(i,j)], end=" ")
        print("")


def maxUtility(U, s, terminals, policy):
    x, y = s
    #Utiltiy of the space to the left
    if (x-1, y) in U:
        if U[(x-1, y)] != "X":
            if (x-1, y) in terminals:
                u_up = terminals[(x-1,y)]
            else:
                u_up = U[(x-1, y)]
        else:
            u_up = U[s]
    else:
        u_up = U[s]

    #utility of the sapce up
    if (x, y-1) in U:
        if U[(x, y-1)] != "X":
            if (x, y-1) in terminals:
                u_left = terminals[(x, y-1)]
            else:
                u_left = U[(x, y-1)]
        else:
            u_left = U[s]
    else:
        u_left = U[s]
    
    #Utility of the space to the right
    if (x+1, y) in U:
        if U[(x+1, y)] != "X":
            if (x+1, y) in terminals:
                u_down = terminals[(x+1, y)]
            else:
                u_down = U[(x+1, y)]
        else:
            u_down = U[s]
    else:
        u_down = U[s]

    #utility of the space down
    if (x, y+1) in U:
        if U[(x, y+1)] != "X":
            if (x, y+1) in terminals:
                u_right = terminals[(x, y+1)]
            else:
                u_right = U[(x, y+1)]
        else:
            u_right = U[s]
    else:
        u_right = U[s]

    move_up = .8*u_up + .1*u_left + .1*u_right
    move_left = .8*u_left + .1*u_up + .1*u_down
    move_right = .8*u_right + .1*u_up + .1*u_down
    move_down = .8*u_down + .1*u_right + .1*u_right
    move = max(move_up, move_left, move_down, move_right)
    if move == move_up:
        policy[s] = "^"
    elif move == move_down:
        policy[s] = "v"
    elif move == move_left:
        policy[s] = "<"
    elif move == move_right:
        policy[s] = ">"

    return move
    

def valueIteration(S, A, R, gamma, K):
    N = len(S.flatten())
    U_prime = {}
    terminals = {}
    policy = {}
    for i, r in enumerate(S):
        for j, c in enumerate(r):
            if c != "." and c != "X":
                U_prime[(i,j)] = float(c)
                terminals[(i,j)] = float(c)
                policy[(i,j)] = "o"
            elif c == ".":
                U_prime[(i,j)] = 0.0
                policy[(i,j)] = "."
            else:
                U_prime[(i,j)] = c
                policy[(i,j)] = c

    for i in range(0, K-1):
        U = U_prime
        delta = 0
        for i, r in enumerate(S):
            for j, c in enumerate(r):
                if (i, j) in terminals:
                    U_prime[(i,j)] = terminals[(i,j)]
                elif U[(i,j)] == 'X':
                    continue
                else:
                    U_prime[(i,j)] = R + gamma*maxUtility(U, (i,j), terminals, policy)
                if abs(U_prime[(i,j)] - U[(i,j)]) > delta:
                    delta = abs(U_prime[(i,j)] - U[(i,j)])

    print_utilities(U_prime, S)
    print_policy(policy, S)


def AgentModel_Q_Learning(environment_file, non_terminal_reward, gamma, number_of_moves, Ne):
    value_iteration(environment_file, non_terminal_reward, gamma, 50)
    return 