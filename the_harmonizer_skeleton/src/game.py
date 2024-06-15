import time

from src.tile import *
from src.elements import *

from agent.agents import *


class Game:
    def __init__(self):
        """
            Initializes the game object class.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.agent_activated = False
        self.agent_solve_time = 0
        self.moves = None
        self.road = None
        self.all_sprites = None
        self.tiles_grid = None
        self.tiles = None
        self.p1_pos = [0, 0]
        self.p2_pos = [0, 0]
        self.button_list = None
        self.playing = False
        self.start_game = False
        self.timer = 0
        self.start_timer = False
        self.end_game = False
        self.best_time = False
        self.elapsed_time = 0
        self.number_of_moves = 0
        self.time_high_score, self.move_high_score = self.get_score()
        self.level = 1

    @staticmethod
    def get_score():
        """
            Gets the high score from the score.txt file.

            Returns:
                float: High score
        """
        try:
            with open("score/score.txt", "r") as file:
                lines = file.read().splitlines()
                return [float(lines[0]), float(lines[1]), float(lines[2])], \
                    [int(lines[3]), int(lines[4]), int(lines[5])]
        except OSError or IOError or Exception:
            return [999.999, 999.999, 999.999]

    def save_score(self):
        """
            Saves the high score to the score.txt file.
        """
        with open("score/score.txt", "w") as file:
            file.write(f"{self.time_high_score[0]}\n{self.time_high_score[1]}\n{self.time_high_score[2]}\n"
                       f"{self.move_high_score[0]}\n{self.move_high_score[1]}\n{self.move_high_score[2]}\n")

    def create_game(self):
        """
            Creates the game matrix.
        """
        grid = []
        for i, row in enumerate(settings.LEVELS[self.level - 1]):
            grid.append([])
            for j, col in enumerate(row):
                grid[i].append(int(col))
                if col == "1":
                    self.p1_pos = [i, j]
                elif col == "2":
                    self.p2_pos = [i, j]
        return grid

    def draw_tiles(self):
        """
            Draws the tiles on the game grid.
        """
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, y in enumerate(x):
                self.tiles[row].append(Tile(self, col, row, str(y)))

    def draw_grid(self):
        """
            Draws the game grid.
        """
        for row in range(-1, settings.GAMESIZE[1] * settings.TILESIZE, settings.TILESIZE):
            pygame.draw.line(self.screen, settings.LIGHTGRAY, (settings.START[0] + row, settings.START[1]),
                             (settings.START[0] + row, settings.GAMESIZE[1] * settings.TILESIZE + settings.START[1]))

        for column in range(-1, settings.GAMESIZE[0] * settings.TILESIZE, settings.TILESIZE):
            pygame.draw.line(self.screen, settings.LIGHTGRAY, (settings.START[0], settings.START[1] + column),
                             (settings.GAMESIZE[0] * settings.TILESIZE + settings.START[0], settings.START[1] + column))

    def draw_element(self):
        """
            Draws the UI elements.
        """
        for button in self.button_list:
            button.draw(self.screen)

        Text(512, 75, settings.TITLE.upper(), 40).draw(self.screen)

        Text(890, 160, "Time", 30).draw(self.screen)
        Text(890, 200, f"{self.elapsed_time:.3f}", 30).draw(self.screen)
        Text(890, 260, "Moves", 30).draw(self.screen)
        Text(890, 300, str(self.number_of_moves), 30).draw(self.screen)
        Text(140, 160, "Time High Score", 30).draw(self.screen)
        Text(140, 200, f"{self.time_high_score[self.level - 1]:.3f}", 30).draw(self.screen)
        Text(140, 260, "Move High Score", 30).draw(self.screen)
        Text(140, 300, str(self.move_high_score[self.level - 1]), 30).draw(self.screen)
        Text(890, 450, "Solve with", 30).draw(self.screen)

    def draw(self):
        """
            Game loop - draw.
        """
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        self.draw_element()
        pygame.display.flip()

    def new(self):
        """
            Starts a new game.
        """
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        settings.GAMESIZE = [len(self.tiles_grid[0]), len(self.tiles_grid)]
        settings.TILESIZE = settings.BOARDSIZE // max(settings.GAMESIZE[0], settings.GAMESIZE[1])
        settings.START = [(settings.WIDTH - settings.BOARDSIZE) // 2, (settings.HEIGHT - settings.BOARDSIZE) // 4 + 50]
        self.best_time = False
        self.elapsed_time = 0
        self.number_of_moves = 0
        self.agent_activated = False
        self.agent_solve_time = 0
        self.moves = None
        self.road = None
        self.start_timer = False
        self.start_game = False
        self.end_game = False
        self.draw_tiles()

        self.button_list = []
        self.button_list.append(Button(412, 660, 200, 50, "Reset", 25, settings.WHITE, settings.BLACK, 25))

        self.button_list.append(Button(387, 580, 50, 50, "1", 25, settings.WHITE, settings.BLACK))
        self.button_list.append(Button(487, 580, 50, 50, "2", 25, settings.WHITE, settings.BLACK))
        self.button_list.append(Button(587, 580, 50, 50, "3", 25, settings.WHITE, settings.BLACK))

        self.button_list.append(Button(800, 480, 80, 50, "BFS T", 25, settings.WHITE, settings.BLACK, 10))
        self.button_list.append(Button(800, 535, 80, 50, "DFS T", 25, settings.WHITE, settings.BLACK, 10))
        self.button_list.append(Button(800, 590, 80, 50, "A* T", 25, settings.WHITE, settings.BLACK, 10))

        self.button_list.append(Button(900, 480, 80, 50, "BFS G", 25, settings.WHITE, settings.BLACK, 10))
        self.button_list.append(Button(900, 535, 80, 50, "DFS G", 25, settings.WHITE, settings.BLACK, 10))
        self.button_list.append(Button(900, 590, 80, 50, "A* G", 25, settings.WHITE, settings.BLACK, 10))

    def solve(self):
        """
            Applies the solution found by an agent to the game.
        """
        if len(self.road) > 0:
            stop = self.road.pop(0)
            self.tiles_grid = stop
            self.number_of_moves += 1
            # time.sleep(0.25)

    def check_player_move_off_grid(self, player, x, y):
        """
            Checks if the player character move off the grid.
        """
        if player == 1:
            return 0 > self.p1_pos[0] + y or self.p1_pos[0] + y >= settings.GAMESIZE[1] \
                or 0 > self.p1_pos[1] + x or self.p1_pos[1] + x >= settings.GAMESIZE[0]
        else:
            return 0 > self.p2_pos[0] - y or self.p2_pos[0] - y >= settings.GAMESIZE[1] \
                or 0 > self.p2_pos[1] - x or self.p2_pos[1] - x >= settings.GAMESIZE[0]

    def check_moves(self, x, y):
        """
            Checks if the moves are valid.
        """
        # If at least one of the players tries to move in a valid space, returns True.
        return not self.check_player_move_off_grid(1, x, y) \
            and self.tiles_grid[self.p1_pos[0] + y][self.p1_pos[1] + x] != 4 \
            or not self.check_player_move_off_grid(2, x, y) \
            and self.tiles_grid[self.p2_pos[0] - y][self.p2_pos[1] - x] != 4

    def move_players(self, x, y):
        """
            Moves the player characters.
        """
        if not self.check_moves(x, y):
            return

        self.number_of_moves += 1

        # If the timer has not started, start it.
        if not self.start_game:
            self.start_timer = True
            self.start_game = True

        # If the player character 1 and player character 2 try to move to the same cell, it merges them.
        if self.p1_pos[0] + y == self.p2_pos[0] - y and self.p1_pos[1] + x == self.p2_pos[1] - x:
            self.tiles_grid[self.p1_pos[0]][self.p1_pos[1]] = 0
            self.tiles_grid[self.p2_pos[0]][self.p2_pos[1]] = 0
            self.tiles_grid[self.p1_pos[0] + y][self.p1_pos[1] + x] = 3
        # If the player character 1 and player character 2 try to move to each other's cell,
        # it merges them in the place of player character 2.
        elif self.p1_pos[0] + y == self.p2_pos[0] and self.p1_pos[1] + x == self.p2_pos[1]:
            self.tiles_grid[self.p1_pos[0]][self.p1_pos[1]] = 0
            self.tiles_grid[self.p2_pos[0]][self.p2_pos[1]] = 3
        # If the player character 1 and player character 2 does not interact with each other, it performs the move.
        else:
            # If the player character 1's target cell is empty and not off grid, it moves the player character 1.
            if not self.check_player_move_off_grid(1, x, y) \
                    and self.tiles_grid[self.p1_pos[0] + y][self.p1_pos[1] + x] == 0:
                self.tiles_grid[self.p1_pos[0] + y][self.p1_pos[1] + x] = 1
                self.tiles_grid[self.p1_pos[0]][self.p1_pos[1]] = 0
                self.p1_pos = (self.p1_pos[0] + y, self.p1_pos[1] + x)
            # If the player character 2's target cell is empty and not off grid, it moves the player character 1.
            if not self.check_player_move_off_grid(2, x, y) \
                    and self.tiles_grid[self.p2_pos[0] - y][self.p2_pos[1] - x] == 0:
                self.tiles_grid[self.p2_pos[0] - y][self.p2_pos[1] - x] = 2
                self.tiles_grid[self.p2_pos[0]][self.p2_pos[1]] = 0
                self.p2_pos = (self.p2_pos[0] - y, self.p2_pos[1] - x)
        self.draw_tiles()

    def check_win(self):
        """
            Checks if the game is won.
        """
        for row in self.tiles_grid:
            for cell in row:
                if cell == 3:
                    return True
        return False

    @staticmethod
    def move_to_text(move):
        """
            Returns the moves as text.
        """
        if move == [1, 0]:
            return "Right"
        elif move == [-1, 0]:
            return "Left"
        elif move == [0, 1]:
            return "Down"
        elif move == [0, -1]:
            return "Up"
        else:
            return "Invalid"

    def print_agent_info(self, agent_name, agent):
        """
            Prints the agent info after it solved the game.
        """
        print("---" * 20)
        print(f"{agent_name} solved the level {self.level} in {self.agent_solve_time * 1000:.3f} milliseconds.\n")
        print(f"The number of moves is {len(self.moves)}.")
        print(f"The move sequence is:\n{list(map(self.move_to_text,self.moves))}\n")
        print(f"The nodes related statistics are:")
        agent.print_info()
        print("---" * 20)

    def events(self):
        """
            Game loop - events.
        """

        # Process input (events)
        for event in pygame.event.get():
            # Checks for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            # Checks for key press
            if not self.end_game and not self.agent_activated and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.move_players(1, 0)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.move_players(-1, 0)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.move_players(0, -1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.move_players(0, 1)

            # Checks for mouse click and gets mouse position
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Checks for button click
                for button in self.button_list:
                    if button.click(mouse_pos):
                        if button.text == "Reset":
                            self.new()
                        elif button.text == "1" or button.text == "2" or button.text == "3":
                            if button.text == "1":
                                self.level = 1
                            elif button.text == "2":
                                self.level = 2
                            elif button.text == "3":
                                self.level = 3
                            self.new()
                        elif not self.end_game and not self.agent_activated \
                                and (button.text == "BFS T" or button.text == "DFS T" or button.text == "A* T"):
                            if button.text == "BFS T":
                                agent = BFSAgent(self.tiles_grid)
                            elif button.text == "DFS T":
                                agent = DFSAgent(self.tiles_grid)
                            elif button.text == "A* T":
                                agent = AStarAgent(self.tiles_grid)
                            else:
                                continue
                            self.agent_activated = True
                            if not self.start_game:
                                self.start_timer = True
                                self.start_game = True
                            solving_start = time.time()
                            # The agent solves the game with tree search and returns the moves and the road.
                            # The moves are the sequence of moves to solve the game like [1, 0], [0, 1], etc.
                            # The road is the sequence of the game matrices to solve the game.
                            self.moves, self.road = agent.tree_solve()
                            self.agent_solve_time = time.time() - solving_start
                            self.print_agent_info(button.text, agent)
                        elif not self.end_game and not self.agent_activated \
                                and (button.text == "BFS G" or button.text == "DFS G" or button.text == "A* G"):
                            if button.text == "BFS G":
                                agent = BFSAgent(self.tiles_grid)
                            elif button.text == "DFS G":
                                agent = DFSAgent(self.tiles_grid)
                            elif button.text == "A* G":
                                agent = AStarAgent(self.tiles_grid)
                            else:
                                continue
                            self.agent_activated = True
                            if not self.start_game:
                                self.start_timer = True
                                self.start_game = True
                            solving_start = time.time()
                            # The agent solves the game with graph search and returns the moves and the road.
                            # The moves are the sequence of moves to solve the game like [1, 0], [0, 1], etc.
                            # The road is the sequence of the game matrices to solve the game.
                            self.moves, self.road = agent.graph_solve()
                            self.agent_solve_time = time.time() - solving_start
                            self.print_agent_info(button.text, agent)

    def update(self):
        """
            Game loop - update.
        """
        # Checks if the game is over
        if self.start_game:
            if self.check_win():
                self.start_game = False
                self.end_game = True

                # Saves the time high score
                if self.time_high_score[self.level - 1] > 0:
                    if self.elapsed_time < self.time_high_score[self.level - 1]:
                        self.time_high_score[self.level - 1] = self.elapsed_time
                        self.best_time = True
                else:
                    self.time_high_score[self.level - 1] = self.elapsed_time
                    self.best_time = True

                # Saves the move high score
                if self.move_high_score[self.level - 1] > 0:
                    if self.number_of_moves < self.move_high_score[self.level - 1]:
                        self.move_high_score[self.level - 1] = self.number_of_moves
                else:
                    self.move_high_score[self.level - 1] = self.number_of_moves

                self.save_score()

            # Starts the game timer
            if self.start_timer:
                self.timer = time.time()
                if self.agent_activated:
                    self.timer -= self.agent_solve_time
                self.start_timer = False

            self.elapsed_time = time.time() - self.timer if not (self.end_game and
                                                                 self.best_time) else self.time_high_score[self.level - 1]

        # Solves the game if agent buttons is pressed
        if self.agent_activated:
            self.solve()
            self.draw_tiles()

        self.all_sprites.update()

    def run(self):
        """
            Starts the game loop.
        """
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
