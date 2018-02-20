
import tkinter
from tkinter import ttk


def main():
    root = tkinter.Tk()
    hearts = tkinter.PhotoImage(file="heart.png")
    label = ttk.Label(root, image=hearts, padding=50)
    label.grid()
    frame = ttk.Frame(root, padding=10)
    frame.grid()
    root.mainloop()


main()
