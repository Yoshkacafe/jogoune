import pyxel
import random
import time
import random

class Button:
    def __init__(self, x, y, img, u, v, w, h):
        self.colkey = 2
        self.x = x
        self.y = y
        self.img = img
        self.u = u
        self.v = v
        self.w = w
        self.h = h

    def over(self):
        mx = pyxel.mouse_x
        my = pyxel.mouse_y
        if mx >= self.x and mx <= self.x+self.w and my >= self.y and my <= self.y+self.h:
            return True
        return False
    
    def click(self):
        if self.over() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, repeat=1000):
            return True
        return False
    
    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v,self. w, self.h)



class App:
    def __init__(self) -> None:
        pyxel.init(256, 256, title="Jogoune")
        self.finish = False
        
        self.one = 0
        self.two = 0
        self.three = 0
        self.four = 0
        self.five = 0

        self.background = pyxel.load("theme2.pyxres")
        self.liste_chat = []

        self.buttonChat1 = Button(20, 170, 0, 0, 80, 32, 32)
        self.buttonChat2 = Button(70, 170, 0, 32, 80, 32, 32)
        self.buttonChat3 = Button(120, 170, 0, 64, 80, 32, 32)
        self.buttonChat4 = Button(170, 170, 0, 96, 80, 32, 32)
        self.buttonChat5 = Button(220, 170, 0, 128, 80, 32, 32)


        self.buttonNewCat = Button(0, 0, 1, 32, 0, 32, 32)
        self.buttonLife = Button(0, 0, 1, 64, 0, 32, 32)
        self.buttonMoney = Button(0, 0, 1, 96, 0, 32, 32)
        self.buttonDamage = Button(0, 0, 1, 0, 0, 32, 32)
        self.buttonSpeed = Button(0, 0, 1, 128, 0, 32, 32)

        self.buff = [self.buttonNewCat, self.buttonLife, self.buttonMoney, self.buttonDamage, self.buttonSpeed]

        self.chatdebloquer = [self.buttonChat1]

        self.lvl = 1

        self.money = 150

        self.type = 1
        self.tour = Tower(self.liste_chat, self.type)
        self.running = True

        self.money_add = 100
        self.life_add = 0
        self.speed_add = 0
        self.damage_add = 0

        pyxel.run(self.update, self.draw)

    def timer(self):
        time = pyxel.frame_count
        if time % 150 == 0:
            self.money += self.money_add
        if time % 75 == 0:
            self.tour.attack()

    # Méthode qui update 30 frames / seconde
    def update(self):
        pyxel.mouse(visible=True)
        if self.running:
            # Condition de clique sur les boutons
            # Augmentation de l'argent
            # self.money += 1
            # print(self.money)
            self.timer()
            if self.tour.life <= 0:
                random.shuffle(self.buff)
                self.running = False
                self.lvl += 1
                self.liste_chat = []
                self.money = 150
                self.type *= 1.5
                self.tour = Tower(self.liste_chat, self.type)
                if self.lvl == 11:
                    self.finish = True
        self.event()

    # Méthode qui se lance 30 fois par seconde
    def draw(self):
        if self.finish:
            pyxel.cls(0)
            pyxel.text(10, 10, "You win your chest ! A famous chest for you !\n :D You can replay the game to try to unlock a rarest chest !", 7)
            pyxel.blt(100, 100, 0, 48, 144, 64, 64, 2)
        elif self.running:
            pyxel.bltm(0,0,0,0,0,256,256)
            pyxel.text(30, 220, f"{self.one}", 0)
            pyxel.text(80, 220, f"{self.two}", 0)
            pyxel.text(130, 220, f"{self.three}", 0)
            pyxel.text(180, 220, f"{self.four}", 0)
            pyxel.text(230, 220, f"{self.five}", 0)
            pyxel.rect(5, 5, 60, 25, 0)
            pyxel.text(10, 10, f"Level : {self.lvl}", 7)
            pyxel.text(10, 20, f"Money : {self.money}$", 7)
            self.tour.spawn()
            self.show_cats()
        else:
            pyxel.bltm(0,0,0,256,0,256,256)
            pyxel.text(10, 10, "You win !", 7)

            pyxel.rect(45, 17, 47, 12, 0)
            pyxel.text(50, 20, "Path 1 :", 7)
            self.buff[0].x = 50
            self.buff[0].y = 80
            self.buff[0].draw()

            pyxel.rect(175, 17, 47, 12, 0)
            pyxel.text(180, 20, "Path 2 : ", 7)
            self.buff[1].x = 175
            self.buff[1].y = 80
            self.buff[1].draw()
            
    
    def show_cats(self):
        for chat in self.liste_chat:
            if chat.life > 0:
                if (chat.x < self.tour.x - (10 + chat.distance)):
                    chat.x += chat.speed
                else:
                    chat.attack(self.tour)
                chat.spawn()
            else:
                if chat.id == 1:
                    self.one -= 1
                elif chat.id == 2:
                    self.two -= 1
                elif chat.id == 3:
                    self.three -= 1
                elif chat.id == 4:
                    self.four -= 1
                else:
                    self.five -= 1
                self.liste_chat.pop(self.liste_chat.index(chat))

        for button in self.chatdebloquer:
            button.draw()

    def event(self):
        if self.buttonChat1.click() and self.buttonChat1 in self.chatdebloquer and self.money >= 100:
            chat1 = Chat_1(self.life_add, self.speed_add, self.damage_add)
            self.liste_chat.append(chat1)
            chat1.spawn()
            self.money -= 100
            self.one += 1                
        if self.buttonChat2.click() and self.buttonChat2 in self.chatdebloquer and self.money >= 225:
            chat2 = Chat_2(self.life_add, self.speed_add, self.damage_add)
            self.liste_chat.append(chat2)
            chat2.spawn()
            self.money -= 225
            self.two += 1
        if self.buttonChat3.click() and self.buttonChat3 in self.chatdebloquer and self.money >= 300:
            chat3 = Chat_3(self.life_add, self.speed_add, self.damage_add)
            self.liste_chat.append(chat3)
            chat3.spawn()
            self.money -= 300
            self.three += 1
        if self.buttonChat4.click() and self.buttonChat4 in self.chatdebloquer and self.money >= 500:
            chat4 = Chat_4(self.life_add, self.speed_add, self.damage_add)
            self.liste_chat.append(chat4)
            chat4.spawn()
            self.money -= 500
            self.four += 1
        if self.buttonChat5.click() and self.buttonChat5 in self.chatdebloquer and self.money >= 1000:
            chat5 = Chat_5(self.life_add, self.speed_add, self.damage_add)
            self.liste_chat.append(chat5)
            chat5.spawn()
            self.money -= 1000
            self.five += 1
        if not self.running and self.buttonMoney.click() and self.buttonMoney in self.buff[:2]:
            print("Plus d'argent")
            self.one = 0
            self.two = 0
            self.three = 0
            self.four = 0
            self.five = 0
            self.running = True
            self.money_add = self.money_add * 2
        if not self.running and self.buttonNewCat.click() and self.buttonNewCat in self.buff[:2]:
            print("New cat")
            self.one = 0
            self.two = 0
            self.three = 0
            self.four = 0
            self.five = 0
            # Afficher le nouveau bouton
            if len(self.chatdebloquer) == 1:
                self.chatdebloquer.append(self.buttonChat2)
                self.running = True
            elif len(self.chatdebloquer) == 2:
                self.chatdebloquer.append(self.buttonChat3)
                self.running = True
            elif len(self.chatdebloquer) == 3:
                self.chatdebloquer.append(self.buttonChat4)
                self.running = True
            elif len(self.chatdebloquer) == 4:
                self.chatdebloquer.append(self.buttonChat5)
                self.running = True
            elif len(self.chatdebloquer) == 5:
                pyxel.text(10, 10, "You have already all the cat ! Let's play again to open new gifts ! :)")
                time.sleep(2)
                self.running = True
        if not self.running and self.buttonDamage.click() and self.buttonDamage in self.buff[:2]:
            print("Plus de dégats")
            self.one = 0
            self.two = 0
            self.three = 0
            self.four = 0
            self.five = 0
            self.damage_add += 20
            self.running = True
        if not self.running and self.buttonLife.click() and self.buttonLife in self.buff[:2]:
            print("Plus de vie")
            self.one = 0
            self.two = 0
            self.three = 0
            self.four = 0
            self.five = 0
            self.running = True
            self.life_add += 500
        if not self.running and self.buttonSpeed.click() and self.buttonSpeed in self.buff[:2]:
            print("Plus de vitesse")
            self.one = 0
            self.two = 0
            self.three = 0
            self.four = 0
            self.five = 0
            self.running = True
            self.speed_add += 0.3
        

class Tower():
    def __init__(self, chats, type) -> None:
        self.chats = chats
        self.x = 200
        self.y = 68
        self.damage = 100 * type
        self.life = 200 * type
        self.zone = 64

    def spawn(self):
        pyxel.rect(self.x-3, self.y - 13, 47, 12, 0)
        pyxel.text(self.x, self.y-10, f"Life : {self.life}", 7)
        pyxel.blt(self.x, self.y, 0, 32, 112, 32, 32, 2)
        pyxel.blt(self.x, self.y, 0, 0, 112, 32, 64, 2)

    def attack(self):
        xmin = self.x
        xmax = self.x - self.zone
        liste = []
        tank = False
        for chat in self.chats:
            if chat.id == 1 :
                tank = True
        for chat in self.chats:
            if chat.x <= xmin and chat.x >= xmax:
                if tank == True:
                    if chat.id == 1 :
                        chat.life -= self.damage * 1.5
                else:
                    chat.life -= self.damage
        
    

class Chat_1():
    def __init__(self, life, speed, damage) -> None:
        self.id = 1
        self.x = 0
        self.y = 100
        self.speed = 0.8 + speed
        self.distance = 10
        self.damage = 10 + damage
        self.life = 1500 + life
        self.color = 1
        self.money = 100
    
    def spawn(self):
        pyxel.blt(self.x, self.y, 0, 0, 48, 32, 32, 2)
        pyxel.text(self.x, self.y-10, f"{self.life}", 4)

    def attack(self, tour):
        time = pyxel.frame_count
        if time % 30 == 0:
            tour.life -= self.damage

class Chat_2():
    def __init__(self, life, speed, damage) -> None:
        self.id = 2
        self.x = 0
        self.y = 100
        self.speed = 1.3 + speed
        self.distance = 10
        self.damage = 100 + damage
        self.life = 500 + life
        self.color = 2
        self.money = 225
    
    def spawn(self):
        pyxel.blt(self.x, self.y, 0, 32, 48, 32, 32, 2)
        pyxel.text(self.x, self.y-10, f"{self.life}", 4)
    
    def attack(self, tour):
        time = pyxel.frame_count
        if time % 30 == 0:
            tour.life -= self.damage

class Chat_3():
    def __init__(self, life, speed, damage) -> None:
        self.id = 3
        self.x = 0
        self.y = 100
        self.speed = 1.5 + speed
        self.distance = 2.5
        self.damage = 250 + damage
        self.life = 500 + life
        self.color = 3
        self.money = 300
    
    def spawn(self):
        pyxel.blt(self.x, self.y, 0, 64, 48, 32, 32, 2)
        pyxel.text(self.x, self.y-10, f"{self.life}", 4)
    
    def attack(self, tour):
        time = pyxel.frame_count
        if time % 30 == 0:
            tour.life -= self.damage

class Chat_4():
    def __init__(self, life, speed, damage) -> None:
        self.id = 4
        self.x = 0
        self.y = 100
        self.speed = 2 + speed
        self.distance = 35
        self.damage = 100 + damage
        self.life = 200 + life
        self.color = 4
        self.money = 500
    
    def spawn(self):
        pyxel.blt(self.x, self.y, 0, 96, 48, 32, 32, 2)
        pyxel.text(self.x, self.y-10, f"{self.life}", 4)
    
    def attack(self, tour):
        time = pyxel.frame_count
        if time % 30 == 0:
            tour.life -= self.damage

class Chat_5():
    def __init__(self, life, speed, damage) -> None:
        self.name = "Nyan Cat ^^"
        self.id = 5
        self.x = 0
        self.y = 100
        self.speed = 0.4 + speed
        self.distance = 25
        self.damage = 1000 + damage
        self.life = 3000 + life
        self.color = 5
        self.money = 1000
    
    def spawn(self):
        pyxel.blt(self.x, self.y, 0, 128, 48, 32, 32, 2)
        pyxel.text(self.x, self.y-10, f"{self.life}", 4)
    
    def attack(self, tour):
        time = pyxel.frame_count
        if time % 30 == 0:
            tour.life -= self.damage
        
App()