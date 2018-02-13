



def main():
    x = [2, 0, 1, 3]
    y = [3, 2, 1, 0]
    z = [1, 3, 2, 0]
    r = [2, 3, 0, 1]
    wheels = [0, x, y, z, r]
    data = ['a', 'a', 'a']
    encryption(data, wheels)
    print(data)


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
    x_rotation(wheels[1])
    if wheels[0] == 1:
        y_rotation(wheels[2])
    elif wheels[0] == 2:
        z_rotation(wheels[3])
    wheels[0] += 1


def x_rotation(wheel):
    


def y_rotation(wheel):



def z_rotation(wheel):



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