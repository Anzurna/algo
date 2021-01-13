import random, sys, time, math
from collections import deque
from queue import PriorityQueue
import numpy as np

def _graph_neighbors(tuple, x_max, y_max, add_diagonal) -> list:
	x, y = tuple
	neighbors = []
	if 1 <= x:  
		neighbors.append((x-1, y))
	if x < x_max:
		neighbors.append((x+1, y))
	if 1 <= y:	
		neighbors.append((x, y-1))
	if y < y_max:
		neighbors.append((x, y+1))

	if add_diagonal:
		if 1 <= y and 1<= x:
			neighbors.append((x-1, y-1))
		if y < y_max and x < x_max:
			neighbors.append((x+1, y+1))
		if 1 <= y and x < x_max:
			neighbors.append((x+1, y-1))
		if 1 <= x and y < y_max:
			neighbors.append((x-1, y+1))
	
	return neighbors	
	
def _graph_cost(current, next) -> float:
	x1, y1 = current
	x2, y2 = next
	dX = abs(x1 - x2)
	dY = abs(y1 -y2)
	
	if (dX and dY) != 0:
		cost = 1.5
	else:
		cost = 1
	return cost
	
def _heuristic(a, b) -> float:
	x1, y1 = a
	x2, y2 = b
	return abs(x1 - x2) + abs(y1 - y2)
			 
def algo(start, goal, matrix) -> list:					
	frontier = PriorityQueue()
	
	came_from = {}

	frontier.put(start, 0)	
	cost_so_far = {}
	came_from[start] = None		
	cost_so_far[start] = 0

	while frontier:
		current = frontier.get()	
		if current == goal:
			break
		for next in _graph_neighbors(current, len(matrix)-1, len(matrix[0])-1, 0):
			new_cost = cost_so_far[current] + _graph_cost(current, next)
			x, y = next
			if matrix[x][y] != 2:
				if next not in cost_so_far or new_cost < cost_so_far[next]:
					cost_so_far[next] = new_cost
					priority = new_cost + _heuristic(goal, next)
					frontier.put(next, priority)
					came_from[next] = current
						
	current_coords = goal
	path = [current]

	while current_coords  != start:
			current_coords  = came_from[current_coords]
			path.append(current_coords )
	path.append(start)
	path.reverse()

	return path

if __name__ == "__main__":
	algo((0,0), (0,0), [])
	print("OOPSIES!")