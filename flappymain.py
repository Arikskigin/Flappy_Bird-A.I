import pygame
import neat
import os
from Bird import Bird
from theBase import theBase
from greenPipe import greenPipe
pygame.font.init()

Window_Width = 570
Window_Height = 770
Gen=0

# makes img 2 times bigger and reads it
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

FONT = pygame.font.SysFont("comicsans", 45)


def draw_window(win, multiple_birds, pipes, base, score, gen):
    if gen == 0:
        gen = 1
    win.blit(BACKGROUND_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = FONT.render("Sc0re: " + str(score), 1, (0, 0, 0))
    win.blit(text, (Window_Width - 10 - text.get_width(), 10))

    text = FONT.render("Gen: " + str(gen -1), 1, (0, 0, 0))
    win.blit(text, (10, 10))

    text = FONT.render("Alive: " + str(len(multiple_birds)), 1, (0, 0, 0))
    win.blit(text, (10, 50))

    base.draw(win)
    for bird in multiple_birds:
        bird.draw(win)

    pygame.display.update()


def evalute_genomes(genomes, config):
    """
    runs the game with fixed population of flapy birds and change fitness based on where they reached in the game
    """
    global Gen

    # making a list of neural networks of the genomes,list that have genomes and the objects of the birds that use this
    # network to play
    networks = []
    genomes_list = []
    multiple_birds = []
    Gen += 1

    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        multiple_birds.append(Bird(210, 230, BIRD_IMAGES))
        # start with 0 fitness
        genome.fitness = 0
        genomes_list.append(genome)

    base = theBase(700, BASE_IMAGE)
    pipes = [greenPipe(570, PIPE_IMAGE)]
    win = pygame.display.set_mode((Window_Width, Window_Height))
    clock = pygame.time.Clock()
    score = 0
    run = True
    while run:
        clock.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_index = 0
        if len(multiple_birds) > 0:
            if len(pipes) > 1 and multiple_birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            run = False
            break

        for x, bird in enumerate(multiple_birds):
            # if bird survived we need to increase its fitness because its doing well
            genomes_list[x].fitness += 0.08
            bird.move()
            network_output = networks[x].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if network_output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        # creating pipes,when pipe reach certain point we need to create another pipe
        for pipe in pipes:
            for x, bird in enumerate(multiple_birds):
                if pipe.collide(bird):
                    genomes_list[x].fitness -= 1
                    multiple_birds.pop(x)
                    networks.pop(x)
                    genomes_list.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() <0:
                rem.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            for genome in genomes_list:
                genome.fitness += 5
            pipes.append(greenPipe(570, PIPE_IMAGE))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(multiple_birds):
            if bird.y + bird.img.get_height() >= 700 or bird.y < 0:
                multiple_birds.pop(x)
                networks.pop(x)
                genomes_list.pop(x)

        base.move()
        draw_window(win, multiple_birds, pipes, base, score ,Gen)


def run(config_path):
    """
      runs the NEAT algorithm to train a neural network.
      :param config_file: location of config file
      :return: None
      """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    statistics = neat.StatisticsReporter()
    population.add_reporter(statistics)
    # calls main function 50 times and generates the game with all genomes
    winner_bird = population.run(evalute_genomes, 50)


if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "Configuration.txt")
    run(config_path)