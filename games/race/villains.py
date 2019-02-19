from collections import deque
import random

from .car import Car

def check_for_collisions(hero, villains):
    hero_points = hero.bounding_box()
    for v in villains:
        for point in hero_points:
            if v.is_point_in_car(point):
                return True
    return False


class Villains():
    def __init__(self):
        self.villains = deque()

    def __getitem__(self, index):
        return self.villains[index]

    def __len__(self):
        return len(self.villains)

    def random_add(self, hero):
        '''
        Randomly generates villains 50% of the time this is called
        '''
        allowed_x = [1, 5, 9]
        # 20 % change of villain generation
        generate = random.randint(1,2) % 1 == 0
        villain = Car(y=random.randint(0,5), x=allowed_x[random.randint(0,2)])
        if not generate and check_for_collisions(hero, [villain]):
            return

        try:
            last_villain = self.villains[-1]
            if check_for_collisions(villain, [last_villain]):
                return
            if (villain.x == 5 or villain.x !=5) and (villain.y + 9) > last_villain.y:
                return
            self.villains.append(villain)
        except IndexError:
            self.villains.append(villain)

    #TODO: control the speed of motion of villains
    def move(self, window):
        for v in self.villains:
            v.move(window, v.y+1, v.x)
    
    def remove(self, window):
        '''
        checks the first car in the list to see if it should be removed
        If its beyond the height of the window it is removed
        '''
        height,_ = window.getmaxyx()
        try:
            first_villain = self.villains[0]
            if (first_villain.y >= height - 4 ):
                self.villains.popleft().clear(window)
            return
        except IndexError:
            return

    def draw(self, window):
        for car in self.villains:
            car.draw(window)
