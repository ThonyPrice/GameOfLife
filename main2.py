import tkinter as tk
import Window as App

def main():
    root = tk.Tk()
    root.title("Conway's Game of Life")
    w, h = 800, 480
    ws, hs = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (ws/2) - (w/2), (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    app = App.MainApplication(root)
    app.mainloop()



if __name__ == '__main__':
    main()
