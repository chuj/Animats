from pybraiself.nn.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection

class Predator:
  def __init__(self, direction, x, y):
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

  def metabolism(self):
    self.energy -= 5

  def update(self):
    