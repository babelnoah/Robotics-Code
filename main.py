# ----------------------------------------------------------------------------- #
#                                                                               #                                                                          
#    Project:        CompCode Sharkbot 3.0 (94027A)                             #
#    Module:         main.py                                                    #
#    Author:         Isabel Prado-Tucker and VEX                                #
#    Created:        Sat Jan 06 2023                                            #
#    Description:    RoboEvents VEX Signature Event @ ICC comp program          # 
#                    UI for auton selection, uses inertial for precision        #
#                                                                               #                                                                         
#    Configuration:  V5 Sharkbot                                                #
#                    Controller                                                 #
#                    Catapult Motor in Port 19                                  #
#                    Catapult Motor in Port 20                                  #
#                    Left Front Motor in Port 11                                #
#                    Left Back Motor in Port 12                                 #
#                    Right Front Motor in Port 13                               #
#                    Right Back Motor in Port 14                                #
#                    Inertial Sensor in Port 4                                  #
#                    Wing Pneumatic 1 in Port A                                 #
#                    Wing Pneumatic 2 in Port B                                 #
#                                                                               #                                                                          
# ----------------------------------------------------------------------------- #

#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
Cata = Motor(Ports.PORT16, GearSetting.RATIO_6_1, True)
Cata.set_velocity(100, PERCENT)
expander = Triport(Ports.PORT19)
digital_out_a = DigitalOut(expander.a)
digital_out_b = DigitalOut(expander.b)
digital_out_c = DigitalOut(expander.c)
digital_out_d = DigitalOut(expander.d)
Climber_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
Climber_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True)
Climber = MotorGroup(Climber_motor_a, Climber_motor_b)
Climber.set_velocity(100, PERCENT)
Intake = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
Intake.set_velocity(100, PERCENT)

left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True) # Front
left_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
left_motor_c = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True) # Back
left_drive_smart = MotorGroup(left_motor_a, left_motor_b, left_motor_c)

right_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
right_motor_c = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b, right_motor_c)

inertia = Inertial(Ports.PORT7) 
left_drive_rotation = Rotation(Ports.PORT9) 
right_drive_rotation = Rotation(Ports.PORT10)
gps = Gps(Ports.PORT18)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, inertia, 220, 267, 267)

# add a small delay for sensor reset/callibration
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
controller_1_right_shoulder_control_motors_stopped = True
controller_1_left_shoulder_control_motors_stopped = True
controller_1_intake_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False
pneumatics_on = False
program = 0

# CREATE GLOBAL VARIABLES
# Which autonomous program to run
which_auton = 0
# Set if need to reverse auton values for opp side of field
##### BLUE IS NOT FLIPPED, RED IS FLIPPED
flip = 0 # Default, don't need to change values at all

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled, controller_1_left_shoulder_control_motors_stopped, controller_1_intake_motors_stopped, pneumatics_on
    # process the controller input every 20 milliseconds
    # update the motors based on the input values

    # Set pneumatic buttons
    controller_1.buttonLeft.pressed(pneumatic_off)
    controller_1.buttonA.pressed(pneumatic_on)

    controller_1.buttonX.pressed(endgame_on)
    controller_1.buttonUp.pressed(endgame_off)
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            drivetrain_left_side_speed = (controller_1.axis3.position() + controller_1.axis1.position()) 
            drivetrain_right_side_speed = (controller_1.axis3.position() - controller_1.axis1.position()) 
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)

            # Control Intake
            if controller_1.buttonL2.pressing():
                Intake.spin(REVERSE)
                controller_1_intake_motors_stopped = False
            elif controller_1.buttonR2.pressing():
                Intake.spin(FORWARD)
                controller_1_intake_motors_stopped = False
            elif not controller_1_intake_motors_stopped:
                Intake.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_intake_motors_stopped = True

            # check the buttonR1/buttonR2 status
            # to control Cata
            if controller_1.buttonR1.pressing():
                Cata.spin(REVERSE)
                controller_1_right_shoulder_control_motors_stopped = False
            elif controller_1.buttonL1.pressing():
                Cata.stop()
                controller_1_right_shoulder_control_motors_stopped = True
            
        # wait before repeating the process
        wait(20, MSEC)
            
#endregion VEXcode Generated Robot Configuration

# PID Controller
def turn_with_pid(req_heading):
    # inspired by https://smithcsrobot.weebly.com/uploads/6/0/9/5/60954939/pid_control_document.pdf
    Kp = 0.5
    Ki = 0.2
    Kd = 0.1
    Threshold = 0.01

    integral = 0
    derivative = 0
    error = 0
    last_error = 0
    time_error = 0
    inertia.reset_rotation()
    inertia.reset_heading()
    while (True):
        error = req_heading - inertia.heading()
        if (abs(error) < Threshold):
            break
        derivative = error - last_error
        speed = Kp*error + Kd*derivative
        if (speed > 100):
            speed = 100
        elif (speed < 0):
            speed = 0
        last_error = error
        left_drive_smart.spin(FORWARD, speed, VelocityUnits.PERCENT)
        right_drive_smart.spin(FORWARD, -1 * speed, VelocityUnits.PERCENT)
    drivetrain.stop()
    pass

def drive_with_pid(req_distance):
    # Inspired by https://smithcsrobot.weebly.com/uploads/6/0/9/5/60954939/pid_control_document.pdf
    Kp = 0.5
    Ki = 0.2
    Kd = 0.1
    Threshold = 0.01

    integral = 0
    derivative = 0
    error = 0
    last_error = 0
    time_error = 0
    inertia.reset_rotation()
    inertia.reset_heading()
    right_drive_rotation.reset_position()
    left_drive_rotation.reset_position()
    while (True):
        error = req_distance - ((right_drive_rotation.angle() + left_drive_rotation.angle()) / 2 * 300) 
        if (abs(error) < Threshold):
            break
        derivative = error - last_error
        speed = Kp*error + Kd*derivative
        if (speed > 100):
            speed = 100
        elif (speed < 0):
            speed = 0
        last_error = error
        drivetrain.drive(FORWARD, speed, PERCENT)
    drivetrain.stop()
    pass

def go_to_location(x, y):
    pass
    
# ######################################
#  Starting Position 1 (opposite side) #
# ######################################
# Remove match load
# Put pre-load into the goal
# Touch elevation bar
# 2/3 AWP, 5-points
def autonomous_opp():
    inertia.reset_heading()
    inertia.reset_rotation()
    drivetrain.set_drive_velocity(75, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)
    wait(1, SECONDS)
    endgame_on()
    Intake.spin(FORWARD)

    # Remove match load
    drivetrain.drive_for(FORWARD, 3.7)
    pneumatic_on()
    drivetrain.turn_for(LEFT, 90, DEGREES, wait=False)
    wait(1, SECONDS)
    #drivetrain.turn_to_rotation(-90)
    drivetrain.set_turn_velocity(30, PERCENT)
    drivetrain.turn_to_rotation(12)
    pneumatic_off()
    

    # Get pre-load in goal
    # drivetrain.turn_to_rotation(15)
    drivetrain.drive_for(FORWARD, 18.5)
    drivetrain.turn_to_rotation(-85)
    Intake.spin(REVERSE)

    drivetrain.set_drive_velocity(100, PERCENT)
    brain.timer.reset()
    while(brain.timer.time(SECONDS) < 1.5):
        drivetrain.drive(FORWARD)
    drivetrain.stop()
    Intake.stop()
    

    # Go to elevation bar
    # drivetrain.set_drive_velocity(60, PERCENT)
    # drivetrain.drive_for(REVERSE, 6)
    # drivetrain.turn_to_rotation(90)
    drivetrain.drive_for(REVERSE, 4)
    endgame_off()
    # drivetrain.drive_for(FORWARD, 4)
    drivetrain.turn_to_rotation(10)
    brain.timer.reset()
    while(brain.timer.time(SECONDS) < 2):
        drivetrain.drive(REVERSE)
    drivetrain.stop()
    drivetrain.drive_for(FORWARD, 2)
    drivetrain.turn_to_rotation(100)
    drivetrain.drive_for(FORWARD, 15)

    ########################################
    # #pneumatic_off()
    # # Get pre-load under other alliance's goal
    # drivetrain.set_drive_velocity(20, PERCENT)
    # drivetrain.set_turn_velocity(10, PERCENT)
    # drivetrain.drive_for(FORWARD, 5)
    # drivetrain.turn_to_heading(-35, DEGREES)
    # drivetrain.set_drive_velocity(100, PERCENT)
    # brain.timer.reset()
    # while(brain.timer.time(SECONDS) < 3):
    #     drivetrain.drive(FORWARD)
    # drivetrain.stop()

    # drivetrain.set_drive_velocity(25, PERCENT)
    # drivetrain.set_turn_velocity(30, PERCENT)

    # # Remove match-load
    # drivetrain.drive_for(REVERSE, 4)
    # drivetrain.turn_to_rotation(0)
    # drivetrain.drive_for(REVERSE, 4)
    # drivetrain.turn_to_rotation(-42)
    # digital_out_b.set(True)
    # #drivetrain.set_drive_velocity(80, PERCENT)
    # drivetrain.drive_for(REVERSE, 6)
    # drivetrain.set_turn_velocity(100, PERCENT)
    # drivetrain.turn_for(LEFT, 90, DEGREES)
    # wait(1, SECONDS)
    # drivetrain.turn_to_rotation(90)
    # digital_out_b.set(False)

    # # Touch colored bar
    # drivetrain.set_turn_velocity(40, PERCENT)
    # drivetrain.drive_for(FORWARD, 14)

# ######################################
#   Starting Position 2 (goal side)    #
# ######################################
# Get pre-load and one of the field triballs into goal
# Go get other field triball and get into goal
# Stretch: get third field triball
# 1/3 Autonomous Win Point, 15 points
def autonomous_same():
    inertia.reset_heading()
    inertia.reset_rotation()
    wait(1, SECONDS)

    endgame_on()
    # Slow speed for greater precision
    drivetrain.set_drive_velocity(50, PERCENT)
    drivetrain.set_turn_velocity(20, PERCENT)

    # Get pre-load and one field triball in
    drivetrain.drive_for(FORWARD, 4)
    drivetrain.turn_to_rotation(-20)
    drivetrain.drive_for(FORWARD, 20)
    #digital_out_a.set(True)
    #drivetrain.set_turn_velocity(10, PERCENT)
    drivetrain.turn_to_rotation(80)
    #drivetrain.set_turn_velocity(20, PERCENT)
    Intake.spin(REVERSE)
    brain.timer.reset()
    drivetrain.set_drive_velocity(100, PERCENT)
    while(brain.timer.time(SECONDS) < 2):
        drivetrain.drive(FORWARD)
    drivetrain.stop()
    Intake.stop()
    drivetrain.set_drive_velocity(50, PERCENT)
    drivetrain.drive_for(REVERSE, 6)
    drivetrain.turn_to_rotation(-90)
    endgame_off()
    brain.timer.reset()
    while(brain.timer.time(SECONDS) < 2):
        drivetrain.drive(REVERSE)
    drivetrain.stop()
    drivetrain.drive_for(FORWARD, 4)
    
    #digital_out_a.set(False)
    #drivetrain.set_turn_velocity(30, PERCENT)

    # # Get other field triball
    # drivetrain.drive_for(REVERSE, 6)
    # drivetrain.turn_to_rotation(-100)
    # Intake.spin(FORWARD)
    # brain.timer.reset()
    # while(brain.timer.time(SECONDS) < 2):
    #     drivetrain.drive(FORWARD)
    # drivetrain.stop()

    # # Get in goal
    # drivetrain.drive_for(REVERSE, 6)
    # drivetrain.turn_to_rotation(70)
    # Intake.spin(REVERSE)
    # drivetrain.set_drive_velocity(100, PERCENT)
    # brain.timer.reset()
    # while(brain.timer.time(SECONDS) < 2):
    #     drivetrain.drive(FORWARD)
    # drivetrain.stop()
    # #drivetrain.set_drive_velocity(50, PERCENT)
    # Intake.stop()
    # drivetrain.drive_for(REVERSE, 6)
    # drivetrain.turn_to_rotation(-90)
    # drivetrain.drive_for(REVERSE, 6)
    # drivetrain.drive_for(FORWARD, 4)

    ############################################
    # # Push pre-load into the goal
    # drivetrain.drive_for(FORWARD, 5.5)
    # drivetrain.turn_to_rotation(38, DEGREES)
    # drivetrain.set_drive_velocity(100, PERCENT)

    # # # Drive to and touch elevation bar
    # brain.timer.reset()
    # while(brain.timer.time(SECONDS) < 3):
    #     Intake.spin(REVERSE)
    #     drivetrain.drive(FORWARD)
    # drivetrain.stop()
    # Intake.stop()
    # drivetrain.set_drive_velocity(50, PERCENT)
    # drivetrain.drive_for(REVERSE, 6)
    # drivetrain.turn_to_rotation(-90, DEGREES)
    # drivetrain.set_drive_velocity(100, PERCENT)
    # brain.timer.reset()
    # while(brain.timer.time(SECONDS) < 1):
    #     drivetrain.drive(REVERSE)
    # drivetrain.stop()
    # drivetrain.set_drive_velocity(50, PERCENT)
    # drivetrain.drive_for(FORWARD, 6)

    # drivetrain.turn_to_rotation(-80, DEGREES)
    # Intake.spin(FORWARD)
    # brain.timer.reset()
    # while(brain.timer.time(SECONDS) < 4):
    #     drivetrain.drive(FORWARD)
    # drivetrain.stop()

    # drivetrain.drive_for(REVERSE, 5)
    # drivetrain.turn_to_rotation(0, DEGREES)
    # pneumatic_on()
    # drivetrain.drive_for(FORWARD, 5)
    # drivetrain.set_turn_velocity(20, PERCENT)
    # drivetrain.turn_to_rotation(80, DEGREES)

    # drivetrain.set_drive_velocity(100, PERCENT)
    # brain.timer.reset()
    # while(brain.timer.time(SECONDS) < 3):
    #     Intake.spin(REVERSE)
    #     drivetrain.drive(FORWARD)
    # drivetrain.stop()
    # Intake.stop()
    # drivetrain.drive_for(REVERSE, 4, INCHES)

# ######################################
#          Skills Autonomous          #
# ######################################
# Launch 46 triballs
# Drive to goal on other side of field
# Push triballs in
def autonomous_skills():
    inertia.reset_heading()
    inertia.reset_rotation()
    wait(1, SECONDS)

    drivetrain.set_drive_velocity(40, PERCENT)
    drivetrain.set_turn_velocity(30, PERCENT)
    Cata.set_velocity(100, PERCENT)

    # Get into position for match loads
    drivetrain.drive_for(FORWARD, 10.75, INCHES)
    drivetrain.turn_to_rotation(75, DEGREES)
    drivetrain.drive_for(REVERSE, 11, INCHES, wait=False)

    # Change to 40 seconds
    Cata.spin_for(REVERSE, 40, SECONDS)

    # # Drive to other side of the field
    drivetrain.turn_to_rotation(90, DEGREES) # Straighten out

    drivetrain.drive_for(FORWARD, 8.5, INCHES)
    drivetrain.turn_to_rotation(180, DEGREES) # Turn to wall

    drivetrain.drive_for(FORWARD, 7, INCHES) # Drive towards wall
    drivetrain.turn_to_rotation(90, DEGREES)
    drivetrain.set_drive_velocity(90, PERCENT)
    drivetrain.drive_for(FORWARD, 35, INCHES) # Drive to the other side

    drivetrain.turn_to_rotation(14, DEGREES) 
    drivetrain.drive_for(FORWARD, 7, INCHES) # Drive away from bar, towards wall

    drivetrain.turn_to_rotation(-50, DEGREES)
    drivetrain.drive_for(FORWARD, 18, INCHES) # Drive towards middle bar

    drivetrain.turn_to_rotation(0, DEGREES)
    drivetrain.drive_for(FORWARD, 4, INCHES) # Drive towards middle of goal

    drivetrain.turn_to_rotation(80, DEGREES)
    pneumatic_on()
    brain.timer.reset()
    while(brain.timer.time(SECONDS) < 3):
        drivetrain.drive(FORWARD) # Push triballs in
    drivetrain.stop()
    pneumatic_off()
    drivetrain.drive_for(REVERSE, 12, INCHES)

    drivetrain.turn_to_rotation(-10, DEGREES)
    drivetrain.drive_for(FORWARD, 8, INCHES) # Line up to do it again

    drivetrain.turn_to_rotation(90, DEGREES) # Push triballs in
    pneumatic_on()
    brain.timer.reset()
    while(brain.timer.time(SECONDS) < 4):
        drivetrain.drive(FORWARD)
    drivetrain.stop()
    pneumatic_off()

    drivetrain.drive_for(REVERSE, 8, INCHES) # Reverse to prevent possession issues


# ######################################
#          Autonomous Selector         #
# ######################################
# Select which auton to run from screen input
def autonomous_fsm():
    global which_auton
    brain.screen.print("Running auton")
    if which_auton == 2 or which_auton == 3:
        autonomous_same()
    elif which_auton == 1 or which_auton == 4:
        autonomous_opp()
    elif which_auton == 5:
        autonomous_skills()

# ######################################
#          Autonomous Selector         #
# ######################################
# Run auton
def autonomous():
    # Start the autonomous control tasks
    auton_task_0 = Thread(autonomous_fsm)
    # wait for the driver control period to end
    while(competition.is_autonomous() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait(10, MSEC)
    # Stop the autonomous control tasks
    auton_task_0.stop()

def pneumatic_on():
    digital_out_a.set(True)
    digital_out_b.set(True)

def pneumatic_off():
    digital_out_a.set(False)
    digital_out_b.set(False)

def endgame_on():
    digital_out_c.set(True)
    digital_out_d.set(True)

def endgame_off():
    digital_out_c.set(False)
    digital_out_d.set(False)

def control_pneumatics():
    global pneumatics_on
    if pneumatics_on:
        pneumatics_on = False
        pneumatic_off()
    else:
        pneumatics_on = True
        pneumatic_on()

def skills_starting_position():
    inertia.reset_heading()
    inertia.reset_rotation()
    wait(1, SECONDS)

    drivetrain.set_drive_velocity(40, PERCENT)
    drivetrain.set_turn_velocity(30, PERCENT)
    Cata.set_velocity(100, PERCENT)

    # Get into position for match loads
    drivetrain.drive_for(FORWARD, 11.25, INCHES)
    drivetrain.turn_to_rotation(75, DEGREES)
    drivetrain.drive_for(REVERSE, 12, INCHES, wait=False)

    # Launch 44 triballs (42 seconds)
    Cata.spin(REVERSE)


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

# ######################################
#               Setup                  #
# ######################################
def when_started():
    # drivetrain.set_drive_velocity(100, PERCENT)
    # drivetrain.set_turn_velocity(100, PERCENT)
    startup_brain()

# ######################################
#           User Control               #
# ######################################
def on_user_control():
    global remote_control_code_enabled, rc_auto_loop_thread_controller_1
    brain.timer.clear()
    brain.screen.print("Running user")
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(80, PERCENT)
    Cata.set_velocity(100, PERCENT)
    # define variable for remote controller enable/disable
    remote_control_code_enabled = True

    rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
    #Climber.spin_for(FORWARD, 4000)
    pass

def user_control():
    # Start the driver control tasks
    driver_control_task_0 = Thread(on_user_control)

    # wait for the driver control period to end
    while(competition.is_driver_control() and competition.is_enabled()):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the driver control tasks
    driver_control_task_0.stop()


#pneumatic_off()
competition = Competition(user_control, autonomous)
when_started()
