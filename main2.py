import tkinter as tk
import Window as App

def main():
    # Set up tkinter window
    root = tk.Tk()
    root.title("Conway's Game of Life")
    root.configure(bg='#1b1b1b')
    w, h = 960, 480
    ws, hs = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (ws/2) - (w/2), (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    # Decide on size of cells
    cell_size = 12
    app = App.MainApplication(root, cell_size)
    app.mainloop()



if __name__ == '__main__':
    main()
