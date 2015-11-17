from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection

class Prey:
  radius = 20
  def __init__(self, direction, x, y):
    # #size of prey
    # self.radius = 20
    #Neural network
    self.nn = FeedForwardNetwork()
    #Add layers
    inLayer = LinearLayer(12)
    hiddenLayer = SigmoidLayer(13)
    outLayer = LinearLayer(6)
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

    # Sees predator
    self.see_predator = False

    # Age
    self.age = 0

    # Fertility (reaches fertility at age 100)
    self.fertility = False



  def update(self):
    # metabolism
    self.energy -= 5
    # Aging
    self.age += 1
    
    # Input vector
        # input values are determined by what the animat 
        # is seeing and / or touching
    input_vector = []

    # Activate the nn
    self.nn.activate(input_vector)

    



