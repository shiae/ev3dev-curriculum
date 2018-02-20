import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import random

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

    canvas = tkinter.Canvas(main_frame, background="white", width=800,
                            height=500)
    canvas.grid(columnspan=3)

    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()
    mqtt_client.connect("draw", "draw")

    label = ttk.Label(main_frame, text='Robo-Map')
    label.grid(columnspan=3)

    spaceBar = ttk.Button(main_frame, text='spaceBar')
    spaceBar.grid(row=3, column=2)
    spaceBar['command'] = lambda: space_bar(mqtt_client, my_delegate)
    root.bind('<space>',lambda event: space_bar(mqtt_client, my_delegate))

    clear_button = ttk.Button(main_frame, text="Clear")
    clear_button.grid(row=3, column=0)
    clear_button["command"] = lambda: clear(canvas)

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=1)
    quit_button["command"] = lambda: quit_program(mqtt_client, True)






































    alt_frame = ttk.Frame(root, padding=20, relief='raised')
    alt_frame.grid()

    robit = com.MqttClient()
    robit.connect_to_ev3()

    left_speed_label = ttk.Label(alt_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(alt_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=4, column=0)

    right_speed_label = ttk.Label(alt_frame, text="Right")
    right_speed_label.grid(row=3, column=2)
    right_speed_entry = ttk.Entry(alt_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=4, column=2)

    # DONE: 3. Implement the callbacks for the drive buttons. Set both the
    # click and shortcut key callbacks.
    #
    # To help get you started the arm up and down buttons have been implemented.
    # You need to implement the five drive buttons.  One has been writen below to help get you started but is commented
    # out. You will need to change some_callback1 to some better name, then pattern match for other button / key combos.

    forward_button = ttk.Button(alt_frame, text="Forward")
    forward_button.grid(row=5, column=1)
    forward_button['command'] = lambda: send_forward(robit,
                                                     left_speed_entry,
                                                     right_speed_entry)
    root.bind('<Up>', lambda event: send_forward(robit, left_speed_entry,
                                                 right_speed_entry))
    # forward_button and '<Up>' key is done for your here...
    # forward_button['command'] = lambda: some_callback1(robit, left_speed_entry, right_speed_entry)
    # root.bind('<Up>', lambda event: some_callback1(robit, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(alt_frame, text="Left")
    left_button.grid(row=6, column=0)
    left_button['command'] = lambda: send_left(robit, left_speed_entry,
                                               right_speed_entry)
    root.bind('<Left>', lambda event: send_left(robit, left_speed_entry,
                                                right_speed_entry))
    # left_button and '<Left>' key

    stop_button = ttk.Button(alt_frame, text="Stop")
    stop_button.grid(row=6, column=1)
    stop_button['command'] = lambda: send_stop(robit)
    root.bind('<space>', lambda event: send_stop(robit))
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)

    right_button = ttk.Button(alt_frame, text="Right")
    right_button.grid(row=6, column=2)
    right_button['command'] = lambda: send_right(robit, left_speed_entry,
                                                 right_speed_entry)
    root.bind('<Right>',
              lambda event: send_right(robit, left_speed_entry,
                                       right_speed_entry))
    # right_button and '<Right>' key

    back_button = ttk.Button(alt_frame, text="Back")
    back_button.grid(row=7, column=1)
    back_button['command'] = lambda: send_backward(robit,
                                                   left_speed_entry,
                                                   right_speed_entry)
    root.bind('<Down>',
              lambda event: send_backward(robit, left_speed_entry,
                                          right_speed_entry))
    # back_button and '<Down>' key

    up_button = ttk.Button(alt_frame, text="Up")
    up_button.grid(row=8, column=0)
    up_button['command'] = lambda: send_up(robit)
    root.bind('<u>', lambda event: send_up(robit))

    down_button = ttk.Button(alt_frame, text="Down")
    down_button.grid(row=9, column=0)
    down_button['command'] = lambda: send_down(robit)
    root.bind('<j>', lambda event: send_down(robit))

    # Buttons for quit and exit
    q_button = ttk.Button(alt_frame, text="Quit")
    q_button.grid(row=8, column=2)
    q_button['command'] = (lambda: quit_program(robit, False))

    e_button = ttk.Button(alt_frame, text="Exit")
    e_button.grid(row=9, column=2)
    e_button['command'] = (lambda: quit_program(robit, True))

    root.mainloop()



def space_bar(mqtt_client, myDelegate):
    print(myDelegate.count)

    mqtt_client.send_message('on_circle_draw', ['red', random.randint(0,
                                                                      myDelegate.count),
                                                random.randint(0,
                                                               myDelegate.count)])
    myDelegate.count += 1


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


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()
