from mbuild.encoder_motor import encoder_motor_class
from mbuild.smartservo import smartservo_class
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild import power_expand_board
from mbuild import gamepad
import novapi
import time

# initialize the variables
auto_stage = 0
shoot = 0
invert = 0
feeddc = 1
lrmode = 0  # Differentiate between shoot and arm control mode
bp = 50
vl = 0.5

# DC motors
feeddc_main = "DC1"
feeddc_front = "DC2"
feeddc_aux = "DC3"
dc4_variable = "DC4"
dc5_variable = "DC5"
handdc1 = "DC6"
handdc2 = "DC7"

# Sensors
dual_rgb_sensor_1 = dual_rgb_sensor_class("PORT2", "INDEX1")
dual_rgb_sensor_2 = dual_rgb_sensor_class("PORT2", "INDEX2")

# Arm
smartservo_arm = smartservo_class("M6", "INDEX1")

# Turret
smartservo_pitch =   smartservo_class("M5", "INDEX1")
smartservo_updown = smartservo_class("M5", "INDEX2")

# Bot motors
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")
# Auto motors
motor1 = encoder_motor_class("M1", "INDEX1")
motor2 = encoder_motor_class("M2", "INDEX1")
motor3 = encoder_motor_class("M3", "INDEX1")
motor4 = encoder_motor_class("M4", "INDEX1")


def AutoStart():
    global auto_stage
    dual_rgb_sensor_1.set_led_color("blue")
    while not gamepad.is_key_pressed("L1"):
        if gamepad.is_key_pressed("L2"):
            for i in range(3):
                dual_rgb_sensor_1.set_led_color("red")
                time.sleep(0.2)
                dual_rgb_sensor_1.set_led_color("blue")
                time.sleep(0.2)
            Manual()
        pass
        
    AutoAssets.ShootRoutine()
    time.sleep(5)
    pass

def Manual():
    global auto_stage
    global invert
    global lrmode
    global feeddc
    global bp
    global vl
    LoadMe()
    while True:
        time.sleep(0.001)
        JoyRes.MovingJoystick(invert,vl)
        ManualRes.InvertLED(invert)
        ManualRes.ControlLED(lrmode)
        JoyRes.MultiControl(lrmode, bp)

        if gamepad.is_key_pressed("Up"):
            #ManualRes.MoveForward()
            smartservo_pitch.move(10,10)

        if gamepad.is_key_pressed("Down"):
            #ManualRes.MoveBackward()
            smartservo_pitch.move(-10,10)

        if gamepad.is_key_pressed("Left"):
            ManualRes.MoveLeft()

        if gamepad.is_key_pressed("Right"):
            ManualRes.MoveRight()

        if gamepad.is_key_pressed("N1"):
            pass
        if gamepad.is_key_pressed("N4"):
            pass


        if gamepad.is_key_pressed("N2"):
            if bp == 50:
                bp = 100
            elif bp == 100:
                bp = 0
            else:
                bp = 50
            while not not gamepad.is_key_pressed("N2"):
                pass
            pass

        if gamepad.is_key_pressed("N3"):
            if feeddc == 0:
                feeddc = 1
            else:
                feeddc = 0
            while not not gamepad.is_key_pressed("N3"):
                pass
            pass

        # Switch shooting to arm control
        if gamepad.is_key_pressed("R2"):
            if lrmode == 0:
                lrmode = 1
            else:
                lrmode = 0
            while not not gamepad.is_key_pressed("R2"):
                pass
        
        # Control speed
        if gamepad.is_key_pressed("L_Thumb"):
            if vl == 0.5:
                vl = 0.8
            elif vl == 0.8:
                vl = 1
            else:
                vl = 0.5

            while not not gamepad.is_key_pressed("L_Thumb"):
                pass
        
        # Invert control direction
        if gamepad.is_key_pressed("R_Thumb"):
            if invert == 0:
                invert = 1
            else:
                invert = 0
            while not not gamepad.is_key_pressed("R_Thumb"):
                pass

        # Dc feed
        if feeddc == 1:
            power_expand_board.set_power(feeddc_front, 100)
        else:
            power_expand_board.stop(feeddc_front)


def LoadMe():
    global auto_stage

    smartservo_arm.set_power(50)
    smartservo_arm.move(30, 10)


class JoyRes:
    def __init__(self):
        pass

    def MovingJoystick(invert,v):
        global auto_stage
        global vl
        Lx = gamepad.get_joystick("Lx")  # literally Lx variable
        Fl = 0   # Front left
        Fr = 0   # Front right
        Rl = 0   # Rear left
        Rr = 0   # Rear right

        
        Fl = Lx
        Fr = Lx
        Rl = Lx
        Rr = Lx

        EFl = vl * (gamepad.get_joystick("Ly") - Rl
                    - gamepad.get_joystick("Rx"))
        EFr = -vl * (gamepad.get_joystick("Ly") + Rr
                     + gamepad.get_joystick("Rx"))
        ERl = vl * (gamepad.get_joystick("Ly")
                    + Fl - gamepad.get_joystick("Rx"))
        ERr = -vl * (gamepad.get_joystick("Ly") - Fr
                     + gamepad.get_joystick("Rx"))

        if invert == 1:
            # If the controls are inverted The arms are now the bot's front
            EFr = vl * (gamepad.get_joystick("Ly")
                        - Fl - gamepad.get_joystick("Rx"))
            EFl = -vl * (gamepad.get_joystick("Ly") + Fr
                         + gamepad.get_joystick("Rx"))
            ERr = vl * (gamepad.get_joystick("Ly") + Rl
                        - gamepad.get_joystick("Rx"))
            ERl = -vl * (gamepad.get_joystick("Ly") - Rr
                         + gamepad.get_joystick("Rx"))
        encoder_motor_M1.set_power(EFl)
        encoder_motor_M2.set_power(EFr)
        encoder_motor_M3.set_power(ERl)
        encoder_motor_M4.set_power(ERr)

    def TurretControl():
        global auto_stage
        # > 40 < 60
        # if smartservo_updown.get_value("angle") > -43:
        #    smartservo_updown.move(-1, 10)

        # if smartservo_updown.get_value("angle") < -60:
        #    smartservo_updown.move(1, 10)
        # else:
        if smartservo_updown.get_value("angle") < -56:
            servo_value = smartservo_updown.get_value("angle")
            while servo_value < -55:
                smartservo_updown.move(3, 10)
                servo_value = smartservo_updown.get_value("angle")

        relative_angle = gamepad.get_joystick("Ry") / 3

        smartservo_updown.move(relative_angle, 10)

    def FeedControl():
        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power(feeddc_main, -100)
            power_expand_board.set_power(feeddc_aux, 75)
        elif gamepad.is_key_pressed("L2"):
            power_expand_board.set_power(feeddc_main, 100)
            power_expand_board.set_power(feeddc_aux, -75)
        else:
            power_expand_board.stop("DC1")

    def ShootControl():
        if gamepad.is_key_pressed("R1"):
            pass
        else:
            pass

    def GrabControl():
        # DC4 L1 release R1 grab
        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power("DC4", 50)

        elif gamepad.is_key_pressed("R1"):
            power_expand_board.set_power("DC4", -50)
        else:
            power_expand_board.stop("DC4")
        pass

    def HandControl():
        power_expand_board.set_power(handdc1, - (gamepad.get_joystick("Ry")))
        power_expand_board.set_power(handdc2, - (gamepad.get_joystick("Ry")))
        # smartservo_arm.move(gamepad.get_joystick("Ry"), 10)
        pass

    def MultiControl(lc, bp):
        if lc == 0:
            # Gun control mode
            JoyRes.TurretControl()
            JoyRes.ShootControl()
            JoyRes.FeedControl()

            # < 15 -- 23 > : 25 max
            power_expand_board.set_power("BL1", bp)
            power_expand_board.set_power("BL2", bp)
        else:
            # Hand control mode
            JoyRes.HandControl()
            JoyRes.GrabControl()
            power_expand_board.stop("BL1")
            power_expand_board.stop("BL2")


class ManualRes:
    def __init__(self):
        pass

    # Miscellaneous
    def InvertLED(i):
        if i != 0:
            dual_rgb_sensor_1.set_led_color("red")
        else:
            dual_rgb_sensor_1.set_led_color("green")

    def ControlLED(k):
        if k != 0:
            dual_rgb_sensor_2.set_led_color("red")
        else:
            dual_rgb_sensor_2.set_led_color("green")
    
    # Joystick Controls
    def MoveBackward():
        global auto_stage
        encoder_motor_M1.set_power(-50)
        encoder_motor_M2.set_power(50)
        encoder_motor_M3.set_power(-50)
        encoder_motor_M4.set_power(50)

    def MoveForward():
        global auto_stage
        encoder_motor_M1.set_power(50)
        encoder_motor_M2.set_power(-50)
        encoder_motor_M3.set_power(50)
        encoder_motor_M4.set_power(-50)

    def MoveRight():
        global auto_stage
        encoder_motor_M1.set_power(50)
        encoder_motor_M2.set_power(50)
        encoder_motor_M3.set_power(-50)
        encoder_motor_M4.set_power(-50)

    def MoveLeft():
        global auto_stage
        encoder_motor_M1.set_power(-50)
        encoder_motor_M2.set_power(-50)
        encoder_motor_M3.set_power(50)
        encoder_motor_M4.set_power(50)

    def StopMoving():
        global auto_stage
        encoder_motor_M1.set_power(0)
        encoder_motor_M2.set_power(0)
        encoder_motor_M3.set_power(0)
        encoder_motor_M4.set_power(0)


class MovementAsset:
    def __init__(self):
        pass

    def move(v1, v2, v3, v4):
        motor1.set_power(v1)
        motor2.set_power(v2)
        motor3.set_power(v3)
        motor4.set_power(v4)

    def stop():
        motor1.set_power(0)
        motor2.set_power(0)
        motor3.set_power(0)
        motor4.set_power(0)


class AutoAssets:
    def __init__(self):
        pass

    def MoveForward():
        MovementAsset.move(25, -25, 25, -25)
        pass

    def MoveBackward():
        MovementAsset.move(-25, 25, -25, 25)
        pass

    def RotateLeft():
        MovementAsset.move(-50, -50, -50, -50)
        pass

    def RotateRight():
        MovementAsset.move(50, 50, 50, 50)
        pass
    def StopMoving():
        MovementAsset.move(0, 0, 0, 0)
    def Shoot():
        power_expand_board.set_power("DC3", 100)
        pass

    # Return value functions

    def getSelfAngle():

        angle = [novapi.get_pitch(), novapi.get_roll(), novapi.get_yaw()]
        return angle


    def GetDistance():
        # GetDistance utilizes a ranging sensor Module
        # What it does is detects an object in front of it
        # And returns a distance value as number

        range = distance_sensor_1.get_distance()

        return range

    # Presets

    def ShootRoutine():
        dual_rgb_sensor_1.set_led_color("red")
        dual_rgb_sensor_2.set_led_color("red")
        time.sleep(1)    

        power_expand_board.set_power("DC2",70)
        power_expand_board.set_power("DC1",-100)
        
        AutoAssets.MoveForward()
        time.sleep(0.5)
        AutoAssets.RotateLeft()
        time.sleep(0.25)

        AutoAssets.MoveForward()
        time.sleep(2)
        AutoAssets.RotateRight()
        time.sleep(0.2)
        
        AutoAssets.MoveForward()
        power_expand_board.set_power("BL1",100)
        power_expand_board.set_power("BL2",100)
        time.sleep(1.25)

        AutoAssets.StopMoving()
        dual_rgb_sensor_2.set_led_color("green")

        time.sleep(10)
        for i in range(10):
            dual_rgb_sensor_1.set_led_color("blue")
            AutoAssets.RotateLeft()
            time.sleep(0.1)
            AutoAssets.StopMoving()
            dual_rgb_sensor_1.set_led_color("red")
            time.sleep(0.2)

        pass

    def EmbraceBallRoutine():

        pass

    def GrabCubeRoutine():

        pass

auto_stage = 1
while True:
    time.sleep(0.001)
    if auto_stage == 1:
        AutoStart()
        auto_stage = 0

    else:
        smartservo_arm.move_to(0, 10)
        Manual()