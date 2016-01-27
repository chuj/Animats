from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
import math

class Prey:
  radius = 5
  def __init__(self, direction, x, y):
    #Neural network
    self.nn = FeedForwardNetwork()
    #Add layers
    inLayer = LinearLayer(3)
    hiddenLayer = SigmoidLayer(4)
    outLayer = LinearLayer(2)
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
    self.energy = 500

    # Location
    self.x = x
    self.y = y

    # Senses predator
    self.senses_predator = False

    # where to move to next to escape from predator
    self.escape_x = 0
    self.escape_y = 0

    # where to move to next if no food or predator, random movement
    self.next_x = 0
    self.next_y = 0

    # eat or not (eating regains energy)
    self.want_to_eat = False

    # move or not
    self.want_to_move = False

    # if energy is less than 100, gets hungry status
    self.is_hungry = False

    # Age
    self.age = 0

    # output thresholds for decisions
    self.move_threshold = 0
    self.eat_threshold = 0

    # has it mated and reproduced yet?
    self.not_mated = True

  def update(self):
    # metabolism depends on which state the prey is in (escaping from predator, idle)
    if (self.senses_predator is True):
      if (self.energy < 50):
        self.energy = 0
      else:
        self.energy -= 50
    else: # idle mode, consumes less energy
      if (self.energy < 25):
        self.energy = 0
      else:
        self.energy -= 25

    if (self.energy < 100):
      self.is_hungry = True
    
    # Aging
    self.age += 1
    
    # Input vector
        # input values are determined by what the animat 
        # is seeing and / or touching
    input_vector = (
                    (2000 * int(self.senses_predator)),
                    (2000 * self.energy),
                    (2000 * self.is_hungry)
                    )

    # Activate the nn
    output_vector = self.nn.activate(input_vector)

    if (output_vector[0] > self.move_threshold):
      self.want_to_move = True
    if (output_vector[1] > self.eat_threshold):
      self.want_to_eat = True
    if (self.want_to_eat):
      if (self.energy >= 400):
        self.energy = 500
      else:
        self.energy += 100
      self.is_hungry = False



