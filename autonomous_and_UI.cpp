# ######################################
#         Brain Startup Screen         #
# ######################################
# Auton selector based on position of field
def startup_brain():
   red_1 = [30, 46 - 20, 100, 50]
   red_2 = [30, 120 + 46 - 20, 100, 50]
   blue_1 = [20 + 130 + 170 + 20, 46 - 20, 100, 50]
   blue_2 = [20 + 130 + 170 + 20, 120 + 46 - 20, 100, 50]
   skills = [20 + 160, 200, 103, 50]


   brain.screen.set_font(FontType.MONO30)
   brain.screen.set_fill_color(Color.WHITE)
   brain.screen.draw_rectangle(0, 0, 480, 272)
   brain.screen.set_pen_color(Color.BLUE)
   #brain.screen.draw_rectangle(10, 10, 460, 74, Color.BLACK)
   brain.screen.set_cursor(1,9)
   brain.screen.print("94027A SharkBot")


   # Replace with photo of field
   brain.screen.draw_image_from_file('field.bmp', 155, 46 - 20)


   brain.screen.set_pen_color(Color.BLACK)


   # Create buttons
   brain.screen.set_pen_width(0)
   brain.screen.set_fill_color(Color.RED)
   brain.screen.draw_rectangle(red_1[0], red_1[1], red_1[2], red_1[3])
   brain.screen.set_cursor(2,3)
   brain.screen.print("Red 1")
   brain.screen.draw_rectangle(red_2[0], red_2[1], red_2[2], red_2[3])
   brain.screen.set_cursor(6,3)
   brain.screen.print("Red 2")


   brain.screen.set_fill_color(Color.BLUE)
   brain.screen.draw_rectangle(blue_1[0], blue_1[1], blue_1[2], blue_1[3])
   brain.screen.set_cursor(2,24)
   brain.screen.print("Blue 1")
   brain.screen.draw_rectangle(blue_2[0], blue_2[1], blue_2[2], blue_2[3])
   brain.screen.set_cursor(6,24)
   brain.screen.print("Blue 2")


   # Create Skills button
   brain.screen.set_fill_color(Color.YELLOW)
   brain.screen.draw_rectangle(skills[0], skills[1], skills[2], skills[3])
   brain.screen.set_cursor(8,13.5)
   brain.screen.print("Skills")


   # Pause until a button is pressed
   while brain.screen.pressing() == False:
       wait(5, MSEC)
   # Select auton from input
   if brain.screen.pressing():
       x = brain.screen.x_position()
       y = brain.screen.y_position()


       if x > red_1[0] and x < red_1[0] + red_1[2]:
           if y > red_1[1] and y < red_1[1] + red_1[3]:
               confirmation_brain(1, -1)
               return 1
           if y > red_2[1] and y < red_2[1] + red_2[3]:
               confirmation_brain(2, -1)
               return 2
       elif x > blue_1[0] and x < blue_1[0] + blue_1[2]:
           if y > blue_1[1] and y < blue_1[1] + blue_1[3]:
               confirmation_brain(3, 1)
               return 3
           if y > blue_2[1] and y < blue_2[1] + blue_2[3]:
               confirmation_brain(4, 1)
               return 4
       elif x > skills[0] and x < skills[0] + skills[2]:
           if y > skills[1] and y < skills[1] + skills[3]:
               confirmation_brain(5, 1)
               return 5
       else:
           startup_brain()


# ######################################
#         Confirmation Screen          #
# ######################################
# Confirms selected autonomous program
def confirmation_brain(auton, flipped):
   global which_auton, flip
   # Fixed bug: prevents prior press from carrying over
   while brain.screen.pressing():
       wait(5, MSEC)


   # Clear screen
   brain.screen.set_fill_color(Color.WHITE)
   brain.screen.set_font(FontType.MONO20)
   brain.screen.draw_rectangle(0, 0, 480, 272)
   brain.screen.set_cursor(1, 3)


   # Prompt with selected autonomous
   if auton == 1:
       brain.screen.print("You selected: red alliance by the blue goal")
   elif auton == 2:
       brain.screen.print("You selected: red alliance by the red goal")
   elif auton == 3:
       brain.screen.print("You selected: blue alliance by the blue goal")
   elif auton == 4:
       brain.screen.print("You selected: blue alliance by the red goal")
   elif auton == 5:
       brain.screen.print("You selected: skills")


   yes = [135, 60, 200, 60]
   no = [135, 140, 200, 60]


   #Confirm selection button
   brain.screen.set_fill_color(Color.GREEN)
   brain.screen.draw_rectangle(yes[0], yes[1], yes[2], yes[3])
   brain.screen.set_cursor(5,16)
   brain.screen.print("Confirm selection")


   # Change selection button
   brain.screen.set_fill_color(Color.RED)
   brain.screen.draw_rectangle(no[0], no[1], no[2], no[3])
   brain.screen.set_cursor(9,16)
   brain.screen.print("Change selection")


   # Wait until pressed by user
   while brain.screen.pressing() == False:
       wait(5, MSEC)


   # If confirmed, display match brain and finalize auton
   # Else, prompt for auton selection again
   if brain.screen.pressing():
       x = brain.screen.x_position()
       y = brain.screen.y_position()


       if y > yes[1] and y < yes[1] + yes[3]:
           which_auton = auton
           flip = flipped
           match_brain()
       elif y > no[1] and y < no[1] + no[3]:
           startup_brain()
  
# ######################################
#             Match Brain              #
# ######################################
# Displays a shark during the match
def match_brain():
   brain.screen.set_fill_color(Color.WHITE)
   brain.screen.draw_rectangle(0, 0, 480, 272)
   brain.screen.draw_image_from_file('shark.bmp', 30, -3)
