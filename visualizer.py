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
        self.general_info = self._gen_new_info()

        self.COLOR_BLUE = (0, 0, 255)
        self.COLOR_RED = (255, 0, 0)
        self.COLOR_GREEN = (0, 255, 0)
        self.COLOR_LIGHTPURPLE = (140, 140, 255)
        self.COLOR_CUSTOM = (128,128, 128)
        self.LMB = 0
        self.MMB = 1 
        self.RMB = 2

        self.LMB_CLICK_INFO = {"color": self.COLOR_RED, 
                               "mouse_button": self.LMB}
        self.RMB_CLICK_INFO = {"color": self.COLOR_BLUE, 
                               "mouse_button": self.RMB}
        self.MMB_CLICK_INFO = {"color": self.COLOR_LIGHTPURPLE, 
                               "mouse_button": self.MMB}

    def _create_grid(self) -> None:
        for y in range(0, self.height, self.block_size + self.border_size):
            r_row = []
            for x in range(0, self.width, self.block_size + self.border_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                r_row.append([rect, self.COLOR_GREEN])
            self.rectangles.append(r_row)

    def _update_grid(self) -> None:
        for row in self.rectangles:
            for rectangle in row:
                rect_pos_and_dimensions, color = rectangle[0], rectangle[1]
                pygame.draw.rect(self.DISPLAYSURF, color, 
                                 rect_pos_and_dimensions)

    def _renew_grid(self) -> None:
        for row in self.rectangles:
            for rectangle in row:
                self._change_color(rectangle, self.COLOR_GREEN)

    def _gen_new_info(self) -> dict:
        return {"start_coords" : (0, 0), 
                "goal_coords"  : (0, 0), 
                "is_start_set" :  False, 
                "is_goal_set"  :  False}

    def _unify_values(self, value) -> int:
        if value == self.COLOR_BLUE:
            return 2
        if value == self.COLOR_GREEN:
            return 0

    def _unify_matrix(self, rectangles) -> list:
        return [[self._unify_values(rectangle[1]) for rectangle in row] for row in rectangles]

    def _calculate_path(self) -> list:
        unified_matrix = self._unify_matrix(self.rectangles)
        return compute_a_star(self.general_info["start_coords"], 
                              self.general_info["goal_coords"], 
                           unified_matrix)	

    def _change_color(self, rectangle, color) -> None:
        rectangle[1] = color

    def _visualize_path(self, path) -> None:
        for x, y in path:
            if ((x, y) != self.general_info["goal_coords"] and
                (x, y) != self.general_info["start_coords"]):
                self._change_color(self.rectangles[x][y], self.COLOR_CUSTOM)
                

    def _check_mouse_collision(self, event) -> dict:
        for index_x, r_row in enumerate(self.rectangles):
            for index_y, rectangle in enumerate(r_row):
                rect_pos_and_dimensions = rectangle[0]
                try:
                    if rect_pos_and_dimensions.collidepoint(event.pos):
                        return {"num_coords": (index_x, index_y), 
                                "object": rectangle, 
                                "has_collided": True}
                except:
                    pass

    def _check_single_mouse_click(self, event_list, event, click_info, 
                                 status_key, coords_key) -> None:
        if event_list[click_info["mouse_button"]]:
            mouse_collision_info = self._check_mouse_collision(event)
            try:
                if (mouse_collision_info["has_collided"] and 
                    not self.general_info[status_key]):

                    self._change_color(mouse_collision_info["object"],
                                      click_info["color"])
                    self.general_info[coords_key] = mouse_collision_info["num_coords"] 
                    self.general_info[status_key] = True				
            except:
                pass

    def _check_multiple_mouse_clicks(self, event_list, event, click_info) -> None:
        if event_list[click_info["mouse_button"]]:
            mouse_collision_info = self._check_mouse_collision(event)
            try:
                if mouse_collision_info["has_collided"]:
                    self._change_color(mouse_collision_info["object"],
                                      click_info["color"])
            except:
                pass			

    def _listen_mouse_events(self, general_info, event) -> None:
        mouse_buttons_pressed = pygame.mouse.get_pressed()
        self._check_single_mouse_click(mouse_buttons_pressed, event,
                                      self.LMB_CLICK_INFO, 
                                      "is_start_set", "start_coords")
        self._check_single_mouse_click(mouse_buttons_pressed, event,
                                      self.MMB_CLICK_INFO,  
                                      "is_goal_set", "goal_coords")
        self._check_multiple_mouse_clicks(mouse_buttons_pressed, event, 
                                         self.RMB_CLICK_INFO)

    def _listen_keyboard_events(self, event) -> None:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self._visualize_path(self._calculate_path())
            if event.key == K_BACKSPACE:
                self._renew_grid()
                self.general_info = self._gen_new_info()

    def main_loop(self) -> None:
        pygame.display.init()
        clock = pygame.time.Clock()
        pygame.mixer.quit()
        self._create_grid()
        self._update_grid()   

        while True: # main game loop
            events = pygame.event.get()
            for event in events:
                print(event)
                self._listen_keyboard_events(event)
                self._listen_mouse_events(self.general_info, event)

            self._update_grid()
            clock.tick(30)
            pygame.display.update()

if __name__ == "__main__":
    visualizer = AlgoVisualizer()
    visualizer.main_loop()