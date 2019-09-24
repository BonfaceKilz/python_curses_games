import random
import curses

from collections import namedtuple

Point = namedtuple('Point', ['x_pos', 'y_pos'])


def initial_snake(width, height):
    snake_x = width // 4
    snake_y = height // 2
    return [
        Point(x_pos=snake_x, y_pos=snake_y),
        Point(x_pos=snake_x - 1, y_pos=snake_y),
        Point(x_pos=snake_x - 2, y_pos=snake_y),
    ]


def initial_food(width, height):
    return Point(x_pos=width // 2, y_pos=height // 2)


class Snake(object):
    SCOREHEIGHT = 4
    MOTIONKEYS = (curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT,
                  curses.KEY_RIGHT, ord('j'), ord('k'), ord('h'), ord('l'))

    def __init__(self, stdscreen):
        curses.curs_set(0)
        self.height, self.width = stdscreen.getmaxyx()
        self.create_score_window()
        self.create_game_window()
        self.snake = initial_snake(self.width, self.height)
        self.food = initial_food(self.width, self.height)
        self.game_window.addch(self.food.y_pos, self.food.x_pos, curses.ACS_PI)
        self.update_score(0)

    def create_score_window(self):
        self.score_window = curses.newwin(self.SCOREHEIGHT, self.width, 0, 0)
        self.score_window.border(0, 0, 0, 0, 0, 0, 0, 0)

    def create_game_window(self):
        self.game_window = curses.newwin(self.height - self.SCOREHEIGHT,
                                         self.width, self.SCOREHEIGHT, 0)
        self.game_window.keypad(1)
        self.game_window.timeout(100)

    def update_score(self, score):
        score_message = 'Score: {}'.format(score)
        height, width = self.score_window.getmaxyx()
        self.score_window.addstr(height // 2, width // 2, score_message)
        self.score_window.refresh()

    def snake_beyond_boundaries_or_hit_itself(self):
        return (self.snake[0].y_pos in [0, self.height]
                or self.snake[0].x_pos in [0, self.width]
                or self.snake[0] in self.snake[1:])

    def move_snake(self, key):
        new_head = Point(x_pos=self.snake[0].x_pos, y_pos=self.snake[0].y_pos)
        if key in [curses.KEY_DOWN, ord('j')]:
            new_head = new_head._replace(y_pos=new_head.y_pos + 1)
        if key in [curses.KEY_UP, ord('k')]:
            new_head = new_head._replace(y_pos=new_head.y_pos - 1)
        if key in [curses.KEY_LEFT, ord('h')]:
            new_head = new_head._replace(x_pos=new_head.x_pos - 1)
        if key in [curses.KEY_RIGHT, ord('l')]:
            new_head = new_head._replace(x_pos=new_head.x_pos + 1)
        self.snake.insert(0, new_head)

    def new_food(self):
        while True:
            new_food = Point(x_pos=random.randint(1, self.width - 1),
                             y_pos=random.randint(
                                 1, self.height - self.SCOREHEIGHT - 1))
            if new_food not in self.snake:
                return new_food

    def eat_food(self):
        if self.snake[0] == self.food:
            self.food = self.new_food()
            return True
        return False

    def pause(self):
        while self.game_window.getch() != ord('p'):
            continue

    def loop(self):
        # Initial direction of snake
        key = curses.KEY_RIGHT
        score = 0
        while True:
            next_key = self.game_window.getch()
            # Quitting the game
            if next_key == ord('q'):
                break
            if next_key == ord('p'):
                self.pause()

            if next_key in self.MOTIONKEYS:
                key = next_key

            if self.snake_beyond_boundaries_or_hit_itself():
                return
            self.move_snake(key)
            if self.eat_food():
                score = score + 1
                self.update_score(score)
                self.game_window.addch(self.food.y_pos, self.food.x_pos,
                                       curses.ACS_PI)
            else:
                tail = self.snake.pop()
                self.game_window.addch(tail.y_pos, tail.x_pos, ' ')
                self.game_window.addch(self.snake[0].y_pos,
                                       self.snake[0].x_pos, curses.ACS_CKBOARD)


def snake_game(stdscreen):
    snake = Snake(stdscreen)
    snake.loop()


if __name__ == '__main__':
    curses.wrapper(snake_game)
