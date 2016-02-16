import math

class Obstacle:
  def __init__(self,x_top, x_bot, y_top, y_bot):
    # Location and dimension of the obstacle, rectangular shape
    self.x_top = x_top
    self.x_bot = x_bot
    self.y_top = y_top
    self.y_bot = y_bot
    
    # rough center of the obstacle, used for predator and preys for sensing
    self.center = ( (x_top + x_bot) / 2.0 , ((y_top + y_bot)/2.0) )

    self.width = x_top - x_bot
    self.height = y_bot - y_top