import random
import Predator
import Prey
import Obstacle
import math
import logging

class Environment:
  def __init__ (self, width, height, num_predator, num_prey):
    # logging: currently turned off
    # filename = "simulation.log"
    # logging.basicConfig(filename = filename, level = logging.DEBUG)
    
    #array to hold predator and prey objs
    self.predators = []
    self.preys = []

    self.mature_predators = []
    self.mature_preys = []

    self.width = width
    self.height = height

    self.num_predator = num_predator
    self.num_prey = num_prey

    # number of iterations where preds still alive
    self.iterations_pred = 0

    # Generation that last living pred belonged to
    self.max_gen_pred = 0

    # Are there any predators left in the environment?
    self.no_pred_left = False

    # predator neural nets
    self.pred_neural_nets = []

    # array to hold obstacles objs
    self.obstacles = []

    # initialize obstacles (for now the obstacles locations are input manually here)
    # note: top left corner of window is 0,0
    # (x_top, x_bot, y_top, y_bot)
    obs_1 = Obstacle.Obstacle(250, 150, 200, 400) # vertical spanning obstacle
    self.obstacles.append(obs_1)
    obs_2 = Obstacle.Obstacle(450 , 150, 400, 500) # horizontally spanning obstacle
    self.obstacles.append(obs_2)
    #initialize predators
    for z in range(0, num_predator):
      location = self.findEmptySpace(Predator.Predator.radius)
      new_pred = Predator.Predator(random.randint( 0, 359), location[0], location[1])
      self.predators.append(new_pred)
    #initialize prey
    for z in range(0, num_prey):    
      location = self.findEmptySpace(Prey.Prey.init_radius)
      new_prey = Prey.Prey(random.randint( 0, 359), location[0], location[1])
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
    print "could not find empty space"

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
    # collision with obstacles
    for obs in self.obstacles:
      if ( ((obs.x_bot - radius) <= x <= (obs.x_top - radius)) and ((obs.y_bot - radius) <= y <= (obs.y_top - radius)) ):
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
        return (prey.x, prey.y, prey.radius)
      elif ( (abs(predator.x - prey.x) < (10 * predator.radius)) and (abs(predator.y - prey.y) < (10 * predator.radius)) ):
        return (prey.x, prey.y, prey.radius)
      elif ( (abs(predator.x - prey.x) < (12 * predator.radius)) and (abs(predator.y - prey.y) < (12 * predator.radius)) ):
        return (prey.x, prey.y, prey.radius)
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

  # detects rectangle / circle intersection
  # returns the center of the obstacle
  def predator_sense_obs(self, predator):
    for obs in self.obstacles:
      pred_distance_x = abs(predator.x - obs.center[0])
      pred_distance_y = abs(predator.y - obs.center[1])

      if (pred_distance_x > (obs.width / 2 )):
        return obs.center
      if (pred_distance_y > (obs.height / 2 )):
        return obs.center
      if ( pred_distance_x <= (obs.width) / 2):
        return obs.center
      if ( pred_distance_y <= (obs.height) / 2):
        return obs.center
      corner_distance_sq = math.pow((pred_distance_x - (obs.width / 2)) , 2 ) + math.pow((pred_distance_y - (obs.height / 2)) , 2 )
      if (corner_distance_sq <= math.pow(predator.radius , 2)):
        return obs.center

  def predator_will_touch(self, predator):
    # check to see if the predator will touch a prey
    for prey in self.preys:
      if ((abs(predator.next_x - prey.x) < (2 * predator.radius)) and (abs(predator.next_y - prey.y) < (2 * predator.radius))):
        return prey
    return self

  def predator_is_touching(self, predator):
    # check to see if the predator is currently touching a prey
    for prey in self.preys:
      if ((abs(predator.x - prey.x) < (2 * predator.radius)) and (abs(predator.y - prey.y) < (2 * predator.radius))):
        return prey
    return self

  # function to allow preys to sense predators around them
  # through diffusion of smell
  def prey_sense_pred(self, prey):
    for pred in self.predators:
      if ( (abs(prey.x - pred.x) < (4 * prey.radius)) and (abs(prey.y - pred.y) < (6 * prey.radius)) ):
        return (pred.x, pred.y)
      elif ( (abs(prey.x - pred.x) < (6 * prey.radius)) and (abs(prey.y - pred.y) < (8 * prey.radius)) ):
        return (pred.x, pred.y)
      elif ( (abs(prey.x - pred.x) < (8 * prey.radius)) and (abs(prey.y - pred.y) < (10 * prey.radius)) ):
        return (pred.x, pred.y)
      else:
        continue
    return None

  # function to allow preys to sense predators around them
  # through diffusion of smell
  def prey_sense_prey(self, prey):
    for prey_to_sense in self.preys:
      if ( (abs(prey.x - prey_to_sense.x) < (4 * prey.radius)) and (abs(prey.y - prey_to_sense.y) < (6 * prey.radius)) ):
        return (prey_to_sense.x, prey_to_sense.y, prey_to_sense.radius)
      elif ( (abs(prey.x - prey_to_sense.x) < (6 * prey.radius)) and (abs(prey.y - prey_to_sense.y) < (8 * prey.radius)) ):
        return (prey_to_sense.x, prey_to_sense.y, prey_to_sense.radius)
      elif ( (abs(prey.x - prey_to_sense.x) < (8 * prey.radius)) and (abs(prey.y - prey_to_sense.y) < (10 * prey.radius)) ):
        return (prey_to_sense.x, prey_to_sense.y, prey_to_sense.radius)
      else:
        continue
    return None

  def update_environment(self):
    # UPDATE what the predators sense
    for pred in self.predators:
      prey_coordinate = self.predator_sense_prey(pred)
      # if predator senses a prey, change to hunting mode
      if (prey_coordinate is not None):
        pred.hunting = True
        # give predator the radius of the prey
        pred.prey_radius = prey_coordinate[2]
        # give the predator a general direction of where prey is
        pred.prey_direction = math.ceil(math.degrees(math.atan2(prey_coordinate[1] - pred.y, prey_coordinate[0] - pred.x)))

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
            break

        # print "Pred energy : "
        # print pred.energy

      else: # predator didn't sense any prey around it, change to idle mode
        # print "Predator senses nothing"
        pred.hunting = False
        # no prey, so give a random angle
        pred.prey_direction = random.randint(0, 359)
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

      #TODO
      # keep track of how many predators attacking that prey
      if (isinstance(pred.contact, Prey.Prey) and pred.move and pred.eat):
        pred.contact.num_atk_pred += 1

      # predator makes its action in the environment
      if pred.move:
        pred.x = pred.next_x
        pred.y = pred.next_y
      else:
        pred.next_x = pred.x
        pred.next_y = pred.y

    #TODO: modify these values when doing experiments
    for prey in self.preys:
      # whether atk was successful or not depends on the number of predators
      if (prey.num_atk_pred > 0):
        rand_num = random.randint(1, 100)
        if (prey.num_atk_pred == 1):
          # 95% chance of dying
          if (rand_num >= 95):
            prey.energy = 0
            prey.energy_per_pred = prey.max_energy / prey.num_atk_pred
        elif (prey.num_atk_pred == 2):
          # 97% chance of dying
          if (rand_num >= 97):
            prey.energy = 0
            prey.energy_per_pred = prey.max_energy / prey.num_atk_pred
        else:
          # 100% chance of dying
          prey.energy = 0
          prey.energy_per_pred = prey.max_energy / prey.num_atk_pred

    for pred in self.predators:
      pred.current_contact = self.predator_is_touching(pred)
      if (isinstance(pred.current_contact, Prey.Prey) and (pred.current_contact.energy == 0) and pred.eat):
        self.preys.remove(pred.current_contact)
        print "A predator KILLED a prey!"
        self.num_prey -= 1
        # location = self.findEmptySpace(Prey.Prey.init_radius)
        # new_prey = Prey.Prey(random.random() * 359, location[0], location[1])
        # self.preys.append(new_prey)
      pred.current_contact = None
      pred.contact = None


    # set new energy levels accordingly
    for pred in self.predators:
      if (isinstance(pred.contact, Prey.Prey) and pred.move and pred.eat):
        pred.energy += pred.contact.energy_per_pred
      # pred dies at age 30
      if (pred.age >= 40):
        pred.energy = 0

    # remove dead predators from the environment
    predators_temp = self.predators
    for pred in predators_temp:
      if (pred.energy <= 0):
        self.predators.remove(pred)
        self.num_predator -= 1
        print "A predator died!"

    # remove dead prey from the environment
    preys_temp = self.preys
    for prey in preys_temp:
      if (prey.energy <= 0):
        self.preys.remove(prey)
        self.num_prey -= 1
        # # when one prey dies, respawn another
        # location = self.findEmptySpace(Prey.Prey.radius)
        # new_prey = Prey.Prey(random.random() * 359, location[0], location[1])
        # self.preys.append(new_prey)
        # self.num_prey += 1

    # TODO: modify how prey sense and update themselves with direction
    # update what the prey sense
    for prey in self.preys:
      # if prey senses another prey, give direction and radius of other prey as input
      prey_coord = self.prey_sense_prey(prey)
      if (prey_coord is not None):
        # give prey the radius of the other prey
        prey.prey_radius = prey_coord[2]
        # give the prey a general direction of other prey
        prey.prey_direction = math.ceil(math.degrees(math.atan2(prey_coord[1] - prey.y, prey_coord[0] - prey.x)))


      # if prey senses a predator, change to escape mode
      pred_coord = self.prey_sense_pred(prey)
      if (pred_coord is not None):
        prey.senses_predator = True
        #TODO: CHANGE THIS PART
        # give the prey a general direction of the predator
        prey.pred_direction = math.ceil(math.degrees(math.atan2(pred_coord[1] - prey.y, pred_coord[0] - prey.x)))
        
        for i in xrange(1, 2, 1):
          inc_x = math.cos(prey.direction) * (1 * prey.radius)
          inc_y = math.sin(prey.direction) * (1 * prey.radius)
          # make sure the prey doesn't go out of bounds
          if (((prey.next_x + inc_x) < 0 ) or ((prey.next_x + inc_x) > self.width )):
            inc_x = inc_x * (-1.0)
          if (((prey.next_y + inc_y) < 0 ) or ((prey.next_y + inc_y) > self.height )):
            inc_y = inc_y * (-1.0)
          prey.next_x += inc_x
          prey.next_y += inc_y

      else:
        # prey did not sense any predators
        prey.senses_predator = False
        # give it a random direction
        prey.pred_direction = random.randint(0, 359)

        for i in xrange(1, 2, 1):
          inc_x_rand = math.cos(prey.direction) * (1.0 * prey.radius)
          inc_y_rand = math.sin(prey.direction) * (1.0 * prey.radius)
          # make sure the prey doesn't go out of bounds
          if (((prey.next_x + inc_x_rand) < 0 ) or ((prey.next_x + inc_x_rand) > self.width )):
            inc_x_rand = inc_x_rand * (-1.0)
          if (((prey.next_y + inc_y_rand) < 0 ) or ((prey.next_y + inc_y_rand) > self.height )):
            inc_y_rand = inc_y_rand * (-1.0)
          prey.next_x += inc_x_rand
          prey.next_y += inc_y_rand

      # run prey NN with new inputs
      prey.update()
      if (prey.want_to_eat):
        # prey doesn't move when eating, stays still
        prey.next_x = prey.x
        prey.next_y = prey.y
        
      if (prey.want_to_move):
        prey.x = prey.next_x
        prey.y = prey.next_y
      # prey dies at age 50
      if (prey.age >= 50):
        prey.energy = 0

    # put mature animats into the list of mature predators and preys
    for pred in self.predators:
      if (pred.age >= 15 and pred.not_mated):
        self.mature_predators.append(pred)

    for prey in self.preys:
      if (prey.age >= 15 and prey.not_mated):
        self.mature_preys.append(prey)

    # check to see if any predators can mate
    while (len(self.mature_predators) >= 2):
      parent1 = self.mature_predators.pop(0)
      parent2 = self.mature_predators.pop(0)
      parent1.not_mated = False
      parent2.not_mated = False
      # reproduce 2 - 4 offspring
      num_offspring = random.randint(1 ,3)
      for x in xrange(num_offspring):
        offspring_location = self.findEmptySpace(Predator.Predator.radius)
        offspring = Predator.Predator(random.random() * 359, offspring_location[0], offspring_location[1])
        # genetic recombination of parent's genotype
        for i in xrange(len(parent1.nn.params)):
          # 90% chance for each weight to be inherited from p1 or p2
          # 10% chance mutation where weight will be random
          if (random.randint(1,10) < 9):
            if (random.randint(0,1) > 0):
              offspring.nn.params[i] = parent1.nn.params[i]
            else:
              offspring.nn.params[i] = parent2.nn.params[i]
        # update offspring generation
        if (parent1.generation >= parent2.generation):
          offspring.generation = parent1.generation + 1
        else:
          offspring.generation = parent2.generation + 1
        self.predators.append(offspring)
        print "New pred offspring! gen is : %d" % offspring.generation
        self.num_predator += 1
    self.mature_predators = []

    # Gives you the max generation that predators survived until
    if (len(self.predators) > 0):
      # Iterations where predators still alive    
      self.iterations_pred += 1
      # Get max generation of pred
      self.predators.sort(key = lambda x: x.generation, reverse = True)
      self.max_gen_pred = self.predators[0].generation

    # check to see if any preys can mate
    while (len(self.mature_preys) >= 2):
      parent1 = self.mature_preys.pop(0)
      parent2 = self.mature_preys.pop(0)
      parent1.not_mated = False
      parent2.not_mated = False
      # reproduce 2 - 4 offspring
      num_offspring = random.randint(1,3)
      for x in xrange(num_offspring):
        offspring_location = self.findEmptySpace(Prey.Prey.init_radius)
        offspring = Prey.Prey(random.random() * 359, offspring_location[0], offspring_location[1])
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
    self.mature_preys = []

    # remove dead prey from the environment
    preys_temp = self.preys
    for prey in preys_temp:
      if (prey.energy <= 0):
        self.preys.remove(prey)
        self.num_prey -= 1

    # clear the old neural nets
    self.pred_neural_nets = []
    # save the surviving predators' neural nets
    for pred in self.predators:
      self.pred_neural_nets.append(pred.nn.params)
    # log the number of predator and prey after this iteration
    # logging.info("Num Pred:%d         Num Prey:%d" % (self.num_predator, self.num_prey))

