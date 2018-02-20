import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.count = 0

    def on_circle_draw(self, color, x, y):
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, width=3)

    def on_square_draw(self, color, x, y, distance):
        self.canvas.create_square(x - (distance/2),
                                  y - (distance/2),
                                  x + (distance/2),
                                  y + (distance/2),
                                  fill=,
                             width=3)



def main():
    root = tkinter.Tk()
    root.title = "MappingRobot"

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    label = ttk.Label(main_frame, text='Robo-Map')
    label.grid(columnspan=7)

    canvas = tkinter.Canvas(main_frame, background="white",width=800,
                            height=400)
    canvas.grid(columnspan=7)

    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()
    mqtt_client.connect("draw", "draw")

    canvas.bind("<Button-1>",
                lambda event: left_mouse_click(event, mqtt_client))

    clear_button = ttk.Button(main_frame, text="Clear")
    clear_button.grid(row=6, column=4)
    clear_button["command"] = lambda: clear(canvas)

    robit = com.MqttClient(my_delegate)
    robit.connect_to_ev3()

    grid_size_label = ttk.Label(main_frame, text="Grid Size")
    grid_size_label.grid(row=4, column=4)
    grid_size_entry = ttk.Entry(main_frame, width=8)
    grid_size_entry.insert(0, "600")
    grid_size_entry.grid(row=5, column=4)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=5, column=1)
    forward_button['command'] = lambda: send_forward(robit, grid_size_entry)
    root.bind('<Up>', lambda event: send_forward(robit, grid_size_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=6, column=0)
    left_button['command'] = lambda: send_left(robit)
    root.bind('<Left>', lambda event: send_left(robit))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=6, column=2)
    right_button['command'] = lambda: send_right(robit)
    right_button['command'] = lambda: send_right(robit)
    root.bind('<Right>',
              lambda event: send_right(robit))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=8, column=1)
    q_button['command'] = (lambda: quit_program(robit, False))

    root.mainloop()


def clear(canvas):
    canvas.delete("all")


def send_forward(mqtt_client, grid_size):
    print("robit_forward")
    mqtt_client.send_message("hop", [int(grid_size.get())])


def send_left(mqtt_client):
    print("robit_left")
    mqtt_client.send_message("rotate_left")


def send_right(mqtt_client):
    print("robit_right")
    mqtt_client.send_message("rotate_right")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def left_mouse_click(event, mqtt_client):
    mqtt_client.send_message('on_circle_draw', ['red', event.x,
                                                event.y])


main()
