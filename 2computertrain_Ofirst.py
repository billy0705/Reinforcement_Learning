import random
import pickle
import numpy as np
import matplotlib.pyplot as plt

episodes = 2000000
lr = 0.4
gamma = 0.99
exp = 0.4
win_reward = 1
lose_reward = -1
tie_reward = 0.5
states2value_cross = {}
states2value_circle = {}
win_history = np.zeros(episodes, dtype='int')

def get_hash(state):
    return str(state.reshape(9))

def choose_action(state, switch, exp):
    positions = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                positions.append((i, j))
    if random.uniform(0, 1) <= exp:
        ranpos = np.random.choice(len(positions))
        action = positions[ranpos]
    else:
        states2value = {}
        if switch ==1:
            states2value = states2value_circle
        else:
            states2value = states2value_cross
        value_max = -999
        for p in positions:
            next_state = state.copy()
            next_state[p] = switch
            next_state_hash = get_hash(next_state)
            if states2value.get(next_state_hash) is None:
                value = 0
            else:
                value = states2value.get(next_state_hash)
            if value >= value_max:
                value_max = value
                action = p
    return action

def update_state(state, action, switch):
    state[action] = switch
    return state

def check(state):
    col_sum = np.sum(state, axis=1)
    row_sum = np.sum(state, axis=0)
    cl1 = state[0][0] + state[1][1] + state[2][2] 
    cl2 = state[2][0] + state[1][1] + state[0][2]
    win = 2
    for i in range(8):
        for j in range(3):
            if col_sum[j] == 3:
                win = 1
                break
            elif col_sum[j] == -3:
                win = -1
                break
        if win != 2:
            break
        for j in range(3):
            if row_sum[j] == 3:
                win = 1
                break
            elif row_sum[j] == -3:
                win = -1
                break
        if win != 2:
            break
        if cl1 == 3:
            win = 1
            break
        elif cl1 == -3:
            win = -1
            break
        if cl2 == 3:
            win = 1
            break
        elif cl2 == -3:
            win = -1
            break
    if np.count_nonzero(state != 0) == 9 and win == 2:
        win = 0
    return win

def circle_reward(reward, circle_states, lr, gamma):
    for st in reversed(circle_states):
        if states2value_circle.get(st) is None:
            states2value_circle[st] = 0
        states2value_circle[st] += lr * (gamma * reward - states2value_circle[st])
        reward = states2value_circle[st]
        pass

def cross_reward(reward, cross_states, lr, gamma):
    for st in reversed(cross_states):
        if states2value_cross.get(st) is None:
            states2value_cross[st] = 0
        states2value_cross[st] += lr * (gamma * reward - states2value_cross[st])
        reward = states2value_cross[st]
        pass

for episode in range(episodes):
    if episode % 1000 == 999:
        print("epoch: {:d} / {:d}".format(episode+1, episodes), end="\r", flush=True)
    # if episode == 100000:
    #     exp = 0.2
    exp -= (0.2)/episodes
    lr -= (0.2)/episodes
    state = np.zeros((3, 3), dtype = 'int')
    circle_states = []
    cross_states = []
    switch = random.randint(0,1)
    if switch == 0:
        switch = -1
    switch = 1
    win = 2
    while win == 2:
        if switch ==1:
            action = choose_action(state, switch, exp)
            state = update_state(state, action, switch)
            state_hash = get_hash(state)
            circle_states.append(state_hash)
            win = check(state)
            switch = -1
        else:
            action = choose_action(state, switch, exp)
            state = update_state(state, action, switch)
            state_hash = get_hash(state)
            cross_states.append(state_hash)
            win = check(state)
            switch =1
        #print(state)
        # print(win)
        if win == 1:
            win_history[episode] = 1
            circle_reward(win_reward, circle_states, lr, gamma)
            cross_reward(lose_reward, cross_states, lr, gamma)
        elif win == -1:
            win_history[episode] = -1
            circle_reward(lose_reward, circle_states, lr, gamma)
            cross_reward(win_reward, cross_states, lr, gamma)
        elif win == 0:
            win_history[episode] = 0
            circle_reward(tie_reward, circle_states, lr, gamma)
            cross_reward(tie_reward, cross_states, lr, gamma)

# print(states2value)
fw = open('./models/value_table_cross', 'wb')
pickle.dump(states2value_cross, fw)
fw.close()
fw = open('./models/value_table_circle', 'wb')
pickle.dump(states2value_circle, fw)
fw.close()
# print(win_history)
count = np.zeros((3, episodes), dtype='float')
for i in range(episodes):
    if i == 0:
        if win_history[i] == 1:
            count[0][i] += 1
        elif win_history[i] == -1:
            count[1][i] += 1
        else:
            count[2][i] += 1
    else:
        if win_history[i] == 1:
            count[0][i] = 1 + count[0][i-1]
            count[1][i] = count[1][i-1]
            count[2][i] = count[2][i-1]
        elif win_history[i] == -1:
            count[0][i] = count[0][i-1]
            count[1][i] = 1 + count[1][i-1]
            count[2][i] = count[2][i-1]
        else:
            count[0][i] = count[0][i-1]
            count[1][i] = count[1][i-1]
            count[2][i] = 1 + count[2][i-1]

episodes = range(1, len(win_history)+1)

plt.plot(episodes, count[0]/episodes, 'b', label='Circle Win')
plt.plot(episodes, count[1]/episodes, 'r', label='Cross Win')
plt.plot(episodes, count[2]/episodes, 'g', label='Tie')
plt.title('Ha Ha')
plt.legend()
plt.show()