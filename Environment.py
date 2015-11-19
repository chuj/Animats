import random
import Predator
import Prey
import math

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
      if ((abs(x - predator.x) < (2 * radius)) and (abs(y - predator.y) < (2 * radius))):
        return False
    # collision with prey
    for prey in self.preys:
      if ((abs(x - prey.x) < (2 * radius)) and (abs(y - prey.y) < (2 * radius))):
        return False
    # the position is collision free
    return True

  # function to allow predators to sense the world around them
  # through diffusion of smell
  # prey that are closer, thus stronger smell, are prioritized
  def predator_sense_env(self, predator):
    for prey in self.preys:
      if ( (abs(predator.x - prey.x) < (4 * radius)) and (abs(predator.y - prey.y) < (4 * radius)) )
        return (prey.x, prey.y)
      elif ( (abs(predator.x - prey.x) < (6 * radius)) and (abs(predator.y - prey.y) < (6 * radius)) )
        return (prey.x, prey.y)
      elif ( (abs(predator.x - prey.x) < (8 * radius)) and (abs(predator.y - prey.y) < (8 * radius)) )
        return (prey.x, prey.y)
      else
        return None

  def predator_is_touching(self, predator):
    # check to see if the predator is touching another predator
    for pred in self.predators:
      if ((abs(predator.x - pred.x) < (2 * Predator.radius)) and (abs(predator.y - pred.y) < (2 * Predator.radius))):
        return pred
    # check to see if the predator is touching a prey
    for prey in self.preys:
      if ((abs(predator.x - prey.x) < (2 * Predator.radius)) and (abs(predator.y - prey.y) < (2 * Predator.radius))):
        return prey
    return self


  # function to allow preys to sense the world around them
  # through diffusion of smell
  #def prey_sense_env(self, prey):

  def update_environment(self):
    # update what the predators sense
    for pred in self.predators:
      coordinate = predator_sense_env(pred)
      # if predator senses a prey, change to hunting mode
      if (coordinate is not None):
        pred.hunting = True
        # if predator can reach the prey in one turn, change to caught_prey mode
        distance_to_prey = math.sqrt((pred.x - coordinate[0])**2 + (pred.x - coordinate[0])**2 )
        if (distance_to_prey <= (4.0 * radius)):
          pred.next_x = coordinate[0]
          pred.next_y = coordinate[1]
        else # predator can't reach prey in one turn, so move as close as it can to prey
          angle = (math.atan2(coordinate[1] - pred.y, coordinate[0] - pred.x))
          inc_x = math.cos(angle) * (4.0 * radius) 
          inc_y = math.sin(angle) * (4.0 * radius)
          pred.next_x = pred.x + inc_x
          pred.next_y = pred.y + inc_y

      else # predator didn't sense any prey around it, change to idle mode
        pred.hunting = False
        # move in random direction
        rand_angle = math.radians(random.randint(0, 360))
        inc_x = math.cos(rand_angle) * (2.0 * radius)
        inc_y = math.sin(rand_angle) * (2.0 * radius)
        # make sure the animat doesn't go out of bounds
        if (((pred.x + inc_x) < 0 ) or ((pred.x + inc_x) > self.width )):
          inc_x = inc_x * (-1.0)
        if (((pred.y + inc_y) < 0 ) or ((pred.y + inc_y) > self.height )):
          inc_y = inc_y * (-1.0)
        pred.next_x = pred.x + inc_x
        pred.next_y = pred.y + inc_y
      # update pred.contact
      pred.contact = predator_is_touching(pred)
      # run predator NN with new inputs
      pred.update()
      # predator makes its action in the environment
      





    # update what the prey sense










