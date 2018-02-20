
import tkinter
from tkinter import ttk


def main():
    root = tkinter.Tk()
    root.title("Robit")
    style = ttk.Style()

    label0 = ttk.Label(root, text=" ", font=('Helvetica', 10))
    label0.grid(row=0, column=0)

    label1 = ttk.Label(root, text="What do you want Robit to do?",
                       font=("Helvetica", 17))
    label1.grid(row=2, column=0)

    style.configure('my.TFrame', background='#a8c9ff')
    frame1 = ttk.Frame(root, style='my.TFrame', padding=70)
    frame1.grid()

    root = tkinter.Toplevel()
    heart = tkinter.PhotoImage(file="heart.png")
    label = ttk.Label(root, image=heart, padding=50)
    label.grid()
    frame = ttk.Frame(root, padding=10)
    frame.grid()
    root.mainloop()

    popup = tkinter.Toplevel(root)
    heart = tkinter.PhotoImage(file="heart.png")
    label = ttk.Label(popup, image=heart, padding=50)
    label.grid()
    frame = ttk.Frame(popup, padding=10)
    frame.grid()

main()
