import random
import curses

import os

class Canvas:
    gameMap = [["-", "-", "-", "-", "-", "-", "-"], ["|", " ", " ", " ", " ", " ", "|"], ["|", " ", " ", " ", " ", " ", "|"],
               ["|", " ", " ", " ", " ", " ", "|"], ["|", " ", " ", " ", " ", " ", "|"],
               ["|", " ", " ", " ", " ", " ", "|"], ["-", "-", "-", "-", "-", "-", "-"]]

    # point, which appears on the map
    points1 = 0
    points2 = 0

    elemList = []

    exOfSnake = False
    lengthOfSnake = 2


    def __init__(self):

        random.randint(2, 5)
        self.points1 = random.randint(1, 6)
        self.points2 = random.randint(1, 6)
        self.elemList.append((random.randint(1, len(self.gameMap) - 2), random.randint(1, len(self.gameMap) - 2), True))
        self.lenOfSnake = 2


    def pointPlaceFinder(self):
        self.points1 = random.randint(1, 5)
        self.points2 = random.randint(1, 5)
        if (self.points1, self.points2, True) in self.elemList:
            self.pointPlaceFinder()


    def updateMap(self):

        self.gameMap = [["-", "-", "-", "-", "-", "-", "-"], ["|", " ", " ", " ", " ", " ", "|"], ["|", " ", " ", " ", " ", " ", "|"],
                        ["|", " ", " ", " ", " ", " ", "|"], ["|", " ", " ", " ", " ", " ", "|"],
                        ["|", " ", " ", " ", " ", " ", "|"], ["-", "-", "-", "-", "-", "-", "-"]] # map leeren


        for elements in self.elemList:
            if elements[2]:
                tmp1 = elements[0]
                tmp2 = elements[1]
                self.gameMap[tmp1].pop(tmp2)
                self.gameMap[tmp1].insert(tmp2, "#")

        # setze Koordinaten für Punkt
        if self.exOfSnake:
            self.pointPlaceFinder()
            self.exOfSnake = False

        self.gameMap[self.points1].pop(self.points2)
        if self.elemList[0][0] == self.points1 and self.elemList[0][1] == self.points2:
            self.gameMap[self.points1].insert(self.points2, "#")
        else:
            self.gameMap[self.points1].insert(self.points2, "P")


        # Wo ist das Futter (Point)? Wo befidnet sich der Schwanz?




    def draw(self):
        clear = lambda: os.system('cls')
        clear()
        self.updateMap()
        for i in self.gameMap:  # male Map
            print(i, sep = ' ', end=' ')
            print('\n')


class Controller:
    points = 0
    c = Canvas()  # Fester Wer hier für Map
    las = "s"
    def exe(self):
        pos1 = self.c.elemList[0][0]  # Position der Snake
        pos2 = self.c.elemList[0][1]
        extentionOfSnake = False

        # am Rand?
        if pos1 < 1 or pos2 < 1 or pos1 > len(self.c.gameMap) - 2 or pos2 > len(self.c.gameMap[1]) - 2:
            self.lostGame()
        self.c.gameMap[pos1][pos2] = " "
        w = input()

        h = self.c.elemList[0]
        self.c.elemList.pop(0)
        if (pos1, pos2, True) in self.c.elemList:
            self.lostGame()
        self.c.elemList.insert(0, h)

        if pos1 == self.c.points1 and pos2 == self.c.points2:
            self.c.lengthOfSnake += 1
            extentionOfSnake = True
            self.c.exOfSnake = True

        # Welche Taste gedrückt
        if w == "a" or w == "A":
            pos2 -= 1
            self.las = "a"
            self.posUpdate(0,-1,extentionOfSnake)
        elif w == "s" or w == "S":
            self.las = "s"
            pos1 += 1
            self.posUpdate(+1,0,extentionOfSnake)
        elif w == "d" or w == "D":
            self.las = "d"
            pos2 += 1
            self.posUpdate(0,+1,extentionOfSnake)
        elif w == "W" or w == "w":
            self.las = "w"
            pos1 -= 1
            self.posUpdate(-1,0,extentionOfSnake)
        else:
            if w == "a" or w == "A":
                pos2 -= 1
                self.las = "a"
                self.posUpdate(0,-1,extentionOfSnake)
            elif w == "s" or w == "S":
                self.las = "s"
                pos1 += 1
                self.posUpdate(+1,0,extentionOfSnake)
            elif w == "d" or w == "D":
                self.las = "d"
                pos2 += 1
                self.posUpdate(0,+1,extentionOfSnake)
            elif w == "W" or w == "w":
                self.las = "w"
                pos1 -= 1
            self.posUpdate(-1,0,extentionOfSnake)


        # am Rand?
        if pos2 > len(self.c.gameMap) or pos1 > len(self.c.gameMap[1]) or pos1 < 0 or pos2 < 0:
            self.lostGame()

        self.c.draw()
        self.points = self.points + 1 * self.c.lengthOfSnake * 100
        self.exe()

    def lostGame(self):
        print("Sie haben das Spiel verloren")
        print("Ihre Punktzahl:", self.points)
        print("Wollen Sie noch eine Runde Spielen?")
        x = input("j/J für Ja")
        if x == "j" or x == "J":
            self.c = Canvas()
            #self.c.elemList.clear()
            #self.c.elemList.append((random.randint(1, len(self.c.gameMap) - 1), (random.randint(1, len(self.c.gameMap[1]) - 1)), True))
           # self.c.lengthOfSnake = 2
            self.las = "s"
            self.points = 0
            self.exe()
        else:
            exit()

    def posUpdate(self, pos1, pos2,extentionOfSnake):
        elemsOfGame2 = []
        if extentionOfSnake:
            le = self.c.lengthOfSnake + 1
            self.c.lengthOfSnake +=1
        else:
            le = self.c.lengthOfSnake

        print(len(self.c.elemList))
        tmp = self.c.elemList[0]

        if pos1 == -1:
            elemsOfGame2.append((tmp[0] - 1, tmp[1], tmp[2]))
        elif pos1 == 1:
            elemsOfGame2.append((tmp[0] + 1, tmp[1], tmp[2]))
        elif pos2 == -1:
            elemsOfGame2.append((tmp[0], tmp[1] - 1, tmp[2]))
        elif pos2 == 1:
            elemsOfGame2.append((tmp[0], tmp[1] + 1, tmp[2]))

        for elements in self.c.elemList:
            if le > 0:
                elemsOfGame2.append((elements[0], elements[1], True))
                le -=1
            else:
                elemsOfGame2.append((elements[0], elements[1], False))

        self.c.elemList = elemsOfGame2
        print(self.c.elemList)

while True:
    con = Controller()
    con.exe()
