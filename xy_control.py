import tkinter
import threading
import can
import command_if

def print_port_input():
    recv_msg = canIF.bus.recv()
    if recv_msg != None:
        print(recv_msg)

    t=threading.Timer(0.1,print_port_input)
    t.start()

class XYPaint:
    def __init__(self,port,x_max = 100.0,y_max = 100.0):
        self.port = port
        self.x_max = x_max
        self.y_max = y_max

        self.port.servo_init(0.15)
        self.port.set_power(0.15,0.15)
        
        self.is_writing = False

        # 操作中の図形のID
        self.curr_id = -1
        
        # メインウィンドウ作成
        root = tkinter.Tk()
        root.title("無題")

        self.cursor_position_label = tkinter.Label(root, text="マウスカーソルの座標を表示します")
        self.cursor_position_label.pack()
        root.bind("<Motion>", self.update_cursor_position)

        # 画像表示用キャンバス作成
        self.canvas = tkinter.Canvas(root, bg="white",width=500,height=500)
        self.canvas.pack(expand=True, fill=tkinter.BOTH)
        # キーバインド
        self.canvas.bind("<ButtonPress-1>", self.on_key_left)
        self.canvas.bind("<ButtonRelease-1>", self.off_key_left)
        self.canvas.bind("<B1-Motion>", self.dragging)
        root.bind("<Delete>", self.clear_canvas)

        root.mainloop()

    # マウス左ボタン押下
    def on_key_left(self, event):
        # 直線描画
        self.curr_id = self.canvas.create_line(event.x, event.y, event.x, event.y,
            fill = "black",width = 1)
        self.is_writing = True
        self.port.move_servo(0.15)
    
    # マウス左ボタン解放
    def off_key_left(self, event):
        self.is_writing = False
        self.port.move_servo(0)
 
   # ドラッグ中
    def dragging(self, event):
        points = self.canvas.coords(self.curr_id)
        points.extend([event.x,event.y])
        self.canvas.coords(self.curr_id, points)

    def update_cursor_position(self,event):
        x = event.x/500.0*100.0 + 10.0
        y = event.y/500.0*100.0 + 10.0
        self.cursor_position_label.config(text=f"X: {format(x, ".1f")}, Y: {format(y, ".1f")}")

        self.port.move_xy(x,y)
        if self.is_writing:
            self.port.move_servo(0.15)
        else:
            self.port.move_servo(0)

    def clear_canvas(self, event):
        self.canvas.delete("all")


if __name__ == '__main__':
    with can.interface.Bus('COM14@115200',bustype='slcan',bitrate=1000000) as bus:
        canIF = command_if.CommandIF(bus)

        t=threading.Thread(target=print_port_input)
        t.start()

        XYPaint(canIF)