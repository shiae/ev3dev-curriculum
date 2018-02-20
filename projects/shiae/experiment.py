
import tkinter
from tkinter import ttk


def main():
    root = tkinter.Toplevel()
    heart = tkinter.PhotoImage(file="heart.png")
    label = ttk.Label(root, image=heart, padding=50)
    label.grid()
    frame = ttk.Frame(root, padding=10)
    frame.grid()
    root.mainloop()


main()
