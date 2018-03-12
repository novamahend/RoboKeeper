from serial import Serial

class StepperMotor():
    """Stepper Motor with Serial"""
    
    def __init__(self, serial_port, baud_rate):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.serial = None
        self.connected = False
        
    def connect(self):
        try:
            self.serial = Serial(serial_port,self.baud_rate)
        except:
            print("Failed connect to serial port",self.serial_port)
        self.connected = True
		
    def disconnect(self):
        try:
            if(self.connected):
                self.serial.close()
        except:
            print("Failed disconnect to serial port",self.serial_port)
        self.connected = False
        
    def move(self,angle):
        if(self.serial is None or not self.connected):
            print("Device is not connected")
            return
        angle = int(angle)
        data = str(angle)+'\r\n'
        self.serial.write(data.encode)