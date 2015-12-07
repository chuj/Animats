from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
import Prey
import Environment

class Predator:
  radius = 20
  def __init__(self, direction, x, y):
    # # size of predator
    # self.radius = 20 
    #Neural network
    self.nn = FeedForwardNetwork()
    #Add layers
    inLayer = LinearLayer(5)
    hiddenLayer = SigmoidLayer(6)
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
    
    # Which direction it's facing- NSWE
    self.direction = direction

    # Location
    self.x = x
    self.y = y

    # Sees prey, hunting mode
    # in hunting mode, predators can move faster, but also consumes more energy
    # if not in hunting mode, then idle mode
    self.hunting = False

    # where to move to next
    self.next_x = 0
    self.next_y = 0

    # what the predator would come into contact with if moves to next_x, next_y
    self.contact = None

    # Age
    self.age = 0

    # Fertility (reaches fertility at age 20)
    self.fertility = False

    # output thresholds for decisions
    self.move_threshold = 0
    self.eat_threshold = 0

    # decisions for output
        # eating a prey gives +250 energy
    self.move = False
    self.eat = False

  def update(self):
    # metabolism depends on which state the predator is in (hunting or idle)
    if (self.hunting is True):
      if (self.energy < 50):
        self.energy = 0
      else:
        self.energy -= 50
    else:
      if (self.energy < 25):
        self.energy = 0
      else:
        self.energy -= 25

    # Aging
    self.age += 1

    # Input vector
        # input values are determined by what the animat 
        # is seeing and / or touching
    input_vector = (
                    (2000 * int(self.hunting)),
                    (2000 * int(isinstance(self.contact, Predator))),
                    (2000 * int(isinstance(self.contact, Prey.Prey))),
                    (2000 * int(isinstance(self.contact, Environment.Environment))),
                    (2000 * self.energy)
                    )

    # Activate the nn
    output_vector = self.nn.activate(input_vector)
    
    if (output_vector[0] > self.move_threshold):
        self.move = True
    if (output_vector[1] > self.eat_threshold):
        self.eat = True
    if (self.eat is True):
        # gains energy if eats the prey
        if ((isinstance(self.contact, Prey.Prey))):
            if (self.energy >= 250):
                self.energy = 500
            else:
                self.energy += 250
        # big penalty if try to eat another predator
        elif ((isinstance(self.contact, Predator))):
            if (self.energy <= 50):
                self.energy = 0
            else:
                self.energy -= 50
        # small penalty if try to eat nothing
        else:
            if (self.energy <= 25):
                self.energy = 0
            else:
                self.energy -= 25



