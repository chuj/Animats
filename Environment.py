import random
import Predator
import Prey
import math
import logging

class Environment:
  def __init__ (self, width, height, num_predator, num_prey):
    # logging
    filename = "simulation.log"
    logging.basicConfig(filename = filename, level = logging.DEBUG)
    #array to hold predator and prey objs
    self.predators = []
    self.preys = []

    self.mature_predators = []
    self.mature_preys = []

    self.width = width
    self.height = height

    self.num_predator = num_predator
    self.num_prey = num_prey

    # self.iterations = 0

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
  # also returns the direction the prey is facing
  def predator_sense_prey(self, predator):
    for prey in self.preys:
      if ( (abs(predator.x - prey.x) < (8 * predator.radius)) and (abs(predator.y - prey.y) < (8 * predator.radius)) ):
        return (prey.x, prey.y)
      elif ( (abs(predator.x - prey.x) < (10 * predator.radius)) and (abs(predator.y - prey.y) < (10 * predator.radius)) ):
        return (prey.x, prey.y)
      elif ( (abs(predator.x - prey.x) < (12 * predator.radius)) and (abs(predator.y - prey.y) < (12 * predator.radius)) ):
        return (prey.x, prey.y)
      else:
        continue
    return None

  # TODO: modify the steps here
  def predator_sense_pred(self, predator):
    for pred in self.predators:
      if ( (abs(predator.x - pred.x) < (8 * predator.radius)) and (abs(predator.y - pred.y) < (8 * predator.radius)) ):
        return (pred.x, pred.y)
      elif ( (abs(predator.x - pred.x) < (10 * predator.radius)) and (abs(predator.y - pred.y) < (10 * predator.radius)) ):
        return (pred.x, pred.y)
      elif ( (abs(predator.x - pred.x) < (12 * predator.radius)) and (abs(predator.y - pred.y) < (12 * predator.radius)) ):
        return (pred.x, pred.y)
      else:
        continue
    return None

  def predator_will_touch(self, predator):
    # check to see if the predator is touching a prey
    for prey in self.preys:
      if ((abs(predator.next_x - prey.x) < (2 * predator.radius)) and (abs(predator.next_y - prey.y) < (2 * predator.radius))):
        return prey
    return self

  # function to allow preys to sense the world around them
  # through diffusion of smell
  def prey_sense_pred(self, prey):
    for pred in self.predators:
      if ( (abs(prey.x - pred.x) < (6 * prey.radius)) and (abs(prey.y - pred.y) < (6 * prey.radius)) ):
        return (pred.x, pred.y)
      elif ( (abs(prey.x - pred.x) < (8 * prey.radius)) and (abs(prey.y - pred.y) < (8 * prey.radius)) ):
        return (pred.x, pred.y)
      elif ( (abs(prey.x - pred.x) < (10 * prey.radius)) and (abs(prey.y - pred.y) < (10 * prey.radius)) ):
        return (pred.x, pred.y)
      else:
        continue
    return None

  def update_environment(self):
    # check to see if any predators can mate
    while (len(self.mature_predators) >= 2):
      parent1 = self.mature_predators.pop(0)
      parent2 = self.mature_predators.pop(0)
      parent1.not_mated = False
      parent2.not_mated = False
      # reproduce 2 - 4 offspring
      num_offspring = random.randint(2 ,4)
      for x in xrange(num_offspring):
        offspring_location = self.findEmptySpace(Predator.Predator.radius)
        offspring = Predator.Predator(random.random() * 360, offspring_location[0], offspring_location[1])
        # genetic recombination of parent's genotype
        for i in xrange(len(parent1.nn.params)):
          # 90% chance for each weight to be inherited from p1 or p2
          # 10% chance mutation where weight will be random
          if (random.randint(1,10) < 9):
            if (random.randint(0,1) > 0):
              offspring.nn.params[i] = parent1.nn.params[i]
            else:
              offspring.nn.params[i] = parent2.nn.params[i]
        self.predators.append(offspring)
        # print "New pred offspring!"
        self.num_predator += 1

    # UPDATE what the predators sense
    for pred in self.predators:
      prey_coordinate = self.predator_sense_prey(pred)
      # if predator senses a prey, change to hunting mode
      if (prey_coordinate is not None):
        pred.hunting = True
        # give the predator a general direction of where prey is
        pred.prey_direction = math.ceil(math.degrees(math.atan2(prey_coordinate[1] - pred.y, prey_coordinate[0] - pred.x)))

        # if predator can reach the prey in one turn
        # TODO: CHANGE THIS PART
        #check each pred step to see if it touches the prey
        # for loop going from steps 1 2 3
          #check each step to see if collision with prey
            #if collision, then move to that step
            # return
        # ADJUST these values for the for loop later
        for i in xrange(1, 3, 1):
          inc_x = math.cos(pred.direction) * (1 * pred.radius)
          inc_y = math.sin(pred.direction) * (1 * pred.radius)
          # make sure the pred doesn't go out of bounds
          if (((pred.next_x + inc_x) < 0 ) or ((pred.next_x + inc_x) > self.width )):
            inc_x = inc_x * (-1.0)
          if (((pred.next_y + inc_y) < 0 ) or ((pred.next_y + inc_y) > self.height )):
            inc_y = inc_y * (-1.0)
          pred.next_x += inc_x
          pred.next_y += inc_y
          pred.contact = self.predator_will_touch(pred)
          if (isinstance(pred.contact, Prey.Prey)):
            return

########## OLD CODE

        # distance_to_prey = math.sqrt((pred.x - prey_coordinate[0])**2 + (pred.y - prey_coordinate[1])**2 )
        # if (distance_to_prey <= (4.0 * pred.radius)):
        #   pred.next_x = prey_coordinate[0]
        #   pred.next_y = prey_coordinate[1]
        # else: 
        # # predator can't reach prey in one turn, so move as close as it can to prey
        #   angle = (math.atan2(prey_coordinate[1] - pred.y, prey_coordinate[0] - pred.x))
        #   inc_x = math.cos(angle) * (4.0 * pred.radius) 
        #   inc_y = math.sin(angle) * (4.0 * pred.radius)
        #   pred.next_x = pred.x + inc_x
        #   pred.next_y = pred.y + inc_y

#####################

      else: # predator didn't sense any prey around it, change to idle mode
        # print "Predator senses nothing"
        pred.hunting = False
        # no prey, so give a random angle
        pred.prey_direction = math.radians(random.randint(0, 359))
        # no prey, randomly decides how much to move      
        inc_x = math.cos(pred.direction) * ((random.randint(1, 2)) * pred.radius)
        inc_y = math.sin(pred.direction) * ((random.randint(1, 2)) * pred.radius)

        # make sure the animat doesn't go out of bounds
        if (((pred.x + inc_x) < 0 ) or ((pred.x + inc_x) > self.width )):
          inc_x = inc_x * (-1.0)
        if (((pred.y + inc_y) < 0 ) or ((pred.y + inc_y) > self.height )):
          inc_y = inc_y * (-1.0)
        pred.next_x += inc_x
        pred.next_y += inc_y
      # update pred.contact
      pred.contact = self.predator_will_touch(pred)
      
      # check to see if predator senses another pred
      pred_coordinate = self.predator_sense_pred(pred)
      if (pred_coordinate is not None):
        # if another predator is sensed, give our pred the general direction
        pred.pred_direction = math.ceil(math.degrees(math.atan2(pred_coordinate[1] - pred.y, pred_coordinate[0] - pred.x)))


      # run predator NN with new inputs
      pred.update()
      # predator makes its action in the environment
      if pred.move:
        pred.x = pred.next_x
        pred.y = pred.next_y
      if pred.eat: 
        if (isinstance(pred.contact, Prey.Prey)):
          self.preys.remove(pred.contact)
          location = self.findEmptySpace(Prey.Prey.radius)
          new_prey = Prey.Prey(random.random() * 360, location[0], location[1])
          self.preys.append(new_prey)
        pred.contact = None
      if (pred.age >= 15 and pred.not_mated):
        self.mature_predators.append(pred)
      # pred dies at age 30
      if (pred.age >= 30):
        pred.energy = 0

    # remove dead predators from the environment
    predators_temp = self.predators
    for pred in predators_temp:
      if (pred.energy <= 0):
        self.predators.remove(pred)
        self.num_predator -= 1

    # check to see if any preys can mate
    while (len(self.mature_preys) >= 2):
      parent1 = self.mature_preys.pop(0)
      parent2 = self.mature_preys.pop(0)
      parent1.not_mated = False
      parent2.not_mated = False
      # reproduce 2 - 4 offspring
      num_offspring = random.randint(1,2)
      for x in xrange(num_offspring):
        offspring_location = self.findEmptySpace(Prey.Prey.radius)
        offspring = Prey.Prey(random.random() * 360, offspring_location[0], offspring_location[1])
        # genetic recombination of parent's genotype
        for i in xrange(len(parent1.nn.params)):
          # 90% chance for each weight to be inherited from p1 or p2
          # 10% chance mutation where weight will be random
          if (random.randint(1,10) < 9):
            if (random.randint(0,1) > 0):
              offspring.nn.params[i] = parent1.nn.params[i]
            else:
              offspring.nn.params[i] = parent2.nn.params[i]
        self.preys.append(offspring)
        self.num_prey += 1

    # TODO: modify how prey sense and update themselves with direction
    # update what the prey sense
    for prey in self.preys:
      # if prey senses a predator, change to escape mode
      pred_coord = self.prey_sense_pred(prey)
      if (pred_coord is not None):
        prey.senses_predator = True
        angle_escape = (math.atan2(pred_coord[1] - prey.y, pred_coord[0] - prey.x))
        inc_x_escape = math.cos(angle_escape) * (3.0 * prey.radius) 
        inc_y_escape = math.sin(angle_escape) * (3.0 * prey.radius)
        # make sure the prey doesn't go out of bounds
        if (((prey.x + inc_x_escape) < 0 ) or ((prey.x + inc_x_escape) > self.width )):
          inc_x_escape = inc_x_escape * (-1.0)
        if (((prey.y + inc_y_escape) < 0 ) or ((prey.y + inc_y_escape) > self.height )):
          inc_y_escape = inc_y_escape * (-1.0)
        prey.escape_x = prey.x + inc_x_escape
        prey.escape_y = prey.y + inc_y_escape
      else:
        # prey did not sense any predators
        prey.senses_predator = False
        # move in random direction
        rand_angle = math.radians(random.randint(0, 360))
        inc_x_rand = math.cos(rand_angle) * (2.0 * prey.radius)
        inc_y_rand = math.sin(rand_angle) * (2.0 * prey.radius)
        # make sure the animat doesn't go out of bounds
        if (((prey.x + inc_x_rand) < 0 ) or ((prey.x + inc_x_rand) > self.width )):
          inc_x_rand = inc_x_rand * (-1.0)
        if (((prey.y + inc_y_rand) < 0 ) or ((prey.y + inc_y_rand) > self.height )):
          inc_y_rand = inc_y_rand * (-1.0)
        prey.next_x = prey.x + inc_x_rand
        prey.next_y = prey.y + inc_y_rand

      # run prey NN with new inputs
      prey.update()
      if (prey.want_to_eat):
        # prey doesn't move when eating, stays still
        prey.next_x = prey.x
        prey.next_y = prey.y
        prey.escape_x = prey.x
        prey.escape_y = prey.y
      if (prey.want_to_move):
        if (prey.senses_predator):
          prey.x = prey.escape_x
          prey.y = prey.escape_y
        else:
          prey.x = prey.next_x
          prey.y = prey.next_y
      if (prey.age >= 30 and prey.not_mated):
        self.mature_preys.append(prey)
      # prey dies at age 30
      if (prey.age >= 50):
        prey.energy = 0

    # remove dead prey from the environment
    preys_temp = self.preys
    for prey in preys_temp:
      if (prey.energy <= 0):
        self.preys.remove(prey)
        self.num_prey -= 1

    # log the number of predator and prey after this iteration
    logging.info("Num Pred:%d         Num Prey:%d" % (self.num_predator, self.num_prey))

