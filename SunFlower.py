import pygame

class SunFlower(pygame.sprite.Sprite):
    def __init__(self, lasttime):
        super(SunFlower, self).__init__()
        self.image = pygame.image.load('material/images/SunFlower_00.png').convert_alpha()

        self.images = [pygame.image.load('material/images/SunFlower_{:02d}.png'.format(i)).convert_alpha() for i in range(0,13)]

        self.rect = self.images[0].get_rect()
        #self.rect.top = 250
        #self.rect.left = 250
        self.lasttime = lasttime
        self.energy = 3 * 15  # 定义向日葵的能量（生命值）
        self.zombies = set()  # 创建向日葵碰到的僵尸集

    def update(self, *args):

        for zombie in self.zombies:
            if zombie.isAlive == False:
                continue

            self.energy -= 1

        if self.energy <= 0:
            for zombie in self.zombies:
                zombie.isMeetjianguo = False
            self.kill()

        self.image = self.images[args[0] % len(self.images)]