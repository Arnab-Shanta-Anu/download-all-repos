from tkinter import *

root = Tk()
root.title("download-script")
root.geometry("600x400+300+300")  # widthxheight+top height+left distance

userNameLbl = Label(root, text="enter your username")
userNameLbl.grid(row=0, column=0)
userNameEntry = Entry(root)
userNameEntry.grid(row=0, column=1)

root.mainloop()
