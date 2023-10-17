import main as pin
import pygame, sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FONTS = [None]
for i in range(1,73):
    FONTS.append(pygame.font.SysFont('Helvetica', i))

FONT_SMALL = pygame.font.SysFont('Helvetica', 18)
FONT_MEDIUM = pygame.font.SysFont('Helvetica', 24)
FONT_LARGE = pygame.font.SysFont('Helvetica', 32)
FONT_TITLE = pygame.font.SysFont('Helvetica', 72)

NODE_LIMIT = 10
NODE_MINIMUM = 1

CLICKED = False

class GameManager():
    def __init__(self):
        self.state = 'MAIN_MENU'
        self.graph = pin.create_graph(8, 'star-2')
        self.pset = [8,7]
        self.notpset = [6,5,4,3,2,1]
        self.enumerate = 0
        self.pinnacleData = {}
        #Create Graph State Variables
        self.graphType = 2
        self.nodeCount = 8
        self.altNodeCount = 2
    
    def run(self):
        self.runState(self.state)

    def runState(self, state: str):
        if state == 'MAIN_MENU':
            #Draw the Title
            title = FONTS[64].render('Main Menu', True, (0, 0, 0))
            SCREEN.blit(title, (int(SCREEN_WIDTH/2 - 0.5*title.get_width()), 16))

            #Choose a Font Size
            f = FONTS[32]

            #Draw the Buttons evenly spaced along the left hand side
            spacing = 16
            button_names = ['Create New Graph', 'Create Pinnacle Set', 'Enumerate Labelings', 'Brute Force Graph', 'Exit Program']
            total_height = 0
            for s in button_names:
                total_height += getButtonDimensionData(s, f, 1.2, 1.2, width=320, height=64)[1]
                if not s == button_names[len(button_names)-1]:
                    total_height += spacing
            wh = int(SCREEN_HEIGHT/2 - 0.5*total_height)
            for s in button_names:
                b = drawButton(s, f, [int(SCREEN_WIDTH/6), wh+32], 1.2, 1.2, width=320, height=64, borderRadius=4)
                wh += 64 + spacing
                if b[4]:
                    if s == button_names[0]:
                        self.state = 'CREATE_GRAPH'
                    elif s == button_names[1]:
                        print(button_names[1])
                    elif s == button_names[2]:
                        print(button_names[2])
                    elif s == button_names[3]:
                        print(button_names[3])
                    elif s == button_names[4]:
                        pygame.quit()
                        sys.exit()
        elif state == 'CREATE_GRAPH':
            #Draw the Title
            title = FONTS[64].render('Create a New Graph', True, (0, 0, 0))
            SCREEN.blit(title, (int(SCREEN_WIDTH/2 - 0.5*title.get_width()), 16))

            #Select a font
            f = FONTS[20]

            #Graph Types
            gt = ['Complete', 'C. Bipartite', 'Star', 'Cycle', 'Wheel', 'Line', 'Custom']
            gt_keys = ['complete', 'bipartite', 'star', 'cycle', 'wheel', 'line', 'custom']

            #Calculate the total width the buttons will take up
            spacing = 8
            total_width = 0
            for s in gt:
                total_width += getButtonDimensionData(s, f, 1.2, 1.2, height=32)[0]
                if not s == gt[len(gt)-1]:
                    total_width += spacing
            ww = int(SCREEN_WIDTH/2 - 0.5*total_width)
            for i, s in enumerate(gt):
                w = getButtonDimensionData(s, f, 1.2, 1.2, height=32)[0]
                bColor = (255,255,255)
                if i == self.graphType: bColor = (192,192,192)
                b = drawButton(s, f, [int(ww+0.5*w), int(SCREEN_HEIGHT/7)], 1.2, 1.2, height=32, bColor=bColor)
                ww += w + spacing
                if b[4]:
                    self.graphType = i
                    if i == 1 or i == 2:
                        self.nodeCount = 2
                        self.altNodeCount = 1
                    else: 
                        self.nodeCount = 1
                        self.altNodeCount = 0
            
            #Now Create the Buttons for adjusting the node count and alt node count if applicable
            ny = int(SCREEN_HEIGHT/5)
            if self.graphType == 1 or self.graphType == 2:
                ncX = int(SCREEN_WIDTH/4)
                ancX = int(SCREEN_WIDTH*3/4)
                if self.graphType == 1:
                    ancS = 'Left Vertex Count: '
                else: ancS = 'Star Vertex Count: '
            else:
                ncX = int(SCREEN_WIDTH/2)
            
            spacing = 4

            #Draw the Node Count Buttons
            #Determine total width of this section
            total_width = 0
            total_width += getButtonDimensionData('Vertex Count: ', f, 1.2, 1.2)[0] + spacing
            total_width += getButtonDimensionData('  +  ', f, 1.2, 1.2)[0] + spacing
            total_width += getButtonDimensionData(f'    {self.nodeCount}    ', f, 1.2, 1.2)[0] + spacing
            total_width += getButtonDimensionData('  -  ', f, 1.2, 1.2)[0]

            #Draw Vertex Count
            ww = int(ncX - 0.5*total_width)
            d = getButtonDimensionData('Vertex Count: ', f, 1.2, 1.2, height=32)[0]
            drawButton('Vertex Count: ', f, [int(ww + 0.5*d), ny], 1.2, 1.2, height=32, bordColor=(255,255,255), bColorDown=(255,255,25), bColorHover=(255,255,255), borderRadius=4)
            ww += d + spacing
            #Draw - button
            d = getButtonDimensionData('  -  ', f, 1.2, 1.2, height=32)[0]
            b = drawButton('  -  ', f, [int(ww + 0.5*d), ny], 1.2, 1.2, borderRadius=4)
            if b[4]:
                if self.nodeCount-1 > self.altNodeCount:
                    self.nodeCount -= 1
            ww += d + spacing
            #Draw Vertex Count Number
            d = getButtonDimensionData(f'    {self.nodeCount}    ', f, 1.2, 1.2, height=32)[0]
            drawButton(f'    {self.nodeCount}    ', f, [int(ww + 0.5*d), ny], 1.2, 1.2, height=32, bordColor=(255,255,255), bColorDown=(255,255,25), bColorHover=(255,255,255), borderRadius=4)
            ww += d + spacing
            #Draw the plus button
            d = getButtonDimensionData('  +  ', f, 1.2, 1.2, height=32)[0]
            b = drawButton('  +  ', f, [int(ww + 0.5*d), ny], 1.2, 1.2, borderRadius=4)
            if b[4]:
                if self.nodeCount < 10:
                    self.nodeCount += 1
            
            #Do the Same thing for the altNodeCount if necessary
            if not ncX == int(SCREEN_WIDTH/2):
                total_width = 0
                total_width += getButtonDimensionData(ancS, f, 1.2, 1.2)[0] + spacing
                total_width += getButtonDimensionData('  +  ', f, 1.2, 1.2)[0] + spacing
                total_width += getButtonDimensionData(f'    {self.altNodeCount}    ', f, 1.2, 1.2)[0] + spacing
                total_width += getButtonDimensionData('  -  ', f, 1.2, 1.2)[0]

                #Draw Vertex Count
                ww = int(ancX - 0.5*total_width)
                d = getButtonDimensionData(ancS, f, 1.2, 1.2, height=32)[0]
                drawButton(ancS, f, [int(ww + 0.5*d), ny], 1.2, 1.2, height=32, bordColor=(255,255,255), bColorDown=(255,255,25), bColorHover=(255,255,255), borderRadius=4)
                ww += d + spacing
                #Draw - button
                d = getButtonDimensionData('  -  ', f, 1.2, 1.2, height=32)[0]
                b = drawButton('  -  ', f, [int(ww + 0.5*d), ny], 1.2, 1.2, borderRadius=4)
                if b[4]:
                    if self.altNodeCount > 1:
                        self.altNodeCount -= 1
                ww += d + spacing
                #Draw Vertex Count Number
                d = getButtonDimensionData(f'    {self.altNodeCount}    ', f, 1.2, 1.2, height=32)[0]
                drawButton(f'    {self.altNodeCount}    ', f, [int(ww + 0.5*d), ny], 1.2, 1.2, height=32, bordColor=(255,255,255), bColorDown=(255,255,25), bColorHover=(255,255,255), borderRadius=4)
                ww += d + spacing
                #Draw the plus button
                d = getButtonDimensionData('  +  ', f, 1.2, 1.2, height=32)[0]
                b = drawButton('  +  ', f, [int(ww + 0.5*d), ny], 1.2, 1.2, borderRadius=4)
                if b[4]:
                    if self.altNodeCount < self.nodeCount-1:
                        self.altNodeCount += 1
                
                #Now we would draw the current graph settings here

                #Now Draw the Back and Accept Buttons
                

            
            

def getButtonDimensionData(text: str, font: pygame.font.Font, padX: float, padY: float, width: int = 0, height: int = 0) -> list:
    """Returns the width and height that a button with these parameters would produce

    Args:
        text (str): text that button will display
        font (pygame.font.Font): the Font obtject to use for the render
        padX (float): The amount of padding percentage horizontal (multiplicative) 1 = no padding
        padY (float): Same as padX but for vertical

    Returns:
        list: [width of button, height of button]
    """
    r = font.render(text, True, (0,0,0))
    if width == 0:
        w = padX*r.get_width()
    else:
        w = width
    if height == 0:
        h = padY*r.get_height()
    else:
        h = height
    return [w,h]

def drawButton(text: str, font: pygame.font.Font, center: list[int], padX: float, padY: float, width: int = 0, height: int = 0, tColor: pygame.Color = (0, 0, 0), borderRadius: int = -1, bColor: pygame.Color = (255, 255, 255), bColorHover: pygame.Color = (192, 192, 192), bColorDown: pygame.Color = (128, 128, 128), bordColor: pygame.Color = (0, 0, 0)) -> list:
    #Set the result of the boolean
    result = False
    #Render and Get Coordinates and Dimensions
    r = font.render(text, True, (0, 0, 0))
    if not width == 0:
        left = int(center[0] - 0.5*width)
        right = int(center[0] + 0.5*width)
    else:
        left = int(center[0] - 0.5*padX*r.get_width())
        right = int(center[0] + 0.5*padX*r.get_width())
    if not height == 0:
        top = int(center[1] - 0.5*height)
        bottom = int(center[1] + 0.5*height)
    else:
        top = int(center[1] - 0.5*padY*r.get_height())
        bottom = int(center[1] + 0.5*padY*r.get_height())
    tl = [left, top]
    br = [right, bottom]
    w = br[0] - tl[0]
    h = br[1] - tl[1]
    #Check if mouse is hovering and pressing
    if mouse_within(tl[0], tl[1], br[0], br[1]):
        bColor = bColorHover
        if pygame.mouse.get_pressed()[0]:
            bColor = bColorDown
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                result = True
    
    #Now we actually draw the button
    pygame.draw.rect(SCREEN, bColor, (tl[0], tl[1], w, h), border_radius=borderRadius)
    pygame.draw.rect(SCREEN, bordColor, (tl[0], tl[1], w, h), 1, border_radius=borderRadius)
    SCREEN.blit(r, (int(center[0] - 0.5*r.get_width()), int(center[1] - 0.5*r.get_height())))

    #Return whether the button was clicked or not
    return [tl[0], tl[1], br[0], br[1], result]

def resetClicks(click: bool):
    if not pygame.mouse.get_pressed()[0]:
        click = False
    return
    

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