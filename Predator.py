from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
import Prey
import Obstacle
import Environment

class Predator:
  radius = 20
  def __init__(self, direction, x, y):
    #Neural network
    self.nn = FeedForwardNetwork()
    #Add layers
    inLayer = LinearLayer(14)
    hiddenLayer = SigmoidLayer(15)
    outLayer = LinearLayer(4)
    self.nn.addInputModule(inLayer)
    self.nn.addModule(hiddenLayer)
    self.nn.addOutputModule(outLayer)
    #Add connections
    in_to_hidden = FullConnection(inLayer, hiddenLayer)
    hidden_to_out = FullConnection(hiddenLayer, outLayer)

    self.nn.addConnection(in_to_hidden)
    self.nn.addConnection(hidden_to_out)
    #initialize NN
    self.nn.sortModules()
    
    # Energy - dies when reaches 0
    self.energy = 380

    # Location
    self.x = x
    self.y = y

    # direction / angle
    self.direction = direction

    # prey's directions. general direction to where prey is
    self.prey_directions = []

    # prey's radiuses
    self.prey_radiuses = []

    # other predator's direction. general direction to where the predator is
    self.pred_direction = 0

    # general direction of sensed obstacle
    self.obs_direction = 0

    # Sees prey, hunting mode
    # in hunting mode, predators can move faster, but also consumes more energy
    # if not in hunting mode, then idle mode
    self.hunting = False

    # tried to eat something last iteration, thus digesting now
    self.digesting = False

    # where to move to next
    self.next_x = x
    self.next_y = y

    # what the predator would come into contact with if moves to next_x, next_y
    self.contact = None

    # what the predator is currently in contact with
    self.current_contact = None

    # Age, reaches maturity at age 50
    self.age = 0

    # Generation, which generation this animat belongs to
    self.generation = 0

    # has it mated and reproduced yet?
    self.not_mated = True

    # output thresholds for decisions
    self.move_threshold = 0
    self.eat_threshold = 0

    # decisions for output
        # eating a prey gives +250 energy
    self.move = False
    self.eat = False

    # number of prey killed, used in reproduction
    self.num_prey_killed = 0

    # reproduction counter
    self.repro_counter = 0

  def update(self):
    # metabolism depends on which state the predator is in (hunting or idle)
    if (self.hunting is True):
      if (self.energy < 20):
        self.energy = 0
      else:
        self.energy -= 20
    else:
      if (self.energy < 10):
        self.energy = 0
      else:
        self.energy -= 10

    # Aging
    self.age += 1
    self.repro_counter += 1

    # Input vector
        # input values are determined by what the animat 
        # is seeing and / or touching
    input_vector = (
                    (2000 * int(self.hunting)), # remove hunting mode?
                    (2000 * int(isinstance(self.contact, Predator))),
                    (2000 * int(isinstance(self.contact, Prey.Prey))),
                    (2000 * int(isinstance(self.contact, Environment.Environment))),
                    (2000 * self.energy),
                    (2000 * self.direction),
                    (2000 * self.prey_directions[0]),
                    (2000 * self.prey_radiuses[0]),
                    (2000 * self.prey_directions[1]),
                    (2000 * self.prey_radiuses[1]),
                    (2000 * self.prey_directions[2]),
                    (2000 * self.prey_radiuses[2]),                                        
                    (2000 * self.pred_direction),
                    (2000 * self.obs_direction)
                    )

    # Activate the nn
    output_vector = self.nn.activate(input_vector)
    
    # move
    if (output_vector[0] > self.move_threshold):
      self.move = True
    else:
      self.move = False
    # eat
    if (output_vector[1] > self.eat_threshold):
      self.eat = True
    else:
      self.eat = False

    # direction: turn right (clockwise)
    self.direction -= output_vector[2]
    #direction: turn left (counter clockwise)
    self.direction += output_vector[3]

