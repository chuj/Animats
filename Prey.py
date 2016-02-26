from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
import math

class Prey:
  # initial radius
  init_radius = 20
  # large radius
  large_radius = 25
  def __init__(self, direction, x, y):
    # radius
    self.radius = self.init_radius
    #Neural network
    self.nn = FeedForwardNetwork()
    #Add layers
    inLayer = LinearLayer(11)
    hiddenLayer = SigmoidLayer(12)
    outLayer = LinearLayer(5)
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
    self.energy = 350

    # Max Energy. the max amount of energy a prey can have
    self.max_energy = 500

    # Location
    self.x = x
    self.y = y

    # direction / angle
    self.direction = direction

    # Senses predator
    self.senses_predator = False

    # predator's general direction
    self.pred_direction = 0

    # other prey's general direction
    self.prey_direction = 0

    # other prey's radius
    self.prey_radius = 0

    # general direction of sensed obstacle
    self.obs_direction = 0

    # where to move to next
    self.next_x = x
    self.next_y = y

    # eat or not (eating regains energy)
    self.want_to_eat = False

    # move or not
    self.want_to_move = False

    # signal or not
    self.signal = False

    # if energy is less than 100, gets hungry status
    self.is_hungry = False

    # Age
    self.age = 0

    # output thresholds for decisions
    self.move_threshold = 0
    self.eat_threshold = 0
    self.signal_threshold = 0

    # direction of signal from other prey
    self.prey_signal_direction = 0

    # has it mated and reproduced yet?
    self.not_mated = True

    # number of attacking preds
    self.num_atk_pred = 0

    # energy per pred. how much energy each predator gains when eating this prey 
    self.energy_per_pred = 0

    # predator signal direction
    self.pred_signal_direction = 0

    # what prey is touching
    self.is_touching = None

  def update(self):
    # metabolism depends on which state the prey is in (escaping from predator, idle)
    if (self.senses_predator is True):
      if (self.energy < 25):
        self.energy = 0
      else:
        self.energy -= 25
    else: # idle mode, consumes less energy
      if (self.energy < 10):
        self.energy = 0
      else:
        self.energy -= 10

    if (self.energy < 100):
      self.is_hungry = True
    else:
      self.is_hungry = False
    
    # Aging
    self.age += 1


    
    # Input vector
        # input values are determined by what the animat 
        # is seeing and / or touching
    input_vector = (
                    (2000 * int(self.senses_predator)),
                    (2000 * self.energy),
                    (2000 * self.is_hungry),
                    (2000 * self.direction),
                    (2000 * self.pred_direction),
                    (2000 * self.prey_direction),
                    (2000 * self.prey_radius),
                    (2000 * self.age),
                    (2000 * self.obs_direction),
                    (2000 * self.prey_signal_direction),
                    (2000 * int( isinstance(self.is_touching, Prey)) )
                    )

    # Activate the nn
    output_vector = self.nn.activate(input_vector)
    # move
    if (output_vector[0] > self.move_threshold):
      self.want_to_move = True
    else:
      self.want_to_move = False
    # eat
    if (output_vector[1] > self.eat_threshold):
      self.want_to_eat = True
    else:
      self.want_to_eat = False
    # direction: turn right (clockwise)
    self.direction -= output_vector[2]
    #direction: turn left (counter clockwise)
    self.direction += output_vector[3]

    # signal other preys
    if (output_vector[4] > self.signal_threshold):
      self.signal = True
    else:
      self.signal = False

    if (self.want_to_eat):
      if (self.energy >= 400):
        self.energy = 500
      else:
        self.energy += 100
      self.is_hungry = False



