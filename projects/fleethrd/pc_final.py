
import tkinter
from tkinter import ttk


def main():
    root = tkinter.Tk()
    gui(root)
    root.mainloop()
    # settings = ['a', 'a', 'a']
    # data = ['a', 'a', 'a']
    #  enigma(settings, data)
    # print(data)


def gui(root):
    root.title("Enigma")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    first_input_label = ttk.Label(main_frame, text="First Input")
    first_input_label.grid(row=0, column=0)
    first_input = ttk.Entry(main_frame, width=8)
    first_input.insert(0, "a")
    first_input.grid(row=1, column=0)

    second_input_label = ttk.Label(main_frame, text="Second Input")
    second_input_label.grid(row=0, column=2)
    second_input = ttk.Entry(main_frame, width=8, justify=tkinter.CENTER)
    second_input.insert(0, "a")
    second_input.grid(row=1, column=2)

    third_input_label = ttk.Label(main_frame, text="Third Input")
    third_input_label.grid(row=0, column=4)
    third_input = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    third_input.insert(0, "a")
    third_input.grid(row=1, column=4)

    first_settings_input_label = ttk.Label(main_frame, text="First Setting")
    first_settings_input_label.grid(row=3, column=0)
    first_settings_input = ttk.Entry(main_frame, width=8)
    first_settings_input.insert(0, "a")
    first_settings_input.grid(row=4, column=0)

    second_settings_input_label = ttk.Label(main_frame, text="Second Setting")
    second_settings_input_label.grid(row=3, column=2)
    second_settings_input = ttk.Entry(main_frame, width=8,
                                      justify=tkinter.CENTER)
    second_settings_input.insert(0, "a")
    second_settings_input.grid(row=4, column=2)

    third_settings_input_label = ttk.Label(main_frame, text="Third Setting")
    third_settings_input_label.grid(row=3, column=4)
    third_settings_input = ttk.Entry(main_frame, width=8,
                                     justify=tkinter.RIGHT)
    third_settings_input.insert(0, "a")
    third_settings_input.grid(row=4, column=4)

    encipher_button = ttk.Button(main_frame, text="Encipher")
    encipher_button.grid(row=6, column=2)
    encipher_button['command'] = (lambda: enigma(first_input, second_input,
                                                 third_input,
                                                 first_settings_input,
                                                 second_settings_input,
                                                 third_settings_input))


def enigma(first_input, second_input, third_input, first_settings_input,
           second_settings_input, third_settings_input):
    x = [2, 0, 1, 3]
    y = [3, 2, 1, 0]
    z = [1, 3, 2, 0]
    r = [2, 3, 0, 1]
    wheels = [0, x, y, z, r]
    settings = [first_settings_input.get(), second_settings_input.get(),
                third_settings_input.get()]
    data = [first_input.get(), second_input.get(), third_input.get()]
    set_up(settings, wheels)
    encryption(data, wheels)
    print(data)


def set_up(settings, wheels):
    letters_to_numbers(settings)
    for k in range(len(settings)):
        for j in range(settings[k]):
            rotation(wheels[k+1])
    numbers_to_letters(settings)


def encryption(data, wheels):
    letters_to_numbers(data)
    system_rotation(wheels)
    data[0] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4][wheels[3][wheels[2][wheels[1][data[0]]]]])))
    system_rotation(wheels)
    data[1] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4][wheels[3][wheels[2][wheels[1][data[1]]]]])))
    system_rotation(wheels)
    data[2] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4][wheels[3][wheels[2][wheels[1][data[2]]]]])))
    numbers_to_letters(data)


def system_rotation(wheels):
    rotation(wheels[1])
    if wheels[0] == 1:
        rotation(wheels[2])
    elif wheels[0] == 2:
        rotation(wheels[3])
    wheels[0] += 1


def rotation(wheel):
    temp = wheel[0]
    for k in range(len(wheel) - 1):
        if wheel[k + 1] > 0:
            wheel[k] = wheel[k + 1] - 1
        else:
            wheel[k] = 3
    if temp > 0:
        wheel[3] = temp - 1
    else:
        wheel[3] = 3


def letters_to_numbers(data):
    for k in range(len(data)):
        if data[k] == 'a':
            data[k] = 0
        elif data[k] == 'b':
            data[k] = 1
        elif data[k] == 'c':
            data[k] = 2
        elif data[k] == 'd':
            data[k] = 3


def numbers_to_letters(data):
    for k in range(len(data)):
        if data[k] == 0:
            data[k] = 'a'
        elif data[k] == 1:
            data[k] = 'b'
        elif data[k] == 2:
            data[k] = 'c'
        elif data[k] == 3:
            data[k] = 'd'


main()
