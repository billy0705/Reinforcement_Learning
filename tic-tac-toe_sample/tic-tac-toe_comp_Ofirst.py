import tkinter as tk
import random
import numpy as np
import pickle

fr = open('./models/value_table_cross', 'rb')
states2value = pickle.load(fr)
fr.close()

def get_hash(state):
    return str(state.reshape(9))

def update_state(state, action, switch):
    state[action] = switch
    return state

def choose_action(state, switch, states2value):
	positions = []
	for i in range(3):
		for j in range(3):
			if state[i][j] == 0:
				positions.append((i, j))

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

def paint_cross(x, y, col):
	c.create_line(x*100+10, y*100+10, x*100+90, y*100+90,fill=col,width=2)
	c.create_line(x*100+90, y*100+10, x*100+10, y*100+90,fill=col,width=2)

def paint_circle(x, y, col):
	c.create_oval(x*100+10, y*100+10, x*100+90, y*100+90, outline=col, width=2)
	
def check(state):
	col_sum = np.sum(state, axis=0)
	row_sum = np.sum(state, axis=1)
	cl1 = state[0][0] + state[1][1] + state[2][2] 
	cl2 = state[2][0] + state[1][1] + state[0][2]
	win = 0
	for i in range(8):
		for j in range(3):
			if col_sum[j] == 3:
				win = 1
				paint_circle(j, 0, 'red')
				paint_circle(j, 1, 'red')
				paint_circle(j, 2, 'red')
				break
			elif col_sum[j] == -3:
				win = -1
				paint_cross(j, 0, 'red')
				paint_cross(j, 1, 'red')
				paint_cross(j, 2, 'red')
				break
		if win != 0:
			break
		for j in range(3):
			if row_sum[j] == 3:
				win = 1
				paint_circle(0, j, 'red')
				paint_circle(1, j, 'red')
				paint_circle(2, j, 'red')
				break
			elif row_sum[j] == -3:
				win = -1
				paint_cross(0, j, 'red')
				paint_cross(1, j, 'red')
				paint_cross(2, j, 'red')
				break
		if win != 0:
			break
		if cl1 == 3:
			win = 1
			paint_circle(0, 0, 'red')
			paint_circle(1, 1, 'red')
			paint_circle(2, 2, 'red')
			break
		elif cl1 == -3:
			win = -1
			paint_cross(0, 0, 'red')
			paint_cross(1, 1, 'red')
			paint_cross(2, 2, 'red')
			break
		if cl2 == 3:
			win = 1
			paint_circle(2, 0, 'red')
			paint_circle(1, 1, 'red')
			paint_circle(0, 2, 'red')
			break
		elif cl2 == -3:
			win = -1
			paint_cross(2, 0, 'red')
			paint_cross(1, 1, 'red')
			paint_cross(0, 2, 'red')
			break
	if np.count_nonzero(state != 0) == 9 and win == 0:
		win = 2
	# print(col_sum, row_sum, cl1, cl2, win)
	return win

def paint(event):
	if event.x > 200:
		x = 2
	elif event.x >100:
		x = 1
	else:
		x = 0
	if event.y > 200:
		y = 2
	elif event.y >100:
		y = 1
	else:
		y = 0
	# print(x, y)
	global switch
	global state
	global Circle_score
	global Cross_score
	win = 0
	temp = switch
	# print(state[x][y])
	if switch == 1 and state[y][x] == 0:
		paint_circle(x, y, 'black')
		state[y][x] = switch
		# print(state)
		l2.config(text='cross turn')
		win = check(state)
		switch = -1
	# elif switch == -1 and state[x][y] == 0:
	# 	paint_cross(x, y, 'black')
	# 	state[x][y] = switch
	# 	l2.config(text='circle turn')
	# 	win = check(state)
	# 	temp = 1
	if win == 0:
		if switch == -1:
			action = choose_action(state, switch, states2value)
			paint_cross(action[1], action[0], 'black')
			state = update_state(state, action, switch)
			win = check(state)
			if win == 0:
				l2.config(text='circle turn')
				switch = 1
			else:
				l2.config(text='Game Finish')
				if win == 1:	
					Circle_score += 1
					l6.config(text=str(Circle_score))
					l7.config(text='Circle Win')
					switch =2
				elif win == -1:	
					Cross_score += 1
					l5.config(text=str(Cross_score))
					l7.config(text='Cross Win')
					switch = 2
				else:
					l7.config(text='Tie')
	else:
		l2.config(text='Game Finish')
		if win == 1:
			Circle_score += 1
			l6.config(text=str(Circle_score))
			l7.config(text='Circle Win')
			switch =2
		elif win == -1:
			Cross_score += 1
			l5.config(text=str(Cross_score))
			l7.config(text='Cross Win')
			switch = 2
		elif win==2:
			l7.config(text='Tie')
	# print(state)


def Game_init():
	c.delete('all')
	c.create_line(100,0,100,300,fill='black',width=2)
	c.create_line(200,0,200,300,fill='black',width=2)
	c.create_line(0,100,300,100,fill='black',width=2)
	c.create_line(0,200,300,200,fill='black',width=2)
	global switch
	switch = random.randint(0,1)
	switch = 1
	if switch == 0:
		switch = -1
		l2.config(text='cross turn')
	else:
		l2.config(text='circle turn')
	global state
	state = np.zeros((3, 3), dtype = 'int')
	global Cross_score
	global Circle_score
	Cross_score = 0
	Circle_score = 0
	l3.config(text='Cross Score:')
	l4.config(text='Circle Score:')
	l6.config(text=str(Circle_score))
	l5.config(text=str(Cross_score))
	l7.config(text='')
	b1.config(text='Game init')
	b2 = tk.Button(f, text='Canvas init', command=canvas_init)
	b2.grid(row=6, column=0)
	global game_count
	game_count = 1
	l1.config(text='Game' + str(game_count))
	if switch == -1:
		action = choose_action(state, switch, states2value)
		paint_cross(action[1], action[0], 'black')
		state = update_state(state, action, switch)
		l2.config(text='circle turn')
		switch = 1


def canvas_init():
	c.delete('all')
	c.create_line(100,0,100,300,fill='black',width=2)
	c.create_line(200,0,200,300,fill='black',width=2)
	c.create_line(0,100,300,100,fill='black',width=2)
	c.create_line(0,200,300,200,fill='black',width=2)
	global switch
	switch = random.randint(0,1)
	switch = 1
	if switch == 0:
		switch = -1
		l2.config(text='cross turn')
	else:
		l2.config(text='circle turn')
	global state
	state = np.zeros((3, 3), dtype = 'int')
	l7.config(text='')
	global game_count
	game_count += 1
	l1.config(text='Game' + str(game_count))
	if switch == -1:
		action = choose_action(state, switch, states2value)
		paint_cross(action[1], action[0], 'black')
		state = update_state(state, action, switch)
		l2.config(text='circle turn')
		switch = 1

window = tk.Tk()
window.title('My Window')
window.geometry('600x310')

c = tk.Canvas(window, height=300, width=300, bg='white')
c.grid(row=0, column=0)

f = tk.Frame(window)
f.grid(row=0, column=1, sticky='n')

l1 = tk.Label(f, text='Press Start To Play', font=('Arial', 30))
l1.grid(row=0, column=0)
b1 = tk.Button(f, text='Start',width=13, height=2, command=Game_init)
b1.grid(row=1, column=0)
l2 = tk.Label(f, text='', font=('Arial', 30))
l2.grid(row=2, column=0)
l3 = tk.Label(f, text='', font=('Arial', 20))
l3.grid(row=3, column=0)
l4 = tk.Label(f, text='', font=('Arial', 20))
l4.grid(row=3, column=1)
l5 = tk.Label(f, text='', font=('Arial', 20))
l5.grid(row=4, column=0)
l6 = tk.Label(f, text='', font=('Arial', 20))
l6.grid(row=4, column=1)
l7 = tk.Label(f, text='', font=('Arial', 30))
l7.grid(row=5, column=0)


c.bind('<Button-1>', paint)

window.mainloop()