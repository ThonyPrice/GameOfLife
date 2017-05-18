# GameOfLife
#### A project in ProjINDA 2017

### 1. Project Description:
In this project we will with the help of Python create a simulation of Conway's Game of life. For more information on Game of Life, see:
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

The developed program will be a desktop application. The project will be written in 100% Python using the library tkinter for the GUI.

In the GUI, the user will be able to read about the Conway's Game of life. The user may also run a simulation of a predetermined Game of Life board. The user can see how the board changes over generations and is also available to change board at any given time. Lastly, the user will also be able to change the speed of the simulation.

![alt text](https://gits-15.sys.kth.se/storage/user/1795/files/f2ccd68c-33ed-11e7-9431-64af81842d93)

Figure 1: GUI of Game of Life (8 May 2017).  

### 2. How to run the program:

2.1 To begin with install python 3.X from Pythons webpage:

https://www.python.org/downloads/

2.2 Install Pygame:

For Mac:

https://pygame.org/wiki/macintosh

For Windows:

http://www.pygame.org/download.shtml

2.2 Clone the repository by using git: <br />
```$ git clone https://gits-15.sys.kth.se/nlindq/GameOfLife.git```

2.3 Run the code in the shell using: <br />
```$ python3 main.py```

### 3. Testing strategy

3.1 The program will be tested properly when close to final version.

3.2 The user tests should be conducted by formulating tasks that are mandatory for a functional minimal viable product. These tasks should then be controlled to be easily performed by an average user.

3.3 A unit test, using pythons unittest, will be used to confirm the correctness and reliability of the core features of the program such as update cells and alive counter.
