import random, sys, time, math, pygame
from pygame.locals import *
import time
from a_star_np import algo as compute_a_star

class AlgoVisualizer:
	def __init__(self):
		self.height = 600
		self.width = 800

		self.DISPLAYSURF = pygame.display.set_mode((self.width, self.height))
		self.rectangles = []
		self.block_size = 5
		self.border_size = 1
		self.general_info = self.new_gen_info()

		self.COLOR_BLUE = (0, 0, 255)
		self.COLOR_RED = (255, 0, 0)
		self.COLOR_GREEN = (0, 255, 0)
		self.COLOR_LIGHTPURPLE = (140, 140, 255)
		self.COLOR_CUSTOM = (128, 128, 128)
		self.LMB = 0
		self.MMB = 1 
		self.RMB = 2

		self.LMB_CLICK_INFO = {"color": self.COLOR_RED, 
							   "mouse_button": self.LMB}
		self.RMB_CLICK_INFO = {"color": self.COLOR_BLUE, 
							   "mouse_button": self.RMB}
		self.MMB_CLICK_INFO = {"color": self.COLOR_LIGHTPURPLE, 
							   "mouse_button": self.MMB}

	def create_grid(self) -> None:
		for y in range(0, self.height, self.block_size + self.border_size):
			self.r_row = []
			for x in range(0, self.width, self.block_size + self.border_size):
				rect = pygame.Rect(x, y, self.block_size, self.block_size)
				self.r_row.append([rect, self.COLOR_GREEN, 0, 0])
			self.rectangles.append(self.r_row)

	def update_grid(self) -> None:
		for row in self.rectangles:
			for item in row:
				rect, color = item[0], item[1]
				pygame.draw.rect(self.DISPLAYSURF, color, rect)
	def renew_grid(self):
		for row in self.rectangles:
			for item in row:
				item[1] = self.COLOR_GREEN
	def new_gen_info(self):
		return {"start_coords": (0, 0), 
				"goal_coords"  : (0, 0), 
				"is_start_set" :  False, 
				"is_goal_set"  :  False}

	def unify_values(self, value) -> tuple:
		if value == self.COLOR_BLUE:
			return 2
		if value == self.COLOR_GREEN:
			return 0

	def unify_matrix(self, rectangles) -> tuple:
		return [[self.unify_values(item[1]) for item in row] for row in rectangles]

	def calculate_path(self) -> list:
		unified_matrix = self.unify_matrix(self.rectangles)
		return compute_a_star(self.general_info["start_coords"], 
							  self.general_info["goal_coords"], 
							  unified_matrix)	

	def visualize_path(self, path) -> None:
		for x, y in path:
			if ((x, y) != self.general_info["goal_coords"] and
			    (x, y) != self.general_info["start_coords"]):
				self.rectangles[x][y][1] = self.COLOR_CUSTOM

	def check_mouse_collision(self, event):
		for index_x, r_row in enumerate(self.rectangles):
			for index_y, item in enumerate(r_row):
				rect = item[0]
				if rect.collidepoint(event.pos):
					return {"num_coords": (index_x, index_y), 
							"object": item, 
							"has_collided": True}

	def check_single_mouse_click(self, event_list, click_info, 
								 event, addit_conditional, cords) -> None:
		if event_list[click_info["mouse_button"]]:
			mouse_collision_info = self.check_mouse_collision(event)
			try:
				if (mouse_collision_info["has_collided"] and 
				    not self.general_info[addit_conditional]):
					mouse_collision_info["object"][1] = click_info["color"]
					self.general_info[cords] = mouse_collision_info["num_coords"] 
					self.general_info[addit_conditional] = True				
			except:
				pass

	def check_multiple_mouse_clicks(self, event_list, click_info, event) -> None:
		if event_list[click_info["mouse_button"]]:
			mouse_collision_info = self.check_mouse_collision(event)
			try:
				if mouse_collision_info["has_collided"]:
					mouse_collision_info["object"][1] = click_info["color"]
			except:
				pass			

	def listen_mouse_events(self, general_info, event) -> None:
		mouse_buttons_pressed = pygame.mouse.get_pressed()
		self.check_single_mouse_click(mouse_buttons_pressed, 
									  self.LMB_CLICK_INFO, 
									  event, 
									  "is_start_set", "start_coords")
		self.check_single_mouse_click(mouse_buttons_pressed, 
									  self.MMB_CLICK_INFO, 
									  event, 
									  "is_goal_set", "goal_coords")
		self.check_multiple_mouse_clicks(mouse_buttons_pressed, 
										 self.RMB_CLICK_INFO, 
										 event)

	def listen_keyboard_events(self, event) -> None:
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				self.visualize_path(self.calculate_path())
			if event.key == K_BACKSPACE:
				self.renew_grid()
				self.general_info = self.new_gen_info()

	def main_loop(self) -> None:
		pygame.display.init()
		loop_time = time.time()
		clock = pygame.time.Clock()
		pygame.mixer.quit()
		self.create_grid()
		self.update_grid()
		print(type(pygame.mouse.get_pressed()))
		print(pygame.mouse.get_pressed())
		while True: # main game loop
			events = pygame.event.get()
			for event in events:
				self.listen_keyboard_events(event)
				self.listen_mouse_events(self.general_info, event)

			self.update_grid()
			clock.tick(30)
			pygame.display.update()

if __name__ == "__main__":
	visualizer = AlgoVisualizer()
	visualizer.main_loop()