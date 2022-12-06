# https://www.redblobgames.com/grids/hexagons/#basics

import numpy as np
import math
import cv2
import random

class HexGameBoard():
    """ An pseudo-infinite hexagonal grid. 
    
    Axial coordinates are used to represent tiles in the hexagonal grid. Hexagons are assumed
    to have the "pointy-top" configuration:
    
     /\
    |  |
     \/
    
    """
    def __init__(self, view_shape=None, hex_size=None):
        # pixel size of each hexagonal tile at render. This is defined as the radius of the outer circle of the hexagon
        self.HEX_SIZE = hex_size

        # As a pseudo-infinite grid is used, @param view_shape only specifies how to view this grid.
        # The view dimensions will only be used in rendering the board to the screen.
        x, y = map(lambda x: x - 1, view_shape)
        self.VIEW_HORIZONTAL = x
        self.VIEW_VERTICAL = y

        # stores "ON" hexagons
        self.board = {} 

    def set_hex(self, hexagon, val=1):
        """ Sets the value of a given hexagon. Default set value is 1 ("ON").
        
        Axial coordinates are used to represent hexagonal tiles.
        """
        q, r = hexagon
        if val:
            self.board[(q, r)] = val
        else:
            del self.board[(q, r)]

    def render_board(self):
        horizontal_spacing = int(math.sqrt(3) * self.HEX_SIZE)
        vertical_spacing = int(3/2 * self.HEX_SIZE)

        render_size = (vertical_spacing * self.VIEW_VERTICAL, horizontal_spacing * self.VIEW_HORIZONTAL)
        render_bg = np.zeros(render_size, dtype="uint8") # greyscale only

        for hexagon in self.board.keys():
            center = self.hex_to_pixel(hexagon)
            corners = self.get_hex_corners(center)

            colour = 255 if self.board[hexagon] == 1 else 128
            cv2.fillPoly(render_bg, [corners], colour)
                
        
        cv2.imshow("_", render_bg)
        cv2.waitKey(0)

    def hex_to_pixel(self, hexagon):
        q, r = hexagon
        x = self.HEX_SIZE * (math.sqrt(3) * q + (math.sqrt(3)/2 * r))
        y = self.HEX_SIZE * 3/2 * r
        return x, y

    def get_hex_corners(self, center):
        """ gets all hexagon corners given a center and global hex size"""
        x, y = center
        corners = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            corners.append(
                (x + self.HEX_SIZE * math.cos(angle_rad),
                y + self.HEX_SIZE * math.sin(angle_rad))
            )
        return np.array(corners, np.int32)

    def get_Moore_neighbours(self, hexagon):
        directional_vectors = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

        q, r = hexagon
        neighbours = []
        for vq, vr in directional_vectors:
            neighbours.append((q + vq, r + vr))

        return neighbours

    def random_board(view_shape=None, hex_size=None, p_dead=0.8):
        board = HexGameBoard(view_shape=view_shape, hex_size=hex_size)

        for r in range(board.VIEW_VERTICAL + 1):
            for q in range(-board.VIEW_VERTICAL // 2, board.VIEW_HORIZONTAL + 1):
                rand = random.random()
                if rand >= p_dead:
                    board.set_hex((q, r)) 

        return board

