import data_converter as dc
import register_map as rm
import can

class CommandIF:
   
    def __init__(self,bus):
        self.bus = bus

    def send_params(self,id,x,y):
        data = dc.float_to_int_list(x) + dc.float_to_int_list(y)
        msg = can.Message(arbitration_id = id,data = data)
        self.bus.send(msg)

    def move_xy(self,x,y):
        self.send_params(rm.LMMDReg.POS,x,y)

    def set_power(self,x_power,y_power):
        self.send_params(rm.LMMDReg.POWER,x_power,y_power)

    def set_p_gain(self,x_p,y_p):
        self.send_params(rm.LMMDReg.GAIN_P,x_p,y_p)
    
    def set_i_gain(self,x_i,y_i):
        self.send_params(rm.LMMDReg.GAIN_I,x_i,y_i)
    
    def set_d_gain(self,x_d,y_d):
        self.send_params(rm.LMMDReg.GAIN_D,x_d,y_d)

    def servo_init(self,pos):
        msg = can.Message(arbitration_id = rm.GPIO_BASE_ID | rm.GPIOReg.PORT_MODE,is_extended_id=True,data=dc.int_to_int_list(int_value = 0b0,dlc = 2))
        self.bus.send(msg)

        msg = can.Message(arbitration_id = rm.GPIO_BASE_ID | rm.GPIOReg.PORT_WRITE,is_extended_id=True,data=dc.int_to_int_list(int_value = 0b1,dlc = 2))
        self.bus.send(msg)

        msg = can.Message(arbitration_id = rm.GPIO_BASE_ID | rm.GPIOReg.PWM_PERIOD,is_extended_id=True,data=dc.int_to_int_list(int_value = 1000,dlc = 2))
        self.bus.send(msg)

        self.move_servo(pos)

    def move_servo(self,pos):
        #pulse width = 0.5~2.4ms(2.5%~12%) 
        pulse_width = int((pos*1.9) / 0.02  + 25)
        msg = can.Message(arbitration_id = rm.GPIO_BASE_ID | rm.GPIOReg.PWM_DUTY,is_extended_id=True,data=dc.int_to_int_list(int_value = pulse_width,dlc = 2))
        self.bus.send(msg)