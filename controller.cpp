# define variables used for controlling motors based on controller inputs
controller_1_right_shoulder_control_motors_stopped = True
controller_1_left_shoulder_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False
program = 0


# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
   global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled, controller_1_left_shoulder_control_motors_stopped
   # process the controller input every 20 milliseconds
   # update the motors based on the input values
   while True:
       if remote_control_code_enabled:
          
           # calculate the drivetrain motor velocities from the controller joystick axies
           drivetrain_left_side_speed = controller_1.axis3.position() - controller_1.axis1.position()
           drivetrain_right_side_speed = controller_1.axis3.position() + controller_1.axis1.position()
          
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
           # check the buttonR1/buttonR2 status
           # to control Cata
           if controller_1.buttonR1.pressing():
               Cata.spin(FORWARD)
               controller_1_right_shoulder_control_motors_stopped = False
           elif controller_1.buttonR2.pressing():
               Cata.spin(REVERSE)
               controller_1_right_shoulder_control_motors_stopped = False
           elif not controller_1_right_shoulder_control_motors_stopped:
               Cata.stop()
               # set the toggle so that we don't constantly tell the motor to stop when
               # the buttons are released
               controller_1_right_shoulder_control_motors_stopped = True
          
           # to control Climber
           if controller_1.buttonL1.pressing():
               Climber.spin(FORWARD)
               controller_1_left_shoulder_control_motors_stopped = False
           elif controller_1.buttonL2.pressing():
               Climber.spin(REVERSE)
               controller_1_left_shoulder_control_motors_stopped = False
           elif not controller_1_left_shoulder_control_motors_stopped:
               Climber.stop()
               # set the toggle so that we don't constantly tell the motor to stop when
               # the buttons are released
               controller_1_left_shoulder_control_motors_stopped = True
       # wait before repeating the process
       wait(20, MSEC)


# define variable for remote controller enable/disable
remote_control_code_enabled = True


rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)


def pneumatic_on():
   digital_out_a.set(True)
   digital_out_b.set(True)


def pneumatic_off():
   digital_out_a.set(False)
   digital_out_b.set(False)


# Set pneumatic buttons
controller_1.buttonUp.pressed(pneumatic_on)
controller_1.buttonDown.pressed(pneumatic_off)
