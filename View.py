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
    self.predator = pygame.image.load("predator_direction.png")
    self.prey = pygame.image.load("prey_direction.png")
    self.background = pygame.image.load("background.jpg")

    # JUST FOR FUN
    # self.predator = pygame.image.load("x_wing.gif")
    # self.prey_test = pygame.image.load("t_fighter.png")
    # self.background = pygame.image.load("black_background.jpg")

    # transform the image sizes to fit
    self.predator_image = pygame.transform.scale(self.predator, (Predator.Predator.radius, Predator.Predator.radius))
    self.prey_image = pygame.transform.scale(self.prey, (Prey.Prey.init_radius, Prey.Prey.init_radius))
    self.large_prey_image = pygame.transform.scale(self.prey, (Prey.Prey.large_radius, Prey.Prey.large_radius))
    self.background = pygame.transform.scale(self.background, (width,height))

    # initialize the Environment
    self.environment = Environment.Environment(width, height, num_predator, num_prey)
    print "environment initialized \n"

  def update(self, iterations):
    # print "still in second main loop" this works fine too
    # update the environment as many times as specified
    for x in range(iterations):
      self.environment.update_environment()

    # repaint the surface
    view.surface.blit(view.background, (0,0))
    # repaint the animats
    for predator in view.environment.predators:
      view.surface.blit( pygame.transform.rotate(view.predator_image, 359 - predator.direction) , (predator.x - predator.radius, predator.y - predator.radius))
    for prey in view.environment.preys:
      if prey.age < 15:
        view.surface.blit( pygame.transform.rotate(view.prey_image, 359 - prey.direction), (prey.x - prey.radius, prey.y - prey.radius))
      else:
        view.surface.blit( pygame.transform.rotate(view.large_prey_image, 359 - prey.direction), (prey.x - prey.radius, prey.y - prey.radius))



# main function
if __name__ == "__main__":
  view = View(800, 800, 30, 60)
  for predator in view.environment.predators:
    view.surface.blit(view.predator_image, (predator.x - predator.radius, predator.y - predator.radius))
  for prey in view.environment.preys:
    view.surface.blit(view.prey_image, (prey.x - prey.radius, prey.y - prey.radius))
  pygame.display.flip()
  # time.sleep(2)
  for i in range(700):
    view.update(1)
    pygame.display.flip()
    time.sleep(5)
  results = open('results', 'w')
  results.write("Iterations : %d \n" % view.environment.iterations_pred)
  print "Iterations : %d" % view.environment.iterations_pred
  results.write("Max gen pred : %d \n" % view.environment.max_gen_pred)
  print "Max gen pred : %d" % view.environment.max_gen_pred
  results.write("Predators left : %d \n" % view.environment.num_predator)
  print "Predators left : %d" % view.environment.num_predator
  results.write("Preys left : %d \n" % view.environment.num_prey)
  print "Preys left : %d" % view.environment.num_prey
  results.write("Number of non-coop attacks : \n")
  for x in range(len(view.environment.non_coop_atk)):
    results.write(str(view.environment.non_coop_atk[x]))
    results.write("\n")
  results.write("Number of coop attacks : \n")
  for x in range(len(view.environment.coop_atk)):
    results.write(str(view.environment.coop_atk[x]))
    results.write("\n")

  # write the surviving predator neural nets
  results.write("Predator Neural Nets : \n")
  for x in range(len(view.environment.pred_neural_nets)):
    results.write(str(view.environment.pred_neural_nets[x]))
    results.write("\n")
  results.close()

  pygame.quit()




