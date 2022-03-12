import pygame
from numpy import argmax, array, transpose
from keras.models import load_model

GRAY = (200, 200, 200)
GRAY2 = (180, 180, 180)
class Evaluator:
    def __init__(self):
        self.model = load_model('modelo.h5')

    def predict(self,data):
        data = transpose(array(data)).reshape(1, 28, 28, 1)
        data = data /255
        predict_value = self.model(data)
        return transpose(array(predict_value))

class ImageNum:
    def __init__(self,pos_x,pos_y,factor):
        self.factor = factor
        self.size = 28
        self.data = []
        for i in range(self.size):
            _aux = []
            for j in range(self.size):
                _aux.append(0)
            self.data.append(_aux)
        self.rects = []
        for i in range(self.size):
            _aux = []
            for j in range(self.size):
                _aux.append(pygame.Rect((i*self.factor+pos_x, j*self.factor+pos_y),(self.factor,self.factor)))
            self.rects.append(_aux)

    def get1Ddata(self):
        out = []
        for i in range(self.size):
            for j in range(self.size):
                out.append(self.data[i][j])
        return out

    def click(self, mouse_x, mouse_y):
        for i in range(len(self.rects)):
            for j in range(len(self.rects)):
                if self.rects[i][j].collidepoint(mouse_x, mouse_y):
                    self.data[i][j] += 255
                    try:
                        esquina = 50
                        cruz = 100
                        self.data[i+1][j+1] += esquina
                        self.data[i+1][j-1] += esquina
                        self.data[i-1][j+1] += esquina
                        self.data[i-1][j-1] += esquina
                        self.data[i+1][j] += cruz
                        self.data[i-1][j] += cruz
                        self.data[i][j+1] += cruz
                        self.data[i][j-1] += cruz
                    except:
                        pass

    def draw(self, screen):
        for i in range(self.size):
            for j in range(self.size):
                self.data[i][j] = max(min(255, self.data[i][j]), 0)
                _color = [self.data[i][j]]*3
                pygame.draw.rect(screen, _color, self.rects[i][j], 0)

class Text_rect:
    def __init__(self, rect, text, color):
        self.rect = rect
        self.text = text
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(self.text, False, (0, 0, 0))
        text_rect = textsurface.get_rect(center=self.rect.center)
        screen.blit(textsurface, text_rect)

class App:

    def __init__(self):
        self.factor = 15

        self.canvas_rect = pygame.Rect((0, 0), (28 * self.factor, 28 * self.factor))
        self.info_rect = pygame.Rect((self.canvas_rect.width, 0), (16 * self.factor, 44 * self.factor))
        self.display_rect = self.canvas_rect.union(self.info_rect)
        self.buttoms_rect = pygame.Rect(self.canvas_rect.bottomleft, (28 * self.factor, 16 * self.factor))
        self.screen = pygame.display.set_mode(self.display_rect.size)

        self.image = ImageNum(0,0,self.factor)
        rect_buttom = pygame.Rect(self.canvas_rect.bottomleft,(10*self.factor,3*self.factor))
        self.reset_buttom = Text_rect(rect_buttom, "Reset", (200, 0, 0))
        self.reset_buttom.rect.midleft = self.buttoms_rect.midleft
        self.reset_buttom.rect.x += self.factor*2
        self.reset_buttom.rect.y += self.factor*2
        rect_buttom = pygame.Rect(self.canvas_rect.bottomleft,(10*self.factor,3*self.factor))
        self.evaluate_buttom = Text_rect(rect_buttom, "Evaluate", (0, 200, 0))
        self.evaluate_buttom.rect.midright = self.buttoms_rect.midright
        self.evaluate_buttom.rect.x -= self.factor*2
        self.evaluate_buttom.rect.y += self.factor*2
        rect_buttom = pygame.Rect(self.canvas_rect.bottomleft,(10*self.factor,3*self.factor))
        self.evaluate_num = Text_rect(rect_buttom, "X", (255, 255, 255))
        self.evaluate_num.rect.center = self.buttoms_rect.center
        self.evaluate_num.rect.y -= self.factor*4

        self.evaluator = Evaluator()
        self.evaluator.predict(self.image.data)

        self.info_nums = []
        for i in range(10):
            _rect = pygame.Rect(self.info_rect.topleft, (self.factor*10,self.factor*2))
            _rect.center = self.info_rect.center
            _rect.y = (i * _rect.height) + (self.factor*2*i) + self.factor*2
            self.info_nums.append(Text_rect(_rect, '{}: 0.00%'.format(i), (240, 240, 240)))

        pygame.font.init()
        self.run()

    def reset_click(self):
        for i in range(self.image.size):
            for j in range(self.image.size):
                self.image.data[i][j] = 0
        self.evaluate_num.text = "X"
        for i in range(len(self.info_nums)):
            self.info_nums[i].text = '{}: 0.00%'.format(i)

    def evaluate_click(self):
        prediction = self.evaluator.predict(self.image.data)
        self.evaluate_num.text = str(argmax(prediction))
        for i in range(len(self.info_nums)):
            self.info_nums[i].text = '{}: {:.2f}%'.format(i,float(prediction[i])*100)

    def run(self):
        _exit = False
        isPressed = False
        while not _exit:
            pygame.draw.rect(self.screen, GRAY, self.info_rect)
            pygame.draw.rect(self.screen, GRAY2, self.buttoms_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _exit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    isPressed = True
                    (x, y) = pygame.mouse.get_pos()
                    self.image.click(x, y)
                    if self.reset_buttom.rect.collidepoint(x,y):
                        self.reset_click()
                    if self.evaluate_buttom.rect.collidepoint(x,y):
                        self.evaluate_click()
                elif event.type == pygame.MOUSEBUTTONUP:
                    isPressed = False
                if event.type == pygame.MOUSEMOTION and isPressed == True:
                    (x, y) = pygame.mouse.get_pos()
                    self.image.click(x, y)
            self.image.draw(self.screen)
            self.reset_buttom.draw(self.screen)
            self.evaluate_buttom.draw(self.screen)
            self.evaluate_num.draw(self.screen)
            for num in self.info_nums:
                num.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        exit(0)

if __name__ == "__main__":
    App()
