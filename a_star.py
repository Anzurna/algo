import random, sys, time, math, pygame
from pygame.locals import *
import time
pygame.display.init()

loop_time = time.time()

height = 400
width = 400
color = (255, 0, 0)
DISPLAYSURF = pygame.display.set_mode((height, width))
rectangles = []
block_size = 25
for y in range(height):
	r_row = []
	for x in range(width):
		rect = pygame.Rect(x*(block_size+1), y*(block_size+1), block_size, block_size)
		r_row.append([rect, (0, 255, 0)])
	rectangles.append(r_row)
clock = pygame.time.Clock()
pygame.mixer.quit()

for row in rectangles:
		for item in row:
			rect, color = item
			pygame.draw.rect(DISPLAYSURF, color, rect)
while True: # main game loop
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
			
	if pygame.mouse.get_pressed()[0]:
		for r_row in rectangles:
			for item in r_row:
				rect, color = item
				if rect.collidepoint(event.pos):
					#if color == (0, 255, 0):
					item[1] = (255, 0, 0)
					#else:
						#item[1] = (0, 255, 0)
					pygame.draw.rect(DISPLAYSURF, color, rect)
	if pygame.mouse.get_pressed()[2]:
		for r_row in rectangles:
			for item in r_row:
				rect, color = item
				if rect.collidepoint(event.pos):
					#if color == (0, 255, 0):
					item[1] = (0, 0, 255)
					#else:
						#item[1] = (0, 255, 0)						
					pygame.draw.rect(DISPLAYSURF, color, rect)
	#for row in rectangles:
		#for item in row:
			#rect, color = item
			#pygame.draw.rect(DISPLAYSURF, color, rect)	
			
	clock.tick(30)
	pygame.display.update()
		