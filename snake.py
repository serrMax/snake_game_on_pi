import unicornhat as unicorn
import time
import random   #for a random apple position
import RPi.GPIO as GPIO #for seven segment LED
from gpiozero import Button #for buttons


#       LED setup (used to display current level in the game)
GPIO.setmode(GPIO.BCM)

# LED segments to GPIO pins mapping
middle = 17
upper_left = 27
top = 22
upper_right = 10
lower_left = 9
bottom = 11
lower_right = 5
dot = 13

#setup output pins
GPIO.setup(middle, GPIO.OUT)      #GPIO 17 - middle segment of the LED
GPIO.setup(upper_left, GPIO.OUT)      #GPIO 27 - upper left 
GPIO.setup(top, GPIO.OUT)      #GPIO 22 - top
GPIO.setup(upper_right, GPIO.OUT)      #GPIO 10 - upper right
GPIO.setup(lower_left, GPIO.OUT)      #GPIO 9  - lower left
GPIO.setup(bottom, GPIO.OUT)      #GPIO 11 - bottom
GPIO.setup(lower_right, GPIO.OUT)      #GPIO 5  - lower right
GPIO.setup(dot, GPIO.OUT)      #GPIO 13 - dot


all_pins = [middle, upper_left, top, upper_right, lower_left, bottom, lower_right, dot]

def led_display_clean() :
    for i in all_pins :
        GPIO.output(i, GPIO.LOW)

def led_draw_number(number) :
    for i in number :
        GPIO.output(i, GPIO.HIGH)

def led_add_dot() :     #dot on LED will be ON when appleCounter == 5 meaning that only 1 more apple is needed for a level up
        GPIO.output(dot, GPIO.HIGH)

#list of LED segments to light up for each number
number_3 = [middle, top, upper_right, bottom, lower_right]
number_4 = [middle, upper_left, upper_right, lower_right]
number_5 = [middle, upper_left, top, bottom, lower_right]
number_6 = [middle, upper_left, top, lower_left, bottom, lower_right]
number_7 = [upper_left, top, upper_right, lower_right]

# LED level
currently_displayed = 'nothing'

#unicorn hat setup
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(0)     #0, 90, 180, 270 degrees
unicorn.brightness(0.25) # 0.0 - 1.0


left_black_button = Button(26) #left button
down_pink_button = Button(16) #down button
right_yellow_button = Button(23) #right button
up_blue_button = Button(6) #up button

#direction flags
go_right = True #starting snake direction
go_down = False
go_up = False
go_left = False

# starting snake position
head_col = 2
head_row = 0
mid_col = 1
mid_row = 0
tail_col = 0
tail_row = 0

snake_head_red = 0
snake_head_green = 255
snake_head_blue = 0

snake_body_red = 255
snake_body_green = 0
snake_body_blue = 0

apple_red = 0
apple_green = 0
apple_blue = 255

# if snake bites its tail or body pixel (head(green) + body(red) = yellow)
bitten_pixel_red = 255
bitten_pixel_green = 255
bitten_pixel_blue = 0

# current_level = number of snake body pixels
current_level = 3

# 5 apples for a current_level up
appleCounter = 0

def isAppleOnSnake(apple_col, apple_row, snake_coordinates) :
        for i in range(len(snake_coordinates)) :
                if apple_col == snake_coordinates[i][0] and apple_row == snake_coordinates[i][1] :
                        return True
        return False

# random apple coordinates, should not match any of the snake pixel coordinates
apple_col = 0
apple_row = 0
snake_coordinates_for_check = [[head_col, head_row], [mid_col, mid_row], [tail_col, tail_row]]

while isAppleOnSnake(apple_col, apple_row, snake_coordinates_for_check):
        apple_col = random.randint(0, 7)
        apple_row = random.randint(0, 7)

def display_frame(snake_coordinates, current_level, apple_col, apple_row) :
        unicorn.clear() #clear the display before showing the next frame
        head_col, head_row = snake_coordinates[0]
        mid_col, mid_row = snake_coordinates[1]
        tail_col, tail_row = snake_coordinates[len(snake_coordinates) - 1]

        # column, row, R, G, B
        unicorn.set_pixel(head_col, head_row, snake_head_red, snake_head_green, snake_head_blue)
        unicorn.set_pixel(mid_col, mid_row, snake_body_red, snake_body_green, snake_body_blue)
        unicorn.set_pixel(tail_col, tail_row, snake_body_red, snake_body_green, snake_body_blue)
                
        if current_level > 3 :
                mid_2_col, mid_2_row = snake_coordinates[2]
                unicorn.set_pixel(mid_2_col, mid_2_row, snake_body_red, snake_body_green, snake_body_blue)
                
                if current_level > 4 :
                        mid_3_col, mid_3_row = snake_coordinates[3]
                        unicorn.set_pixel(mid_3_col, mid_3_row, snake_body_red, snake_body_green, snake_body_blue)
                
                        if current_level > 5 :
                                mid_4_col, mid_4_row = snake_coordinates[4]
                                unicorn.set_pixel(mid_4_col, mid_4_row, snake_body_red, snake_body_green, snake_body_blue)
                
                                if current_level > 6 :
                                        mid_5_col, mid_5_row = snake_coordinates[5]
                                        unicorn.set_pixel(mid_5_col, mid_5_row, snake_body_red, snake_body_green, snake_body_blue)
                
        unicorn.set_pixel(apple_col, apple_row, apple_red, apple_green, apple_blue)
        unicorn.show()
        time.sleep(0.15) #pace of the game

# start of the game
snake_coordinates_for_display = [[head_col, head_row], [mid_col, mid_row], [tail_col, tail_row]]
display_frame(snake_coordinates_for_display, current_level, apple_col, apple_row)


def show_winning_animation() :  # Four parts : blue part, snakes eating blue, collision of snakes, falling snakes
        led_display_clean()
        unicorn.clear() #clear the display before showing the animation

        #       START OF THE BLUE PART
        blue_part_coordinates = [[0, 0], [0 , 1], [0, 2], [0, 3], [0, 4], [1, 4], [1, 5], [1, 6], [1, 7], [2, 7], [3, 6], [3, 5], [3, 4]]

        for i in blue_part_coordinates :
                unicorn.set_pixel(i[0], i[1], apple_red, apple_green, apple_blue)        #the left part
                unicorn.set_pixel(7 - i[0], i[1], apple_red, apple_green, apple_blue)    #since it is completely symmetrical, this is how we draw the right part
                unicorn.show()
                time.sleep(0.25)
        #       END OF THE BLUE PART

        #       START OF THE SNAKES EATING BLUE PART
        
        eating_path = [[0, 0], [0, 0]]  #just so that mid and tail parts of snakes do not raise out of range error
        eating_path += blue_part_coordinates #snakes will be eating the blue pixels
        snake_head_position = 2 #because head's index = 2, mid = 1, tail = 0

        while snake_head_position < len(eating_path) :
                unicorn.clear() #clear the display before showing the next frame
                #left snake
                unicorn.set_pixel(eating_path[snake_head_position - 1][0], eating_path[snake_head_position - 1][1], snake_body_red, snake_body_green, snake_body_blue)
                unicorn.set_pixel(eating_path[snake_head_position - 2][0], eating_path[snake_head_position - 2][1], snake_body_red, snake_body_green, snake_body_blue)
                unicorn.set_pixel(eating_path[snake_head_position][0], eating_path[snake_head_position][1], snake_head_red, snake_head_green, snake_head_blue)
                #right snake
                unicorn.set_pixel(7 - eating_path[snake_head_position - 1][0], eating_path[snake_head_position - 1][1], snake_body_red, snake_body_green, snake_body_blue)
                unicorn.set_pixel(7 - eating_path[snake_head_position - 2][0], eating_path[snake_head_position - 2][1], snake_body_red, snake_body_green, snake_body_blue)
                unicorn.set_pixel(7 - eating_path[snake_head_position][0], eating_path[snake_head_position][1], snake_head_red, snake_head_green, snake_head_blue)
                
                # remaining pixels of the path should be blue
                remaining_pixels_start = snake_head_position + 1
                while remaining_pixels_start < len(eating_path) :
                        unicorn.set_pixel(eating_path[remaining_pixels_start][0], eating_path[remaining_pixels_start][1], apple_red, apple_green, apple_blue) #left part
                        unicorn.set_pixel(7 - eating_path[remaining_pixels_start][0], eating_path[remaining_pixels_start][1], apple_red, apple_green, apple_blue) #right part
                        remaining_pixels_start += 1
                unicorn.show()
                time.sleep(0.15)

                eating_path.pop(0) #pixels behind the snake should be off

        #       END OF THE SNAKES EATING BLUE PART



        #       START OF THE COLLISION PART
        collision_path = [[3, 5],[3, 4],[3, 3],[3, 2],[3, 1],[3, 0],[2, 0],[1, 0],[0, 0],[0, 1],[0, 2],[0, 3],[0, 4],[1, 4],[2, 4],[3, 4]]
        snake_head_position = 2 #because head's index = 2, mid = 1, tail = 0 
        
        while snake_head_position < len(collision_path) :
                unicorn.clear()
                #left snake
                unicorn.set_pixel(collision_path[snake_head_position][0], collision_path[snake_head_position][1], snake_head_red, snake_head_green, snake_head_blue)
                unicorn.set_pixel(collision_path[snake_head_position - 1][0], collision_path[snake_head_position - 1][1], snake_body_red, snake_body_green, snake_body_blue)
                unicorn.set_pixel(collision_path[snake_head_position - 2][0], collision_path[snake_head_position - 2][1], snake_body_red, snake_body_green, snake_body_blue)
                #right snake
                unicorn.set_pixel(7 - collision_path[snake_head_position][0], collision_path[snake_head_position][1], snake_head_red, snake_head_green, snake_head_blue)
                unicorn.set_pixel(7 - collision_path[snake_head_position - 1][0], collision_path[snake_head_position - 1][1], snake_body_red, snake_body_green, snake_body_blue)
                unicorn.set_pixel(7 - collision_path[snake_head_position - 2][0], collision_path[snake_head_position - 2][1], snake_body_red, snake_body_green, snake_body_blue)
                unicorn.show()

                if len(collision_path) > 10 :
                        time.sleep(0.1) #high speed in the first part of the collision
                elif len(collision_path) <= 10 :
                        time.sleep(0.05)  #even higher in the second
                collision_path.pop(0) #snake moves 1 pixel forward

        #       END OF THE COLLISION PART

        #freeze after collision
        time.sleep(0.8)

        #       FALLING OF THE SNAKES
        for i in range(5, 8, 1) :
                unicorn.clear()
                #left snake
                unicorn.set_pixel(1, i, snake_body_red, snake_body_green, snake_body_blue)
                unicorn.set_pixel(2, i, snake_body_red, snake_body_green, snake_body_blue)
                unicorn.set_pixel(3, i, snake_head_red, snake_head_green, snake_head_blue)
                #right snake
                unicorn.set_pixel(4, i, snake_head_red, snake_head_green, snake_head_blue)
                unicorn.set_pixel(5, i, snake_body_red, snake_body_green, snake_body_blue)
                unicorn.set_pixel(6, i, snake_body_red, snake_body_green, snake_body_blue)
                unicorn.show()
                time.sleep(0.1)

        unicorn.clear()

def show_game_over_animation(game_over_snake_coordinates, level, head_bitten_pixel) :
        #common for all levels(5,6,7 -> only possible snake length for game over)
        mid_col, mid_row = game_over_snake_coordinates[0]
        mid_2_col, mid_2_row = game_over_snake_coordinates[1]
        mid_3_col, mid_3_row = game_over_snake_coordinates[2]
        tail_col, tail_row = game_over_snake_coordinates[len(game_over_snake_coordinates) - 1]
        
        unicorn.clear() #clear the display before the next frame
        unicorn.set_pixel(mid_col, mid_row, snake_body_red, snake_body_green, snake_body_blue)
        unicorn.set_pixel(mid_2_col, mid_2_row, snake_body_red, snake_body_green, snake_body_blue)
        unicorn.set_pixel(mid_3_col, mid_3_row, snake_body_red, snake_body_green, snake_body_blue)

        if level == 5 :
                unicorn.set_pixel(tail_col, tail_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)    # Green(head) + Red(body) = Yellow(crash point)
        
        elif level == 6 :
                unicorn.set_pixel(tail_col, tail_row, snake_body_red, snake_body_green, snake_body_blue)
                mid_4_col, mid_4_row = game_over_snake_coordinates[len(game_over_snake_coordinates) - 2]
                unicorn.set_pixel(mid_4_col, mid_4_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)  # Green(head) + Red(body) = Yellow(crash point)
        
        elif level == 7 :
                mid_4_col, mid_4_row = game_over_snake_coordinates[len(game_over_snake_coordinates) - 3]
                mid_5_col, mid_5_row = game_over_snake_coordinates[len(game_over_snake_coordinates) - 2]
                unicorn.set_pixel(mid_5_col, mid_5_row, snake_body_red, snake_body_green, snake_body_blue)

                if head_bitten_pixel == 'tail' :
                        unicorn.set_pixel(mid_4_col, mid_4_row, snake_body_red, snake_body_green, snake_body_blue)
                        unicorn.set_pixel(tail_col, tail_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)  # Green(head) + Red(body) = Yellow(crash point)
                
                elif head_bitten_pixel == 'mid_4' :
                        unicorn.set_pixel(mid_4_col, mid_4_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)  # Green(head) + Red(body) = Yellow(crash point)
                        unicorn.set_pixel(tail_col, tail_row, snake_body_red, snake_body_green, snake_body_blue)
        unicorn.show()
        time.sleep(1)

        unicorn.clear()  #clear the display before the next frame
        unicorn.show() #empty part of the blinking
        time.sleep(1)

        unicorn.set_pixel(mid_col, mid_row, snake_body_red, snake_body_green, snake_body_blue)
        unicorn.set_pixel(mid_2_col, mid_2_row, snake_body_red, snake_body_green, snake_body_blue)
        unicorn.set_pixel(mid_3_col, mid_3_row, snake_body_red, snake_body_green, snake_body_blue)

        if level == 5 :
                unicorn.set_pixel(tail_col, tail_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)    # Green(head) + Red(body) = Yellow(crash point)
        
        elif level == 6 :
                unicorn.set_pixel(tail_col, tail_row, snake_body_red, snake_body_green, snake_body_blue)
                unicorn.set_pixel(mid_4_col, mid_4_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)  # Green(head) + Red(body) = Yellow(crash point)
        
        elif level == 7 :
                unicorn.set_pixel(mid_5_col, mid_5_row, snake_body_red, snake_body_green, snake_body_blue)

                if head_bitten_pixel == 'tail' :
                        unicorn.set_pixel(mid_4_col, mid_4_row, snake_body_red, snake_body_green, snake_body_blue)
                        unicorn.set_pixel(tail_col, tail_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)  # Green(head) + Red(body) = Yellow(crash point)
                
                elif head_bitten_pixel == 'mid_4' :
                        unicorn.set_pixel(mid_4_col, mid_4_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)  # Green(head) + Red(body) = Yellow(crash point)
                        unicorn.set_pixel(tail_col, tail_row, snake_body_red, snake_body_green, snake_body_blue)
        unicorn.show()
        time.sleep(1)
        
        #snake falling part
        if level == 5 :
                while mid_row < 7 or mid_2_row < 7 or mid_3_row < 7 or tail_row < 7 :
                        unicorn.clear()  #clear the display before the next frame
                        if mid_row < 7 :
                                mid_row += 1
                                unicorn.set_pixel(mid_col, mid_row, snake_body_red, snake_body_green, snake_body_blue)
                        if mid_2_row < 7 :
                                mid_2_row += 1
                                unicorn.set_pixel(mid_2_col, mid_2_row, snake_body_red, snake_body_green, snake_body_blue)
                        if mid_3_row < 7 :
                                mid_3_row += 1
                                unicorn.set_pixel(mid_3_col, mid_3_row, snake_body_red, snake_body_green, snake_body_blue)
                        if tail_row < 7 :
                                tail_row += 1
                                unicorn.set_pixel(tail_col, tail_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)  # Green(head) + Red(body) = Yellow(crash point)
                        unicorn.show()
                        time.sleep(0.1)

        elif level == 6 :
                while mid_row < 7 or mid_2_row < 7 or mid_3_row < 7 or mid_4_row < 7 or tail_row < 7 :
                        unicorn.clear()  #clear the display before the next frame
                        if mid_row < 7 :
                                mid_row += 1
                                unicorn.set_pixel(mid_col, mid_row, snake_body_red, snake_body_green, snake_body_blue)
                        if mid_2_row < 7 :
                                mid_2_row += 1
                                unicorn.set_pixel(mid_2_col, mid_2_row, snake_body_red, snake_body_green, snake_body_blue)
                        if mid_3_row < 7 :
                                mid_3_row += 1
                                unicorn.set_pixel(mid_3_col, mid_3_row, snake_body_red, snake_body_green, snake_body_blue)
                        if mid_4_row < 7 :
                                mid_4_row += 1
                                unicorn.set_pixel(mid_4_col, mid_4_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)  # Green(head) + Red(body) = Yellow(crash point)
                        if tail_row < 7 :
                                tail_row += 1
                                unicorn.set_pixel(tail_col, tail_row, snake_body_red, snake_body_green, snake_body_blue)  
                        unicorn.show()
                        time.sleep(0.1)

        elif level == 7 :
                while mid_row < 7 or mid_2_row < 7 or mid_3_row < 7 or mid_4_row < 7 or mid_5_row < 7 or tail_row < 7 :
                        unicorn.clear()  #clear the display before the next frame
                        if mid_row < 7 :
                                mid_row += 1
                                unicorn.set_pixel(mid_col, mid_row, snake_body_red, snake_body_green, snake_body_blue)
                        if mid_2_row < 7 :
                                mid_2_row += 1
                                unicorn.set_pixel(mid_2_col, mid_2_row, snake_body_red, snake_body_green, snake_body_blue)
                        if mid_3_row < 7 :
                                mid_3_row += 1
                                unicorn.set_pixel(mid_3_col, mid_3_row, snake_body_red, snake_body_green, snake_body_blue)
                        if mid_5_row < 7 :
                                mid_5_row += 1
                                unicorn.set_pixel(mid_5_col, mid_5_row, snake_body_red, snake_body_green, snake_body_blue)
                        if mid_4_row < 7 :
                                mid_4_row += 1
                                if head_bitten_pixel == 'mid_4' :
                                        unicorn.set_pixel(mid_4_col, mid_4_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)  # Green(head) + Red(body) = Yellow(crash point)
                                
                                elif head_bitten_pixel == 'tail' :
                                        unicorn.set_pixel(mid_4_col, mid_4_row, snake_body_red, snake_body_green, snake_body_blue)
                        if tail_row < 7 :
                                tail_row += 1
                                if head_bitten_pixel == 'mid_4' :
                                        unicorn.set_pixel(tail_col, tail_row, snake_body_red, snake_body_green, snake_body_blue)  
                                
                                elif head_bitten_pixel == 'tail' :
                                        unicorn.set_pixel(tail_col, tail_row, bitten_pixel_red, bitten_pixel_green, bitten_pixel_blue)  # Green(head) + Red(body) = Yellow(crash point)
                        unicorn.show()
                        time.sleep(0.1)

try :
        while True : #game loop
                
                if left_black_button.is_pressed :    # go left
                        if go_right == False :
                                go_left = True
                                go_up = False
                                go_down = False
                        
                elif down_pink_button.is_pressed :   #go down
                        if go_up == False :
                                go_down = True
                                go_right = False
                                go_left = False
                        
                elif right_yellow_button.is_pressed : #go right
                        if go_left == False :
                                go_right = True
                                go_up = False
                                go_down = False

                elif up_blue_button.is_pressed :   #go up
                        if go_down == False :
                                go_up = True
                                go_left = False
                                go_right = False

                # -- -- PREPARING FOR THE NEXT FRAME BY MOVING THE SNAKE BODY BY 1 PIXEL
                if current_level == 7 :
                        if appleCounter != 5 :
                                tail_col, tail_row = mid_5_col, mid_5_row
                                mid_5_col, mid_5_row = mid_4_col, mid_4_row
                                mid_4_col, mid_4_row = mid_3_col, mid_3_row
                                mid_3_col, mid_3_row = mid_2_col, mid_2_row
                                mid_2_col, mid_2_row = mid_col, mid_row
                        elif appleCounter == 5 :
                                print("You won!")
                                show_winning_animation()
                                break

                if current_level == 6 :
                        if appleCounter != 5 :
                                tail_col, tail_row = mid_4_col, mid_4_row
                        elif appleCounter == 5 :    #add new pixel (mid_5)
                                appleCounter = 0
                                current_level = 7
                                mid_5_col, mid_5_row = mid_4_col, mid_4_row

                        mid_4_col, mid_4_row = mid_3_col, mid_3_row
                        mid_3_col, mid_3_row = mid_2_col, mid_2_row
                        mid_2_col, mid_2_row = mid_col, mid_row

                if current_level == 5 :
                        if appleCounter != 5 :
                                tail_col, tail_row = mid_3_col, mid_3_row
                        elif appleCounter == 5 :    #add new pixel (mid_4)
                                appleCounter = 0
                                current_level = 6
                                mid_4_col, mid_4_row = mid_3_col, mid_3_row

                        mid_3_col, mid_3_row = mid_2_col, mid_2_row
                        mid_2_col, mid_2_row = mid_col, mid_row

                if current_level == 4 : 
                        if appleCounter != 5 :
                                tail_col, tail_row = mid_2_col, mid_2_row        
                        elif appleCounter == 5 : #add new pixel (mid_3)
                                appleCounter = 0
                                current_level = 5
                                mid_3_col, mid_3_row = mid_2_col, mid_2_row

                        mid_2_col, mid_2_row = mid_col, mid_row
                        
                if current_level == 3 :
                        if appleCounter != 5 :
                                tail_col, tail_row = mid_col, mid_row
                        elif appleCounter == 5 : #add new pixel (mid_2)
                                appleCounter = 0
                                current_level = 4
                                mid_2_col, mid_2_row = mid_col, mid_row

                #in any case, mid pixel follows the head, common for every level and case
                mid_col, mid_row = head_col, head_row

                # -- -- END OF PREP
                                
                
                # next coordinates for the snake head
                if go_right :
                        if head_col == 7 :
                                head_col = 0
                        elif head_col != 7 :
                                head_col += 1      
                elif go_left :
                        if head_col == 0 :
                                head_col = 7
                        elif head_col != 0 :
                                head_col -= 1      
                elif go_up :
                        if head_row == 0 :
                                head_row = 7
                        elif head_row != 0 :
                                head_row -= 1
                elif go_down :
                        if head_row == 7 :
                                head_row = 0
                        elif head_row != 7 :
                                head_row += 1

                # -- -- -- CHECK FOR "GAME OVER"
                        # If game over, blinking animation with the final snake position
                if current_level == 5 :
                        if head_col == tail_col and head_row == tail_row :
                                snake_coordinates_for_game_over_animation = [[mid_col, mid_row], [mid_2_col, mid_2_row], [mid_3_col, mid_3_row], [tail_col, tail_row]]
                                show_game_over_animation(snake_coordinates_for_game_over_animation, current_level, "tail")
                                print("You lost")
                                break

                elif current_level == 6 :
                        if (head_col == tail_col and head_row == tail_row) or (head_col == mid_4_col and head_row == mid_4_row):
                                snake_coordinates_for_game_over_animation = [[mid_col, mid_row], [mid_2_col, mid_2_row], [mid_3_col, mid_3_row], [mid_4_col, mid_4_row], [tail_col, tail_row]]
                                show_game_over_animation(snake_coordinates_for_game_over_animation, current_level, "mid_4")
                                print("You lost")
                                break

                elif current_level == 7 :
                        if (head_col == tail_col and head_row == tail_row) or (head_col == mid_4_col and head_row == mid_4_row) or (head_col == mid_5_col and head_row == mid_5_row):
                                snake_coordinates_for_game_over_animation = [[mid_col, mid_row], [mid_2_col, mid_2_row], [mid_3_col, mid_3_row], [mid_4_col, mid_4_row], [mid_5_col, mid_5_row], [tail_col, tail_row]]
                                if head_col == tail_col and head_row == tail_row :
                                        show_game_over_animation(snake_coordinates_for_game_over_animation, current_level, "tail")
                                elif head_col == mid_4_col and head_row == mid_4_row :
                                        show_game_over_animation(snake_coordinates_for_game_over_animation, current_level, "mid_4")
                                print("You lost")
                                break
                # -- -- -- END OF "GAME OVER" CHECK
                
                #if the apple is eaten, increase the appleCounter and create new apple
                if apple_col == head_col and apple_row == head_row :
                        appleCounter += 1
                        if current_level == 3 :
                                snake_coordinates_for_check = [[head_col, head_row], [mid_col, mid_row], [tail_col, tail_row]]
                                while isAppleOnSnake(apple_col, apple_row, snake_coordinates_for_check) :
                                        apple_col = random.randint(0, 7)
                                        apple_row = random.randint(0, 7)
                        elif current_level == 4 :
                                snake_coordinates_for_check = [[head_col, head_row], [mid_col, mid_row], [mid_2_col, mid_2_row], [tail_col, tail_row]]
                                while isAppleOnSnake(apple_col, apple_row, snake_coordinates_for_check) :
                                        apple_col = random.randint(0, 7)
                                        apple_row = random.randint(0, 7)
                        elif current_level == 5 :
                                snake_coordinates_for_check = [[head_col, head_row], [mid_col, mid_row], [mid_2_col, mid_2_row], [mid_3_col, mid_3_row], [tail_col, tail_row]]
                                while isAppleOnSnake(apple_col, apple_row, snake_coordinates_for_check):
                                        apple_col = random.randint(0, 7)
                                        apple_row = random.randint(0, 7)
                        elif current_level == 6 :
                                snake_coordinates_for_check = [[head_col, head_row], [mid_col, mid_row], [mid_2_col, mid_2_row], [mid_3_col, mid_3_row], [mid_4_col, mid_4_row], [tail_col, tail_row]]
                                while isAppleOnSnake(apple_col, apple_row, snake_coordinates_for_check):
                                        apple_col = random.randint(0, 7)
                                        apple_row = random.randint(0, 7)
                        elif current_level == 7 :
                                snake_coordinates_for_check = [[head_col, head_row], [mid_col, mid_row], [mid_2_col, mid_2_row], [mid_3_col, mid_3_row], [mid_4_col, mid_4_row], [mid_5_col, mid_5_row], [tail_col, tail_row]]
                                while isAppleOnSnake(apple_col, apple_row, snake_coordinates_for_check):
                                        apple_col = random.randint(0, 7)
                                        apple_row = random.randint(0, 7)
                #display the frame
                if current_level == 3 :
                        snake_coordinates_for_display = [[head_col, head_row], [mid_col, mid_row], [tail_col, tail_row]]               
                        display_frame(snake_coordinates_for_display, current_level, apple_col, apple_row)

                elif current_level == 4 :
                        snake_coordinates_for_display = [[head_col, head_row], [mid_col, mid_row], [mid_2_col, mid_2_row], [tail_col, tail_row]]
                        display_frame(snake_coordinates_for_display, current_level, apple_col, apple_row)

                elif current_level == 5 :
                        snake_coordinates_for_display = [[head_col, head_row], [mid_col, mid_row], [mid_2_col, mid_2_row], [mid_3_col, mid_3_row],[tail_col, tail_row]]
                        display_frame(snake_coordinates_for_display, current_level, apple_col, apple_row)

                elif current_level == 6 :
                        snake_coordinates_for_display = [[head_col, head_row], [mid_col, mid_row], [mid_2_col, mid_2_row], [mid_3_col, mid_3_row], [mid_4_col, mid_4_row], [tail_col, tail_row]]
                        display_frame(snake_coordinates_for_display, current_level, apple_col, apple_row)

                elif current_level == 7 :

                        if appleCounter != 5 :
                                snake_coordinates_for_display = [[head_col, head_row], [mid_col, mid_row], [mid_2_col, mid_2_row], [mid_3_col, mid_3_row], [mid_4_col, mid_4_row], [mid_5_col, mid_5_row],[tail_col, tail_row]]
                                display_frame(snake_coordinates_for_display, current_level, apple_col, apple_row)
                        
                        # if it is the last frame, there should not be the next apple
                        elif appleCounter == 5 :
                                unicorn.clear() #clear the display before showing the last frame
                                # column, row, R, G, B
                                unicorn.set_pixel(head_col, head_row, snake_head_red, snake_head_green, snake_head_blue)
                                unicorn.set_pixel(mid_col, mid_row, snake_body_red, snake_body_green, snake_body_blue)
                                unicorn.set_pixel(tail_col, tail_row, snake_body_red, snake_body_green, snake_body_blue)
                                unicorn.set_pixel(mid_2_col, mid_2_row, snake_body_red, snake_body_green, snake_body_blue)
                                unicorn.set_pixel(mid_3_col, mid_3_row, snake_body_red, snake_body_green, snake_body_blue)
                                unicorn.set_pixel(mid_3_col, mid_3_row, snake_body_red, snake_body_green, snake_body_blue)
                                unicorn.set_pixel(mid_4_col, mid_4_row, snake_body_red, snake_body_green, snake_body_blue)
                                unicorn.set_pixel(mid_3_col, mid_3_row, snake_body_red, snake_body_green, snake_body_blue)
                                unicorn.set_pixel(mid_4_col, mid_4_row, snake_body_red, snake_body_green, snake_body_blue)
                                unicorn.set_pixel(mid_5_col, mid_5_row, snake_body_red, snake_body_green, snake_body_blue)
                                unicorn.show()
                                time.sleep(0.2)

                #display the current level on LED
                if currently_displayed == 'nothing' :
                        led_draw_number(number_3)
                        currently_displayed = '3'
                elif currently_displayed == '3' :
                        if appleCounter == 4 :
                                led_add_dot()
                        elif appleCounter == 5 :
                                led_display_clean()
                                led_draw_number(number_4)
                                currently_displayed = '4'
                elif currently_displayed == '4' :
                        if appleCounter == 4 :
                                led_add_dot()
                        elif appleCounter == 5 :
                                led_display_clean()
                                led_draw_number(number_5)
                                currently_displayed = '5'
                elif currently_displayed == '5' :
                        if appleCounter == 4 :
                                led_add_dot()
                        elif appleCounter == 5 :
                                led_display_clean()
                                led_draw_number(number_6)
                                currently_displayed = '6'
                elif currently_displayed == '6' :
                        if appleCounter == 4 :
                                led_add_dot()
                        elif appleCounter == 5 :
                                led_display_clean()
                                led_draw_number(number_7)
                                currently_displayed = '7'
                elif currently_displayed == '7' :
                        if appleCounter == 4 :
                                led_add_dot()
                        
finally :
        #clean both unicornhat and led
        unicorn.off()
        led_display_clean()