import Environment
import Predator
import Prey

import pygame
import math
import time

class View:
  def __init__(self, width, height, num_predator, num_prey):
    # initialize the pygame view
    pygame.init()
    print "pygame init worked \n"
    # initialize surface size
    self.surface = pygame.display.set_mode((width,height))

    # load pictures for predator and Prey
    self.predator = pygame.image.load("predator.png")
    self.prey = pygame.image.load("prey.png")

    # transform the image sizes to fit
    self.predator_image = pygame.transform.scale(self.predator, (20,20))
    self.prey_image = pygame.transform.scale(self.prey, (20,20))

    # initialize the Environment
    self.environment = Environment.Environment(1000,1000, num_predator, num_prey)
    print "environment initialized \n"

  def update(self, iterations):
    # update the environment as many times as specified
    for x in range(iterations):
      self.environment.update_environment()

    # repaint the animats
    for predator in view.environment.predators:
      view.surface.blit(view.predator_image, (predator.x - predator.radius, predator.y - predator.radius))
    for prey in view.environment.preys:
      view.surface.blit(view.prey_image, (prey.x - prey.radius, prey.y - prey.radius))



# main function
if __name__ == "__main__":
  view = View(1000, 1000, 2, 20)

  for predator in view.environment.predators:
    view.surface.blit(view.predator_image, (predator.x - predator.radius, predator.y - predator.radius))
  for prey in view.environment.preys:
    view.surface.blit(view.prey_image, (prey.x - prey.radius, prey.y - prey.radius))
  pygame.display.flip()
  for i in range(10):
    view.update(10)
    pygame.display.flip()
    time.sleep(0.5)
  pygame.quit()