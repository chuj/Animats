import random
import Predator
import Prey

class Environment:
  def __init__ (self, width, height, num_predator, num_prey):
    #array to hold predator and prey objs
    self.predators = []
    self.preys = []

    self.width = width
    self.height = height

    self.num_predator = num_predator
    self.num_prey = num_prey

    #initialize predators
    for z in range(0, num_predator):
      location = self.findEmptySpace(Predator.Predator.radius)
      new_pred = Predator.Predator(random.random() * 360, location[0], location[1])
      self.predators.append(new_pred)
    #initialize prey
    for z in range(0, num_prey):    
      location = self.findEmptySpace(Prey.Prey.radius)
      new_prey = Prey.Prey(random.random() * 360, location[0], location[1])
      self.preys.append(new_prey)

  def findEmptySpace(self, radius):
    x_placements = range(0, self.width, radius)
    y_placements = range(0, self.height, radius)
    # choose a random x_placements and y_placements
    random.shuffle(x_placements)
    random.shuffle(y_placements)
    for x in x_placements:
      for y in y_placements:
        if (self.collisionFree(x, y, radius)):
          return (x, y)

  #returns true if no collision, false if collision
  def collisionFree(self, x, y, radius):
    # check to see it's within the bounds of the environment
    if (((x - radius) < 0) or ((x + radius) > self.width)):
      return False
    if (((y - radius) < 0) or ((y + radius) > self.height)):
      return False
    # collision with other predators
    for predator in self.predators:
      if ( (abs(x - predator.x) < (2 * radius)) and (abs(y - predator.y) < (2 * radius))):
        return False
    # collision with prey
    for prey in self.preys:
      if ( (abs(x - prey.x) < (2 * radius)) and (abs(y - prey.y) < (2 * radius))):
        return False
    # the position is collision free
    return True


#define size of Environment
#define methods to allow animats to see
#define collision rules when animats run into the border
#define collision rules for animats running into other animats?
#initiate and create the animats
