import Environment
import Predator
import Prey
import Obstacle
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
    self.obstacle = pygame.image.load("obstacle.jpg")

    # JUST FOR FUN
    # self.predator = pygame.image.load("x_wing.gif")
    # self.prey_test = pygame.image.load("t_fighter.png")
    # self.background = pygame.image.load("black_background.jpg")

    # transform the image sizes to fit
    self.predator_image = pygame.transform.scale(self.predator, (Predator.Predator.radius, Predator.Predator.radius))
    self.prey_image = pygame.transform.scale(self.prey, (Prey.Prey.init_radius, Prey.Prey.init_radius))
    self.large_prey_image = pygame.transform.scale(self.prey, (Prey.Prey.large_radius, Prey.Prey.large_radius))
    self.background = pygame.transform.scale(self.background, (width,height))
    self.obstacle_image_vert = pygame.transform.scale(self.obstacle, (100, 200))
    self.obstacle_image_horz = pygame.transform.rotate(self.obstacle_image_vert, -90)
    self.obstacle_image_horz = pygame.transform.scale(self.obstacle_image_horz, ( 300,100) )

    # initialize the Environment
    self.environment = Environment.Environment(width, height, num_predator, num_prey)
    print "environment initialized \n"

  def update(self, iterations):
    # update the environment as many times as specified
    for x in range(iterations):
      self.environment.update_environment()

    # repaint the surface
    view.surface.blit(view.background, (0,0))
    # repaint the obstacles
    view.surface.blit(view.obstacle_image_vert, (view.environment.obstacles[0].x_bot, view.environment.obstacles[0].y_top) ) 
    # TODO
    view.surface.blit(view.obstacle_image_horz, (view.environment.obstacles[1].x_bot, view.environment.obstacles[1].y_top) ) 
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
  view = View(800, 800, 20, 50)
  view.surface.blit(view.obstacle_image_vert, (view.environment.obstacles[0].x_bot, view.environment.obstacles[0].y_top) ) 
  # TODO
  view.surface.blit(view.obstacle_image_horz, (view.environment.obstacles[1].x_bot, view.environment.obstacles[1].y_top) ) 
  for predator in view.environment.predators:
    view.surface.blit(view.predator_image, (predator.x - predator.radius, predator.y - predator.radius))
  for prey in view.environment.preys:
    view.surface.blit(view.prey_image, (prey.x - prey.radius, prey.y - prey.radius))
  pygame.display.flip()
  # time.sleep(2)
  for i in range(700):
    view.update(1)
    pygame.display.flip()
    # time.sleep(5)
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
  # results.write("Number of failed non-coop attacks : \n")
  # for x in range(len(view.environment.non_coop_atk_failed)):
  #   results.write(str(view.environment.non_coop_atk_failed[x]))
  #   results.write("\n")
  results.write("Number of coop attacks : \n")
  for x in range(len(view.environment.coop_atk)):
    results.write(str(view.environment.coop_atk[x]))
    results.write("\n")
  # results.write("Number of failed coop attacks : \n")
  # for x in range(len(view.environment.coop_atk_failed)):
  #   results.write(str(view.environment.coop_atk_failed[x]))
  #   results.write("\n")
  results.write("Number of non-coop attacks on large : \n")
  for x in range(len(view.environment.non_coop_atk_large)):
    results.write(str(view.environment.non_coop_atk_large[x]))
    results.write("\n")
  # results.write("Number of failed non-coop attacks on large : \n")
  # for x in range(len(view.environment.non_coop_atk_large_failed)):
  #   results.write(str(view.environment.non_coop_atk_large_failed[x]))
  #   results.write("\n")
  results.write("Number of coop attacks on large : \n")
  for x in range(len(view.environment.coop_atk_large)):
    results.write(str(view.environment.coop_atk_large[x]))
    results.write("\n")
  # results.write("Number of failed coop attacks on large : \n")
  # for x in range(len(view.environment.coop_atk_large_failed)):
  #   results.write(str(view.environment.coop_atk_large_failed[x]))
  #   results.write("\n")

  # write the surviving predator neural nets
  results.write("Predator Neural Nets : \n")
  for x in range(len(view.environment.pred_neural_nets)):
    results.write(str(view.environment.pred_neural_nets[x]))
    results.write("\n")
  results.close()

  pygame.quit()




