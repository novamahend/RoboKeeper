from StepperMotor import *
from Tracker import *
from threading import Thread

cam = Camera(0)
inputs = Input()
tracker = Tracker()
motor = StepperMotor("COM3",115200)
display = Display("Display",640,480)

#Global Variable
is_running = False
is_ready_to_move = False
is_move_done = False
ball_distance = 0
ball_degree = 0

def get_input():
    global is_running

    is_running = True
    
    while(is_running):
        inputs.update_value()
        value = inputs.get_value()
        time.sleep(0.1)
        #print(value)

def tracking():
    global is_running, ball_distance, ball_degree

    is_running = True
    
    cam.connect()
    i = 0
    while(is_running):
        start = time.time()

        ret, frame = cam.get_frame()
        if ret is False:
            print("No frame")
            continue

        frame = tracker.threshold(frame)
        frame, ball_distance, ball_degree = tracker.track(frame)
        display.show(frame)
        
        end = time.time()
        print(i,(end-start)*1000)
        i = i +1
    cam.disconnect()

def move_motor():
    global is_running,is_ready_to_move, is_move_done, ball_distance, ball_degree

    is_running = True
    
    motor.connect()
    
    while(is_running):
        if(is_ready_to_move and not is_move_done):
            motor.move(ball_degree)
        #print(ball_distance,ball_degree)
        
get_input_thread = Thread(target = get_input)
tracking_thread = Thread(target = tracking)
move_motor_thread = Thread(target = move_motor)

inputs.create_trackbar()

get_input_thread.start()
tracking_thread.start()
move_motor_thread.start()

while(True):
    key = cv2.waitKey(1) & 0xFF
    if key is 27:
        is_running = False
        break
    
if(is_running is True):
    is_running = False
cv2.destroyAllWindows()

