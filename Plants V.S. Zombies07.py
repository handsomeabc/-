import time

import pygame
import os

from Bullet import Bullet
from Wandou import Wandou   #导入Wandou.py文件中的Wandou类
from SunFlower import SunFlower
from Jianguo import Jianguo
from Sun import Sun
from Zombie import Zombie
from FlagZombie import FlagZombie

pygame.init()     #初始化pygame
backgd_size = (1200, 600)   #定义背景的宽度和高度

screen = pygame.display.set_mode(backgd_size)  #导入背景的宽度和高度
pygame.display.set_caption("Plants V.S. Zombies")  #设置窗口标题

#初始化音乐模块
pygame.mixer.init()
#加载音乐
pygame.mixer.music.load("material/music/02 - Crazy Dave (Intro Theme).mp3")


#导入背景图片
bg_img_path = 'material/images/background1.jpg'  #背景图片相对路径
bg_img_obj = pygame.image.load(bg_img_path).convert_alpha()  #定义背景图片对象

sunflowerImg = pygame.image.load('material/images/Sunflower_00.png').convert_alpha()
jianguoImg = pygame.image.load('material/images/WallNut_00.png').convert_alpha()
wandouImg = pygame.image.load('material/images/Peashooter_00.png').convert_alpha()

sunbackImg = pygame.image.load('material/images/SeedBank.png').convert_alpha()  #创建放植物的窗口对象
flower_seed = pygame.image.load('material/images/Sunflower.gif')      #创建向日葵卡片对象
jianguo_seed = pygame.image.load('material/images/WallNut.gif')        #创建坚果卡片对象
wandou_seed = pygame.image.load('material/images/Peashooter.gif')     #创建豌豆射手卡片对象



#导入向日葵积分框
#sunbank_img_path = 'material/images/SunBack.png'  #积分框相对路径
#sunbank_img_obj = pygame.image.load(sunbank_img_path).convert_alpha()  #定义背景图片对象

text = '900'    #设置的初始分数，字符串形式
sun_font = pygame.font.SysFont('arial',20) #定义了一个字体对象，包括分数的字体和大小
sun_num_surface = sun_font.render(text,True,(0,0,0)) #导入字体（字符串形式）和颜色，将其变为图片，再到屏幕上

#wandou = Wandou()  #创建一个豌豆类对象
#sunflower = SunFlower()
#jianguo = Jianguo()
#zombie = Zombie()


#spriteGroup = pygame.sprite.Group()   #定义精灵组，相当于一个集合，相当于一个列表
#spriteGroup.add(wandou)      #调用.add方法把豌豆类对象放到精灵组里面
#spriteGroup.add(sunflower)
#spriteGroup.add(jianguo)
#spriteGroup.add(zombie)
bulletGroup = pygame.sprite.Group()   #定义子弹精灵组
zombieGroup = pygame.sprite.Group()   #定义僵尸精灵组
jianguoGroup = pygame.sprite.Group()  #定义坚果精灵组
wandouGroup = pygame.sprite.Group()  #定义豌豆精灵组
sunflowerGroup = pygame.sprite.Group()   #定义向日葵精灵组

sunList = pygame.sprite.Group()   #定义太阳精灵组

#sunList = []

clock = pygame.time.Clock()   #初始化的pygame的时钟对象

GEN_SUN_EVENT = pygame.USEREVENT + 1  #自定义一个GEN_SUN_EVENT事件，其值为系统事件USEREVENT（24）加1
pygame.time.set_timer(GEN_SUN_EVENT, 1000)  #使用该方法每一秒钟产生一个GEN_SUN_EVENT事件

GEN_BULLET_EVENT = pygame.USEREVENT + 2  #自定义一个GEN_BULLET_EVENT事件，其值为系统事件USEREVENT（24）加2
pygame.time.set_timer(GEN_BULLET_EVENT, 1000)  #使用该方法每一秒钟产生一个GEN_BULLET_EVENT事件

GEN_ZOMBIE_EVENT = pygame.USEREVENT + 3  #自定义一个GEN_ZOMBIE_EVENT事件，其值为系统事件USEREVENT（24）加2
pygame.time.set_timer(GEN_ZOMBIE_EVENT, 5000)  #使用该方法每五秒钟产生一个GEN_ZOMBIE_EVENT事件

GEN_FLAGZOMBIE_EVENT = pygame.USEREVENT + 4  #自定义一个GEN_FLAGZOMBIE_EVENT事件，其值为系统事件USEREVENT（24）加4
pygame.time.set_timer(GEN_FLAGZOMBIE_EVENT, 8000)  #使用该方法每八秒钟产生一个GEN_FLAGZOMBIE_EVENT事件

choose = 0
#定义主方法
def main():
    global text            #将text定义为全局变量
    global sun_num_surface  #将sun_num_surface定义为全局变量
    global choose         #将choose定义为全局变量
    global count
    running = True

    index = 0
    while running:
        if int(text) >= 1200:
            print("游戏胜利！")
            exit(1)

        if index >= 120:
           index = 0

        clock.tick(20)   #设置帧率为20，也就是每秒钟运行20次循环

        #播放音乐
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

        #每两秒钟生成一个太阳花
        # if index % 40 == 0:
        #    sun = Sun(sunflower.rect)   #传入sunflower.rect参数，创建太阳对象
        #   sunList.add(sun)        #将sun对象加入到精灵组里面，参与update(刷新)与draw(显示)

        #每2秒产生一个子弹
        #if index % 40 == 0:
        #    for sprite in spriteGroup:
        #        if isinstance(sprite, Wandou):
        #            bullet = Bullet(sprite.rect, backgd_size)
        #            spriteGroup.add(bullet)

        #进行冲突检测
        #在子弹组里面循环，在僵尸组里面循环，利用碰撞检测方法来判断是否发生碰撞
        #如果发生碰撞，则僵尸生命值减1，从子弹组里面移除发生碰撞过的子弹
        for bullet in bulletGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_mask(bullet,zombie):
                    zombie.energy -= 1
                    bulletGroup.remove(bullet)

        for jianguo in jianguoGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_mask(jianguo, zombie):
                    zombie.isMeetjianguo = True
                    jianguo.zombies.add(zombie)

        for wandou in wandouGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_mask(wandou, zombie):
                    zombie.isMeetjianguo = True
                    wandou.zombies.add(zombie)

        for sunflower in sunflowerGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_mask(sunflower, zombie):
                    zombie.isMeetjianguo = True
                    sunflower.zombies.add(zombie)





        screen.blit(bg_img_obj,(0, 0))  #导入背景图片到窗口，以及起始位置（0，0）
        screen.blit(sunbackImg,(250, 0))  #导入积分框图及位置
        screen.blit(sun_num_surface,(270, 60))  #导入分数及位置

        screen.blit(flower_seed,(330, 10))     #导入向日葵卡片到窗口位置
        screen.blit(jianguo_seed, (380, 10))   #导入坚果卡片到窗口位置
        screen.blit(wandou_seed, (430, 10))    #导入豌豆射手卡片到窗口位置

        #spriteGroup.update(index)   #调用精灵组每个对象的update方法进行更新，index是要传进去的参数
        #spriteGroup.draw(screen)    #把更新后的每个对象的所有元素都draw到屏幕上

        bulletGroup.update(index)  # 调用精灵组每个对象的update方法进行更新，index是要传进去的参数
        bulletGroup.draw(screen)  # 把更新后的每个对象的所有元素都draw到屏幕上

        zombieGroup.update(index)  # 调用精灵组每个对象的update方法进行更新，index是要传进去的参数
        zombieGroup.draw(screen)  # 把更新后的每个对象的所有元素都draw到屏幕上

        sunList.update(index)   #调用精灵组每个对象的update方法进行更新，index是要传进去的参数
        sunList.draw(screen)    #把更新后的每个对象的所有元素都draw到屏幕上

        jianguoGroup.update(index)  # 调用精灵组每个对象的update方法进行更新，index是要传进去的参数
        jianguoGroup.draw(screen)  # 把更新后的每个对象的所有元素都draw到屏幕上

        wandouGroup.update(index)  # 调用精灵组每个对象的update方法进行更新，index是要传进去的参数
        wandouGroup.draw(screen)  # 把更新后的每个对象的所有元素都draw到屏幕上

        sunflowerGroup.update(index)  # 调用精灵组每个对象的update方法进行更新，index是要传进去的参数
        sunflowerGroup.draw(screen)  # 把更新后的每个对象的所有元素都draw到屏幕上


        #screen.blit(wandou.images[index%13],wandou.rect)
        #screen.blit(sunflower.images[index%13],sunflower.rect)
        #screen.blit(jianguo.images[index%13],jianguo.rect)

        #for sun in sunList:
         #   screen.blit(sun.images[index % 17], sun.rect)

        (x, y) = pygame.mouse.get_pos()

        if choose == 1:
            screen.blit(sunflowerImg, (x, y))
        elif choose == 2:
            screen.blit(jianguoImg, (x, y))
        elif choose == 3:
            screen.blit(wandouImg, (x, y))

        #if choose == 1:
        #    screen.blit(sunflowerImg, (x - sunflowerImg.get_rect().width // 2, y - sunflowerImg.get_rect().height // 2))
        #if choose == 2:
        #    screen.blit(jianguoImg, (x - sunflowerImg.get_rect().width // 2, y - sunflowerImg.get_rect().height // 2))
        #if choose == 3:
        #    screen.blit(wandouImg, (x - sunflowerImg.get_rect().width // 2, y - sunflowerImg.get_rect().height // 2))


        index += 1


        for event in pygame.event.get():  # 调用pygame里面的一个事件，从消息队列取得消息，与鼠标，键盘交互
            # 如果这个GEN_ZOMBIE_EVENT事件发生（即在图片的右端四行中随机产生僵尸），每隔三秒产生一个
            if event.type == GEN_ZOMBIE_EVENT:
                zombie = Zombie()
                zombieGroup.add(zombie)

            #如果这个GEN_FLAGZOMBIE_EVENT事件发生（即在图片的右端四行中随机产生旗帜僵尸），每隔三秒产生一个
            if event.type == GEN_FLAGZOMBIE_EVENT:
                flagzombie = FlagZombie()
                zombieGroup.add(flagzombie)

            #如果这个GEN_SUN_EVENT事件（即在图片上某个位置种了向日葵）发生，就在向日葵上产生太阳
            if event.type == GEN_SUN_EVENT:
                for sprite in sunflowerGroup:
                    #if isinstance(sprite,SunFlower):
                    now = time.time()
                    if now - sprite.lasttime >= 5:
                        sun = Sun(sprite.rect)  # 传入sunflower.rect参数，创建太阳对象
                        sunList.add(sun)  # 将sun对象加入到精灵组里面，参与update(刷新)与draw(显示)
                        sprite.lasttime = now

            #如果这个GEN_BULLET_EVENT事件发生（即在图片上的某个位置种下了豌豆射手），就会发射子弹
            if event.type == GEN_BULLET_EVENT:
                 for sprite in wandouGroup:#遍历精灵组
                   #  if isinstance(sprite, Wandou):  #如果这个精灵是豌豆的话
                     bullet = Bullet(sprite.rect, backgd_size)  #就产生一个子弹类对象
                     bulletGroup.add(bullet)   #将这个子弹类对象加入到精灵组里面

            if event.type == pygame.QUIT:  # 判断是否点击了鼠标右上角的关闭按钮
                running = False  # 点了关闭按钮就将running设为False，退出循环
            if event.type == pygame.MOUSEBUTTONDOWN:   #不管是鼠标的左键，右键还是滚轮按下，都会触发这个事件
                pressed_key = pygame.mouse.get_pressed()  #通过这个函数的调用得到按下的键
                print(pressed_key)
                if pressed_key[0] == 1:
                    pos = pygame.mouse.get_pos()  #该方法可以得到鼠标在屏幕中按下的位置
                    print(pos)
                    x,y = pos
                    if 330 <= x <= 380 and 10 <= y <= 80 and int(text) >= 50:
                        print("点中了向日葵卡片")
                        choose = 1
                    elif 380 < x <= 430 and 10 <= y <= 80 and int(text) >= 50:
                        print("点中了坚果卡片")
                        choose = 2
                    elif 430 < x <= 480 and 10 <= y <= 80 and int(text) >= 100:
                        print("点中了豌豆射手卡片")
                        choose = 3
                    elif 250 < x < 1200 and 80 < y < 600:
                        #种植植物
                        if choose == 1:
                            current_time = time.time()
                            sunflower = SunFlower(current_time)
                            sunflower.rect.top = y
                            sunflower.rect.left = x
                            sunflowerGroup.add(sunflower)
                            choose = 0

                            #扣除种向日葵的分数
                            text = int(text)
                            text -= 50
                            myfont = pygame.font.SysFont('arial', 20)
                            sun_num_surface = myfont.render(str(text), True, (0, 0, 0))
                        elif choose == 2:
                            jianguo = Jianguo()
                            jianguo.rect.top = y
                            jianguo.rect.left = x
                            jianguoGroup.add(jianguo)
                            choose = 0

                            # 扣除坚果的分数
                            text = int(text)
                            text -= 50
                            myfont = pygame.font.SysFont('arial', 20)
                            sun_num_surface = myfont.render(str(text), True, (0, 0, 0))
                        elif choose == 3:
                            wandou = Wandou()
                            wandou.rect.top = y
                            wandou.rect.left = x
                            wandouGroup.add(wandou)
                            choose = 0

                            # 扣除豌豆射手的分数
                            text = int(text)
                            text -= 100
                            myfont = pygame.font.SysFont('arial', 20)         # 定义了一个字体对象，包括分数的字体和大小
                            sun_num_surface = myfont.render(str(text), True, (0, 0, 0))    # 导入字体（字符串形式）和颜色，将其变为图片，再到屏幕上




                        print('nnnnnnnn')
                        print(x, y)
                    else:
                        pass
                    for sun in sunList:
                        if sun.rect.collidepoint(pos):
                            sunList.remove(sun)
                            text=str(int(text)+50)
                            sun_font = pygame.font.SysFont('arial', 20)  # 定义了一个字体对象，包括分数的字体和大小
                            sun_num_surface = sun_font.render(text, True, (0, 0, 0))  # 导入字体（字符串形式）和颜色，将其变为图片，再到屏幕上




        pygame.display.update()  #更新界面方法

#调用主方法
if __name__ == '__main__':
    main()
