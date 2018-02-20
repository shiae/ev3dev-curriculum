import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.count = 0

    def on_circle_draw(self, color, x, y):
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, width=3)


def main():
    root = tkinter.Tk()
    root.title = "MappingRobot"

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    label = ttk.Label(main_frame, text='Robo-Map')
    label.grid(columnspan=3)

    canvas = tkinter.Canvas(main_frame, background="white",width=800,
                            height=400)
    canvas.grid(columnspan=3)

    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()
    mqtt_client.connect("draw", "draw")

    canvas.bind("<Button-1>",
                lambda event: left_mouse_click(event, mqtt_client))

    clear_button = ttk.Button(main_frame, text="Clear")
    clear_button.grid(row=3, column=1)
    clear_button["command"] = lambda: clear(canvas)

    robit = com.MqttClient()
    robit.connect_to_ev3()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=3, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=4, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=3, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=4, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=5, column=1)
    forward_button['command'] = lambda: send_forward(robit,
                                                     left_speed_entry,
                                                     right_speed_entry)
    root.bind('<Up>', lambda event: send_forward(robit, left_speed_entry,
                                                 right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=6, column=0)
    left_button['command'] = lambda: send_left(robit, left_speed_entry,
                                               right_speed_entry)
    root.bind('<Left>', lambda event: send_left(robit, left_speed_entry,
                                                right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=6, column=1)
    stop_button['command'] = lambda: send_stop(robit)
    root.bind('<space>', lambda event: send_stop(robit))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=6, column=2)
    right_button['command'] = lambda: send_right(robit, left_speed_entry,
                                                 right_speed_entry)
    root.bind('<Right>',
              lambda event: send_right(robit, left_speed_entry,
                                       right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=7, column=1)
    back_button['command'] = lambda: send_backward(robit,
                                                   left_speed_entry,
                                                   right_speed_entry)
    root.bind('<Down>',
              lambda event: send_backward(robit, left_speed_entry,
                                          right_speed_entry))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=8, column=1)
    q_button['command'] = (lambda: quit_program(robit, False))

    root.mainloop()


def clear(canvas):
    canvas.delete("all")


def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print("robit_forward")
    mqtt_client.send_message("drive", [int(left_speed_entry.get()),
                                       int(right_speed_entry.get())])


def send_backward(mqtt_client, left_speed_entry, right_speed_entry):
    print("robit_backward")
    mqtt_client.send_message("drive", [-int(left_speed_entry.get()),
                                       -int(right_speed_entry.get())])


def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    print("robit_left")
    mqtt_client.send_message("turn", [int(left_speed_entry.get()),
                                      int(right_speed_entry.get())])


def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    print("robit_right")
    mqtt_client.send_message("turn", [-int(left_speed_entry.get()),
                                      -int(right_speed_entry.get())])


def send_stop(mqtt_client):
    print("robit_stop")
    mqtt_client.send_message("stop")


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
