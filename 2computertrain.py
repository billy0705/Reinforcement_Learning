import random
import pickle
import numpy as np
import matplotlib.pyplot as plt

epochs = 100000
lr = 0.3
gamma = 0.99
exp = 0.3
global states2value
states2value = {}
win_history = np.zeros(epochs, dtype='int')

def get_hash(state):
    return str(state.reshape(9))

def choose_action(state, switch):
    positions = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                positions.append((i, j))
    if random.uniform(0, 1) <= exp:
        ranpos = np.random.choice(len(positions))
        action = positions[ranpos]
    else:
        global states2value
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

def circle_reward(reward, circle_states):
    global states2value
    for st in reversed(circle_states):
        if states2value.get(st) is None:
            states2value[st] = 0
        states2value[st] += lr * (gamma * reward - states2value[st])
        reward = states2value[st]
        pass

def cross_reward(reward, cross_states):
    global states2value
    for st in reversed(cross_states):
        if states2value.get(st) is None:
            states2value[st] = 0
        states2value[st] += lr * (gamma * reward - states2value[st])
        reward = states2value[st]
        pass

for epoch in range(epochs):
    if epoch % 1000 == 999:
        print("\repoch: {:d} / {:d}".format(epoch+1, epochs), end="", flush=True)
    if epoch == 100000:
        exp = 0.2
    state = np.zeros((3, 3), dtype = 'int')
    circle_states = []
    cross_states = []
    switch = random.randint(0,1)
    if switch == 0:
        switch = -1
    win = 2
    while win == 2:
        if switch ==1:
            action = choose_action(state, switch)
            state = update_state(state, action, switch)
            state_hash = get_hash(state)
            circle_states.append(state_hash)
            win = check(state)
            switch = -1
        else:
            action = choose_action(state, switch)
            state = update_state(state, action, switch)
            state_hash = get_hash(state)
            cross_states.append(state_hash)
            win = check(state)
            switch =1
        #print(state)
        # print(win)
        if win == 1:
            win_history[epoch] = 1
            circle_reward(1, circle_states)
            cross_reward(-1, cross_states)
        elif win == -1:
            win_history[epoch] = -1
            circle_reward(-1, circle_states)
            cross_reward(1, cross_states)
        elif win == 0:
            win_history[epoch] = 0
            circle_reward(0.5, circle_states)
            cross_reward(0.5, cross_states)

# print(states2value)
fw = open('./models/value_table', 'wb')
pickle.dump(states2value, fw)
fw.close()
# print(win_history)
count = np.zeros((3, epochs), dtype='int')
for i in range(epochs):
    count[0][i] = np.count_nonzero(win_history[0:i] == 1)
    count[1][i] = np.count_nonzero(win_history[0:i] == -1)
    count[2][i] = np.count_nonzero(win_history[0:i] == 0)
epochs = range(1, len(win_history)+1)

plt.plot(epochs, count[0], 'b', label='Circle Win')
plt.plot(epochs, count[1], 'r', label='Cross Win')
plt.plot(epochs, count[2], 'g', label='Tie')
plt.title('Ha Ha')
plt.legend()
plt.show()