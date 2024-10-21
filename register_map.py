import enum

GPIO_BASE_ID = 0x01300000

class GPIOReg(enum.IntEnum):
    NOP = 0x0
    PORT_MODE = 0x1
    PORT_READ = 0x2
    PORT_WRITE = 0x3
    PORT_INT_EN = 0x4
    ESC_MODE_EN = 0x5
    PWM_PERIOD = 0x10
    PWM_DUTY = 0x20
    MONITOR_PERIOD = 0xF0
    MONITOR_REG = 0xF1

class LMMDCommand(enum.IntEnum):
    SET_ORIGIN = 0x0
    TARGET_POS = 0x1
    POWER = 0x2
    GAIN_P = 0x3
    GAIN_I = 0x4
    GAIN_D = 0x5