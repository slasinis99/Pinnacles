import main as pin
import pygame, sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FONT_SMALL = pygame.font.SysFont('Helvetica', 18)
FONT_MEDIUM = pygame.font.SysFont('Helvetica', 24)
FONT_LARGE = pygame.font.SysFont('Helvetica', 32)
FONT_TITLE = pygame.font.SysFont('Ariel', 72)

NODE_LIMIT = 10
NODE_MINIMUM = 1


class GameManager():
    def __init__(self):
        #Inherent Variables
        self.state = 'MAIN'
        self.currentGraph = None
        self.pinnacleSet = []
        self.notPinnacleSet = []
        #Main Menu Buttons
        self.createGraphButton = StateButton(int(SCREEN_WIDTH/4), int(SCREEN_HEIGHT/4), 'Create Graph', 'CREATE_GRAPH', self)
        self.createPinnacleSetButton = StateButton(int(SCREEN_WIDTH*3/4), int(SCREEN_HEIGHT/4), 'Create Pinnacle Set', 'CREATE_PINNACLE_SET', self)
        self.createEnumerateGraphButton = StateButton(int(SCREEN_WIDTH/4), int(SCREEN_HEIGHT*3/4), 'Enumerate Graph', 'ENUMERATE_GRAPH', self)
        self.createBruteForceButton = StateButton(int(SCREEN_WIDTH*3/4), int(SCREEN_HEIGHT*3/4), 'Brute Force Graph', 'BRUTE_FORCE_GRAPH', self)
        #Create Graph Variables
        self.graphTypes = ['Complete', 'Star', 'C. Bipartite', 'Cycle', 'Wheel']
        self.graphTypeKeys = ['complete', 'star', 'bipartite', 'cycle', 'wheel']
        self.graphTypeSelection = 0
        self.graphToggleButtons = []
        lx = int(SCREEN_WIDTH/7)
        for i, s in enumerate(self.graphTypes):
            self.graphToggleButtons.append(ToggleButton(lx + int(i*SCREEN_WIDTH*11/60), SCREEN_HEIGHT*3/16, s))
        self.nodeCount = NODE_MINIMUM+1
        self.altNodeCount = 1
        self.nodeInc = Incrementer(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), 'Node Count')
        self.altNodeInc = None
        self.clicked = False
        self.enumerate = 0
        self.brute = 0
    
    def run(self):
        #Main Menu, Draw the Options: Create Graph, Create Pinnacle Set, Enumerate Graph, Brute Force Graph
        if self.state == 'MAIN':
            #Draw Main Menu at the Top
            r = FONT_TITLE.render('Main Menu', True, (0, 0, 0))
            SCREEN.blit(r, (int(SCREEN_WIDTH/2 - r.get_width()/2), 16))
            #Draw the Four Buttons
            self.createGraphButton.draw(True)
            self.createPinnacleSetButton.draw(not self.currentGraph == None)
            self.createEnumerateGraphButton.draw(not self.currentGraph == None and not self.pinnacleSet == [])
            self.createBruteForceButton.draw(not self.currentGraph == None)
            if not self.currentGraph == None:
                s = f'{self.graphTypes[self.graphTypeSelection]} with {self.nodeCount} nodes'
                if self.graphTypeSelection == 1:
                    s += f' and {self.altNodeCount} stars'
                elif self.graphTypeSelection == 2:
                    s += f' and {self.altNodeCount} left side nodes'
                s += f', S = {sorted(self.pinnacleSet, reverse=True)}'
                s = FONT_LARGE.render(s, True, (0,0,0))
                SCREEN.blit(s, (int(SCREEN_WIDTH/2 - s.get_width()/2), int(SCREEN_HEIGHT/2 - s.get_height()/2)))
        elif self.state == 'CREATE_GRAPH':
            #Draw the Title at the Top
            r = FONT_TITLE.render('Create a Graph', True, (0, 0, 0))
            SCREEN.blit(r, (int(SCREEN_WIDTH/2 - r.get_width()/2), 16))
            #Draw the Toggle Buttons Along with Type Assignment
            for i, b in enumerate(self.graphToggleButtons):
                if b.draw(i == self.graphTypeSelection) and not i == self.graphTypeSelection:
                    self.graphTypeSelection = i
                    self.nodeCount = NODE_MINIMUM+1
                    self.altNodeCount = 1
                    if i == 1 or i == 2:
                        self.nodeInc = Incrementer(int(SCREEN_WIDTH/4), int(SCREEN_HEIGHT/2), 'Node Count')
                        if i == 1:
                            self.altNodeInc = Incrementer(int(SCREEN_WIDTH*3/4), int(SCREEN_HEIGHT/2), 'Star Count')
                        else:
                            self.altNodeInc = Incrementer(int(SCREEN_WIDTH*3/4), int(SCREEN_HEIGHT/2), 'Left Vertex Count')
                    else:
                        self.nodeInc = Incrementer(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), 'Node Count')
            #Now Draw the Node Count and Alt Node Count depending of graph selection
            if self.graphTypeSelection == 1 or self.graphTypeSelection == 2:
                self.nodeCount = self.nodeInc.draw(self.nodeCount, NODE_MINIMUM+self.altNodeCount, NODE_LIMIT)
                self.altNodeCount = self.altNodeInc.draw(self.altNodeCount, NODE_MINIMUM, self.nodeCount-1)
            else:
                self.nodeCount = self.nodeInc.draw(self.nodeCount, int(NODE_MINIMUM), int(NODE_LIMIT))
            #Now Draw the Back and Continue Buttons
            if basicButton(int(SCREEN_WIDTH/4), int(SCREEN_HEIGHT*7/8), 'Go Back'):
                self.state = 'MAIN'
            if basicButton(int(SCREEN_WIDTH*3/4), int(SCREEN_HEIGHT*7/8), 'Create Graph'):
                self.currentGraph = pin.create_graph(self.nodeCount, f'{self.graphTypeKeys[self.graphTypeSelection]}-{self.altNodeCount}')
                self.pinnacleSet = [self.nodeCount]
                self.notPinnacleSet = [i for i in range(1,self.nodeCount)]
                self.state = 'MAIN'
        elif self.state == 'CREATE_PINNACLE_SET':
            removePin = False
            addPin = False
            removeVal = -1
            #Draw the Title at the Top
            r = FONT_TITLE.render('Create a Pinnacle Set', True, (0,0,0))
            SCREEN.blit(r, (int(SCREEN_WIDTH/2 - r.get_width()/2), 16))
            #Draw the Buttons in Pinnacle Set
            r = FONT_LARGE.render('Pinnacle Set', True, (0, 0, 0))
            SCREEN.blit(r, (int(SCREEN_WIDTH/2 - r.get_width()/2), int(SCREEN_HEIGHT/4)))
            for i, v in enumerate(self.pinnacleSet):
                if pinButton(int(SCREEN_WIDTH/4 + i*SCREEN_WIDTH/16), int(SCREEN_HEIGHT/3), str(v)) and not self.clicked and not i == 0:
                    removePin = True
                    removeVal = v
                    self.clicked = True
            #Now Draw the not pinnacles
            r = FONT_LARGE.render('Other Labels', True, (0, 0, 0))
            SCREEN.blit(r, (int(SCREEN_WIDTH/2 - r.get_width()/2), int(SCREEN_HEIGHT*2/3)))
            for i, v in enumerate(self.notPinnacleSet):
                if pinButton(int(SCREEN_WIDTH/4 + i*SCREEN_WIDTH/16), int(SCREEN_HEIGHT*3/4), str(v)) and not self.clicked:
                    addPin = True
                    removeVal = v
                    self.clicked = True
            if removePin:
                self.pinnacleSet.remove(removeVal)
                self.notPinnacleSet.append(removeVal)
                self.notPinnacleSet.sort()
            if addPin:
                self.notPinnacleSet.remove(removeVal)
                self.pinnacleSet.append(removeVal)
                self.pinnacleSet.sort(reverse=True)
            #Handle the Accept Button
            if basicButton(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT*7/8), 'Accept'):
                self.state = 'MAIN'
        elif self.state == 'ENUMERATE_GRAPH':
            #Draw the Title at the Top
            r = FONT_TITLE.render(f'Enumeration', True, (0,0,0))
            SCREEN.blit(r, (int(SCREEN_WIDTH/2 - r.get_width()/2), 16))
            s = f'{self.graphTypes[self.graphTypeSelection]} with {self.nodeCount} nodes'
            if self.graphTypeSelection == 1:
                s += f' and {self.altNodeCount} stars'
            elif self.graphTypeSelection == 2:
                s += f' and {self.altNodeCount} left side nodes'
            s += f', S = {sorted(self.pinnacleSet, reverse=True)}'
            s = FONT_LARGE.render(s, True, (0,0,0))
            SCREEN.blit(s, (int(SCREEN_WIDTH/2 - s.get_width()/2), int(SCREEN_HEIGHT/4 - s.get_height()/2)))
            s = f'Total = {self.enumerate}'
            s = FONT_LARGE.render(s, True, (0,0,0))
            SCREEN.blit(s, (int(SCREEN_WIDTH/2 - s.get_width()/2), int(SCREEN_HEIGHT/2 - s.get_height()/2)))
            #Handle the Accept Button
            if basicButton(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT*7/8), 'Main Menu'):
                self.state = 'MAIN'
        elif self.state == 'BRUTE_FORCE_GRAPH':
            #Draw the Title at the Top
            r = FONT_TITLE.render(f'Brute Force Data', True, (0,0,0))
            SCREEN.blit(r, (int(SCREEN_WIDTH/2 - r.get_width()/2), 16))
            wy = SCREEN_HEIGHT/6
            for key in self.brute.keys():
                s = FONT_SMALL.render(key+': ', True, (0, 0, 0))
                SCREEN.blit(s, (int(SCREEN_WIDTH/2 - s.get_width()), int(wy)))
                v = FONT_SMALL.render(str(self.brute[key]), True, (0,0,0))
                SCREEN.blit(v, (int(SCREEN_WIDTH/2), int(wy)))
                wy += v.get_height() + 8
            #Handle the Accept Button
            if basicButton(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT*7/8), 'Main Menu'):
                self.state = 'MAIN'
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        




class StateButton():
    def __init__(self, cx: int, cy: int, text: str, state: str, master: GameManager):
        self.cx = cx
        self.cy = cy
        self.lx = int(self.cx - SCREEN_WIDTH/6)
        self.ty = int(self.cy - SCREEN_HEIGHT/16)
        self.w = int(SCREEN_WIDTH/3)
        self.h = int(SCREEN_HEIGHT/8)
        self.font = FONT_LARGE.render(text, True, (0, 0, 0))
        self.x = int(cx - self.font.get_width()/2)
        self.y = int(cy - self.font.get_height()/2)
        self.state = state
        self.master = master
        self.clicked = False

    def draw(self, active: bool):
        bColor = (255, 255, 255)
        if mouse_within(self.lx, self.ty, self.lx + self.w, self.ty + self.h):
            if active:
                bColor = (128, 128, 128)
            if pygame.mouse.get_pressed()[0] and not self.clicked and active:
                self.master.state = self.state
                if self.state == 'ENUMERATE_GRAPH':
                    self.master.enumerate = pin.distinct_graph_labelings(self.master.currentGraph, self.master.pinnacleSet)[0]
                if self.state == 'BRUTE_FORCE_GRAPH':
                    self.master.brute = dict(pin.get_all_pinnacle_data(self.master.currentGraph))
                self.clicked = True
        
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        
        if not active: bColor = (192, 192, 192)

        pygame.draw.rect(SCREEN, bColor, (self.lx, self.ty, self.w, self.h))
        pygame.draw.rect(SCREEN, (0, 0, 0), (self.lx, self.ty, self.w, self.h), 2)
        SCREEN.blit(self.font, (self.x, self.y))

class ToggleButton():
    def __init__(self, cx: int, cy: int, text: str):
        self.cx = cx
        self.cy = cy
        self.lx = int(cx - SCREEN_WIDTH/14)
        self.ty = int(cy - SCREEN_HEIGHT/32)
        self.w = int(SCREEN_WIDTH/7)
        self.h = int(SCREEN_HEIGHT/16)
        self.text = text
        self.font = FONT_MEDIUM.render(text, True, (0, 0, 0))
        self.x = int(cx - self.font.get_width()/2)
        self.y = int(cy - self.font.get_height()/2)
        self.clicked = False
    
    def draw(self, selected: bool) -> bool:
        bColor = (255, 255, 255)
        if mouse_within(self.lx, self.ty, self.lx + self.w, self.ty + self.h):
            bColor = (128, 128, 128)
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                selected = True
                self.clicked = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        if selected: bColor = (128, 128, 128)

        pygame.draw.rect(SCREEN, bColor, (self.lx, self.ty, self.w, self.h))
        pygame.draw.rect(SCREEN, (0, 0, 0), (self.lx, self.ty, self.w, self.h), 2)
        SCREEN.blit(self.font, (self.x, self.y))

        return selected

class Incrementer():
    def __init__(self, cx: int, cy: int, text: str) -> int:
        self.cx = cx
        self.cy = cy
        self.text = text
        self.font = FONT_MEDIUM.render(text+': ', True, (0, 0, 0))
        self.clicked = False

    def draw(self, value: int, valueMin: int, valueMax: int):
        #Draw the Name of the Incrementer
        SCREEN.blit(self.font, (self.cx - self.font.get_width(), self.cy - self.font.get_height()))
        #Handle the Minus Button
        minusColor = (255, 255, 255)
        minus = FONT_MEDIUM.render(' - ', True, (0, 0, 0))
        minusX = self.cx
        minusY = self.cy - self.font.get_height()
        minusW = 2*minus.get_width()
        minusH = self.font.get_height()
        if mouse_within(minusX, minusY, minusX + minusW, minusY + minusH):
            minusColor = (128,128,128)
            if pygame.mouse.get_pressed()[0] and not self.clicked and value > valueMin:
                self.clicked = True
                value -= 1
        #Now we handle drawing value
        vX = minusX+minusW
        vY = minusY
        vW = 2*minusW
        vH = minusH
        v = FONT_MEDIUM.render(f' {value} ', True, (0, 0, 0))
        #Now we handle the Plus Button
        plusColor = (255, 255, 255)
        plus = FONT_MEDIUM.render(' + ', True, (0, 0, 0))
        plusX = vX + vW
        plusY = vY
        plusW = 2*plus.get_width()
        plusH = self.font.get_height()
        if mouse_within(plusX, plusY, plusX + plusW, plusY + plusH):
            plusColor = (128,128,128)
            if pygame.mouse.get_pressed()[0] and not self.clicked and value < valueMax:
                self.clicked = True
                value += 1
        #Now we draw it
        #Minus
        pygame.draw.rect(SCREEN, minusColor, (minusX, minusY, minusW, minusH))
        pygame.draw.rect(SCREEN, (0, 0, 0), (minusX, minusY, minusW, minusH), 1)
        SCREEN.blit(minus, (int(minusX + 0.5*minusW - minus.get_width()/2), int(minusY + 0.5*minusH - minus.get_height()/2)))
        #Value
        pygame.draw.rect(SCREEN, (0, 0, 0), (vX, vY, vW, vH), 1)
        SCREEN.blit(v, (int(vX + 0.5*vW - v.get_width()/2), int(vY + 0.5*vH - v.get_height()/2)))
        #Plus
        pygame.draw.rect(SCREEN, plusColor, (plusX, plusY, plusW, plusH))
        pygame.draw.rect(SCREEN, (0, 0, 0), (plusX, plusY, plusW, plusH), 1)
        SCREEN.blit(plus, (int(plusX + 0.5*plusW - plus.get_width()/2), int(plusY + 0.5*plusH - plus.get_height()/2)))

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return value

def basicButton(cx: int, cy: int, text: str) -> bool:
    ret = False
    t = FONT_LARGE.render(text, True, (0, 0, 0))
    bColor = (255, 255, 255)
    if mouse_within(int(cx - - SCREEN_WIDTH/10), int(cy - t.get_height()/2), int(cx + - SCREEN_WIDTH/10), int(cy + t.get_height()/2)):
        bColor = (128,128,128)
        if pygame.mouse.get_pressed()[0]:
            ret = True
    pygame.draw.rect(SCREEN, bColor, (int(cx - SCREEN_WIDTH/10), int(cy - SCREEN_HEIGHT/32), int(SCREEN_WIDTH/5), int(SCREEN_HEIGHT/16)))
    pygame.draw.rect(SCREEN, (0, 0, 0), (int(cx - SCREEN_WIDTH/10), int(cy - SCREEN_HEIGHT/32), int(SCREEN_WIDTH/5), int(SCREEN_HEIGHT/16)), 1)
    SCREEN.blit(t, (int(cx - t.get_width()/2), int(cy - t.get_height()/2)))
    return ret

def pinButton(cx: int, cy: int, text: str) -> bool:
    ret = False
    t = FONT_SMALL.render(text, True, (0, 0, 0))
    bColor = (255, 255, 255)
    if mouse_within(int(cx - t.get_width()), int(cy - t.get_height()), int(cx + t.get_width()), int(cy + t.get_height())):
        bColor = (128,128,128)
        if pygame.mouse.get_pressed()[0]:
            ret = True
    pygame.draw.rect(SCREEN, bColor, (int(cx - t.get_width()), int(cy - t.get_height()), int(2*t.get_width()), int(2*t.get_height())))
    pygame.draw.rect(SCREEN, (0, 0, 0), (int(cx - t.get_width()), int(cy - t.get_height()), int(2*t.get_width()), int(2*t.get_height())), 1)
    SCREEN.blit(t, (int(cx - t.get_width()/2), int(cy - t.get_height()/2)))
    return ret

def mouse_within(x1: int, y1: int, x2: int, y2: int) -> bool:
    mx, my = pygame.mouse.get_pos()
    x = sorted([x1, mx, x2])
    y = sorted([y1, my, y2])
    return x[1] == mx and y[1] == my
        

def main():
    pygame.display.set_caption('Pinnacles on Graphs')

    game = GameManager()

    run = True

    while run:
        SCREEN.fill((255, 255, 255))
        
        game.run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()



if __name__ == '__main__':
    main()