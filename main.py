'''Snake Game
Creator : Amal Irfan'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color,Rectangle
from kivy.properties import NumericProperty
from includes import *
from kivy.clock import Clock
from random import randrange

class Square(Widget):
    '''Square is a Widget containing a Rectangle
    whose color is defined by bg_color'''
    pass
class SnakePart(Square):
    '''Snake part is a Square. what's special about
    it is that it's colors are randomly chosen from
    includes.SNAKE_COLORS'''
    pass
class Food(Square):
    '''Food is a Square. what's special about it is
    that, it's colors are randomly chosen from
    includes.SNAKE_COLORS'''
    pass
class ScoreLabel(Label):pass

# finished
class GameScreen(Screen):
    '''GameScreen is the main game window. this is
    where everything is drawn on'''
    step_size = SQUARE_SIZE
    snake_parts = []
    movement_x = 0
    movement_y = 0
    
    # finished
    def new(self):
        self.clear_widgets()
        self.snake_parts = []
        self.movement_x = 0
        self.movement_y = 0
        head = SnakePart()
        head.pos = (0,0)
        head.x = 0
        head.y = 0
        self.snake_parts.append(head)
        self.add_widget(head)
        food = Food()
        food.x = randrange(0,self.width-food.width,self.step_size)
        food.y = randrange(0,self.height-food.width,self.step_size)
        self.add_widget(food)
        self.food = food
        self.score_label = Label()
        self.add_widget(self.score_label)
        self.run = True

    # finished
    def next_frame(self,d):
        if not self.run:return True
        # Move snake
        head = self.snake_parts[0]
        food = self.food
        last_x = self.snake_parts[-1].x
        last_y = self.snake_parts[-1].y
        # Move snake body
        for i, part in enumerate(self.snake_parts):
            if i == 0:continue
            part.new_x = self.snake_parts[i-1].x
            part.new_y = self.snake_parts[i-1].y
        for part in self.snake_parts[1:]:
            part.x = part.new_x
            part.y = part.new_y
        # Move snake head
        head.x += self.movement_x
        head.y += self.movement_y
        # Check if snake collide with food
        if self.widgets_collides(head,food):
            self.remove_widget(food)
            food = self.food = Food()
            self.add_widget(food)
            food.x = randrange(0,self.width-food.width,self.step_size)
            food.y = randrange(0,self.height-food.width,self.step_size)
            new_part = SnakePart()
            new_part.x = last_x
            new_part.y = last_y
            self.snake_parts.append(new_part)
            self.add_widget(new_part)
        # Check if snake collide with snake
        for part in self.snake_parts[1:]:
            if self.widgets_collides(part,head):
                main.game_over()
                return False

        # Check if snake collide with walls
        if head.x < 0 or head.right > self.right\
        or head.y < 0 or head.top > self.top:
            main.game_over()
            return False
        self.score_label.text= str(len(self.snake_parts)-1)
    
    # finished
    def on_touch_up(self,touch):
        # delta positions
        dx = touch.opos[0]-touch.x
        dy = touch.opos[1]-touch.y
        
        if abs(dx) == abs(dy):return
        if abs(dx) > abs(dy):
            # Move left or right
            self.movement_y = 0
            if dx < 0:
                # Move right
                self.movement_x = self.step_size if not self.movement_x else self.movement_x
            else:
                # Move left
                self.movement_x = -self.step_size if not self.movement_x else self.movement_x
        else:
            # Move up or down
            self.movement_x = 0
            if dy < 0:
                # Move up
                self.movement_y = self.step_size if not self.movement_y else self.movement_y
            else:
                # Move down
                self.movement_y = -self.step_size if not self.movement_y else self.movement_y
    
    # finished
    def widgets_collides(self,wid1,wid2):
        ''' takes two widgets and returns True if 
        the are colliding with each other else
        returns False '''
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        return True

class MainApp(App):
    '''MainApp is The Main App. Nothing special
    here runs self.root.new() and schedules
    self.root.next_frame() to run every 1/4 of
    a second in the function on_start'''

    # finished
    def start_game(self):
        self.root.ids.game.new()
        Clock.schedule_interval(self.root.ids.game.next_frame,1/4)
    def game_over(self):
        self.root.current = 'main'

main = MainApp()

if __name__=='__main__':
    main.run()