from collections import namedtuple

Point = namedtuple('Point', ['y', 'x'])


def rotate_point_clockwise(point, origin):
    '''
    Performs a 90 degree rotation about relative origin
    Then adds the vector to get coordinates in global system
    '''
    return Point(y=-point.x+origin.y, x=point.y+origin.x)


class Shape:

    def __init__(self, shape, boundingbox):
        self.shape = shape
        self.boundingbox = boundingbox

    def move_down(self):
        self.shape = [Point(y=coord.y+1, x=coord.x) for coord in self.shape]
        self.boundingbox = [Point(y=coord.y+1, x=coord.x)
                            for coord in self.boundingbox]

    def rotate_clockwise(self):
        [bb_y, bb_x] = self.get_shape_center()
        origin = Point(y=bb_y, x=bb_x)
        shape_relative = [Point(y=coord.y-bb_y, x=coord.x-bb_x)
                          for coord in self.shape]
        boundingbox_relative = [Point(y=coord.y-bb_y, x=coord.x-bb_x)
                                for coord in self.boundingbox]
        self.shape = [rotate_point_clockwise(coord, origin)
                      for coord in shape_relative]
        self.boundingbox = [rotate_point_clockwise(coord, origin)
                            for coord in boundingbox_relative]

    def get_shape_center(self):
        bb_y = (self.boundingbox[0].y + self.boundingbox[2].y) / 2
        bb_x = (self.boundingbox[0].x + self.boundingbox[1].x) / 2
        return (bb_y, bb_x)


class Zed(Shape):

    def __init__(self, y=0, x=0):
        shape = [
                Point(y, x), Point(y, x+1),
                Point(y+1, x+1), Point(y+1, x+2)
                ]
        boundingbox = [
                Point(y, x), Point(y, x+2),
                Point(y+1, x), Point(y+1, x+2)
                ]
        super(Zed, self).__init__(shape, boundingbox)


class L(Shape):

    def __init__(self, y=0, x=0):
        shape = [
                Point(y, x),
                Point(y+1, x),
                Point(y+2, x), Point(y+2, x+1)
                ]
        boundingbox = [
                Point(y, x), Point(y, x+1),
                Point(y+2, x), Point(y+2, x+1)
                ]
        super(L, self).__init__(shape, boundingbox)


class Box(Shape):

    def __init__(self, y=0, x=0):
        shape = [
                Point(y, x), Point(y, x+1),
                Point(y+1, x), Point(y+1, x+1)
                ]
        super(Box, self).__init__(shape, shape)


class Tee(Shape):

    def __init__(self, y=0, x=0):
        shape = [
                Point(y, x),
                Point(y+1, x), Point(y+1, x+1),
                Point(y+2, x)
                ]
        boundingbox = [
                Point(y, x), Point(y, x+1),
                Point(y+2, x), Point(y+2, x+1)
                ]
        super(Tee, self).__init__(shape, boundingbox)


shapes = [Zed, L, Box, Tee]
