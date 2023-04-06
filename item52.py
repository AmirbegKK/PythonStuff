# import subprocess

# result = subprocess.run(
# 	['echo', 'Hello from the child!'],
# 	capture_output=True,
# 	encoding='utf-8',
# 	)

# result.check_returncode()
# print(result.stdout)


# proc = subprocess.Popen(['sleep', '1'])
# while proc.poll() is None:
# 	print('Working...')
# print('Exit status', proc.poll())

# import time

# start = time.time()

# sleep_procs = []

# for _ in range(10):
# 	proc = subprocess.Popen(['sleep', '1'])
# 	sleep_procs.append(proc)

# for proc in sleep_procs:
# 	proc.communicate()

# end = time.time()

# delta = end - start

# # print(f'Finished in {delta:.3} seconds')


# import os

# def run_encrypt(data):
# 	env = os.environ.copy()

# 	env['password'] = '1234567890'

# 	proc = subprocess.Popen(
# 		['openssl', 'enc', '-des3', '-pass', 'env:password'],
# 		env=env,
# 		stdin=subprocess.PIPE,
# 		stdout=subprocess.PIPE,
# 		)

# 	proc.stdin.write(data)
# 	proc.stdin.flush()
# 	return proc

# procs = []

# for _ in range(3):
# 	data = os.urandom(10)
# 	proc = run_encrypt(data)
# 	procs.append(proc)

# for proc in procs:
# 	out, _ = proc.communicate()
# 	print(out[-10:])

# def run_hash(input_stdin):
# 	return subprocess.Popen(
# 		['openssl', 'dgst', '-whirlpool', '-binary'],
# 		stdin=input_stdin,
# 		stdout=subprocess.PIPE)

# encrypt_procs = []
# hash_procs = []

# for _ in range(3):
# 	data = os.urandom(10)

# 	encrypt_proc = run_encrypt(data)
# 	encrypt_procs.append(encrypt_proc)

# 	hash_proc = run_hash(encrypt_proc.stdout)
# 	hash_procs.append(hash_proc)

# 	encrypt_proc.stdout.close()
# 	encrypt_proc.stdout = None

# for proc in encrypt_procs:
# 	proc.communicate()
# 	assert proc.returncode == 0

# for proc in hash_procs:
# 	out, _ = proc.communicate()
# 	print(out[-10:])
	# assert proc.returncode == 0

# proc = subprocess.Popen(['sleep', '5'])
# try:
# 	proc.communicate(timeout=1)
# # except subprocess.TimeoutExpired:
# # 	proc.terminate()
# # 	proc.wait()

# # print('Exit status', proc.poll())




# # ----------------------------------------------------
# # ----------------------------------------------------
# # Item 53: Use Threads for blocking I/O

# # import select
# # import socket
# # import time
# # from threading import Thread

# # def slow_systemcall():
# # 	select.select([socket.socket()], [], [], 0.1)

# # start = time.time()

# # threads = []

# # for _ in range(5):
# # 	thread = Thread(target=slow_systemcall)
# # 	thread.start()
# # 	threads.append(thread)

# # def compute_helicopter_loc(index):
# # 	...

# # for i in range(5):
# # 	compute_helicopter_loc(i)

# # for thread in threads:
# # 	thread.join()

# # end = time.time()
# # delta = end - start

# # print(f'Took {delta:.3} seconds')



# # ----------------------------------------------------
# # ----------------------------------------------------
# # 
# # Item 54: Use Lock To Prevent Data Races in Threads

# # from threading import Lock, Thread

# # def worker(sensor_index, how_many, counter):
# # 	for _ in range(how_many):
# # 		counter.increment(1)

# # class LockingCounter:
# # 	def __init__(self):
# # 		self.lock = Lock()
# # 		self.count = 0

# # 	def increment(self, offset):
# # 		with self.lock:
# # 			self.count += offset

# # counter = LockingCounter()
# # threads = []
# # for i in range(5):
# # 	thread = Thread(target=worker, args=(i, 10**5, counter))
# # 	threads.append(thread)
# # 	thread.start()

# # for thread in threads:
# # 	thread.join()

# # expected = (10**5)*5
# # found = counter.count

# # print(f'Counter should be {expected}, got {found}')


# # ----------------------------------------------------
# # ----------------------------------------------------
# # 
# # Item 56: Know How To Recognize When Concurrency Is Necessary
# # 

ALIVE = '*'
EMPTY = '-'

class Grid:
	def __init__(self, height, width):
		self.height = height
		self.width = width
		self.rows = []

		for _ in range(self.height):
			self.rows.append([EMPTY] * self.width)

	def get(self, y, x):
		return self.rows[y % self.height][x % self.width]

	def set(self, y, x, state):
		self.rows[y % self.height][x % self.width] = state

	def __str__(self):
		final_str = ''
		for row in self.rows:
			final_str += ''.join(row) + '\n'
		return final_str

def count_neighbours(y, x, get):
	n_ = get(y - 1, x + 0) # North
	ne = get(y - 1, x + 1) # Northeast
	e_ = get(y + 0, x + 1) # East
	se = get(y + 1, x + 1) # Southeast
	s_ = get(y + 1, x + 0) # South
	sw = get(y + 1, x - 1) # Southwest
	w_ = get(y + 0, x - 1) # North
	nw = get(y + 1, x - 1) # Northwest
	neighbours_state = [n_, ne, e_, se, s_, sw, w_, nw]
	count = 0

	for state in neighbours_state:
		if state == ALIVE:
			count += 1
	return count

import aiohttp
import asyncio

async def game_logic(state, neighbours):
	if state == ALIVE:
		if neighbours < 2:
			return EMPTY
		elif neighbours > 3:
			return EMPTY
	else:
		if neighbours == 3:
			return ALIVE
	async with aiohttp.ClientSession() as ses:
		await ses.get('http://httpbin.org/get')
	return state

async def step_cell(y, x, get, set):
	state = get(y, x)
	neighbours = count_neighbours(y, x, get)
	next_state = await game_logic(state, neighbours)
	set(y, x, next_state)

async def simulate(grid):
	tasks = []
	next_grid = Grid(grid.height, grid.width)
	for y in range(grid.height):
		for x in range(grid.width):
			tasks.append(step_cell(y, x, grid.get, next_grid.set))
	await asyncio.gather(*tasks)

	return next_grid

grid = Grid(3, 5)
grid.set(0, 3, ALIVE)
grid.set(1, 1, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(0, 0, ALIVE)
import time

start = time.time()
for i in range(5):
	grid = asyncio.run(simulate(grid))
	print(grid)
delta = time.time() - start
print(f'Execution time is {delta:.2}')


