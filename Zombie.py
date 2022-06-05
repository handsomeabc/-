import random

import pygame

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super(Zombie, self).__init__()
        self.image = pygame.image.load('material/images/Zombie_0.png').convert_alpha()
        self.images = [pygame.image.load('material/images/Zombie_{}.png'.format(i)).convert_alpha() for i in range(0, 22)]
        self.dieimages = [pygame.image.load('material/images/ZombieDie_{}.png'.format(i)).convert_alpha() for i in range(0, 10)]
        self.attack_images = [pygame.image.load('material/images/ZombieAttack_{}.png'.format(i)).convert_alpha() for i in range(0, 21)]

        self.rect = self.images[0].get_rect()
        self.rect.top = 25 + random.randrange(0,4)*125   #随机生成一个25，25+125，25+125*2，25+125*3其中的一个数
        self.energy = 6

        self.rect.left = 1000
        self.speed =  1
        self.dietimes = 0
        self.isMeetjianguo = False
        self.isAlive = True


    def update(self, *args):
        if self.energy > 0:
            if self.isMeetjianguo:
                self.image = self.attack_images[args[0] % len(self.attack_images)]
            else:
                self.image = self.images[args[0] % len(self.images)]
            if self.rect.left > 250 and not self.isMeetjianguo:
                self.rect.left -= self.speed
            if self.rect.left <= 250:
                running = False
                print("游戏失败！")
                exit(-1)

        else:
            if self.dietimes < 20:
                self.image = self.dieimages[self.dietimes // 2]
                self.dietimes += 1
            else:
                if self.dietimes > 30:
                    self.isAlive = False
                    self.kill()

                else:
                    self.dietimes += 1

