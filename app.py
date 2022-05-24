#reference for tkinter: https://pythonexamples.org/python-tkinter-login-form/

#import tkinter
from tkinter import *       
from functools import partial
from tkinter import font as tkfont      # formatting purposes

#reference for mysql connector: https://www.youtube.com/watch?v=oDR7k66x-AU&t=427s&ab_channel=DiscoverPython

# install mysql 
import mysql.connector as mariadb

#create mysql connection 
dbConnect = mariadb.connect(user ="test", password='cmsc127', host ='localhost', port ='3306')
dbCursor = dbConnect.cursor()

# show databases then use CMSC127Project
dbCursor.execute("SHOW DATABASES")

#CHECKING PURPOSES ONLY: prints all databases in MariaDB if it has connected successfully (delete / comment after)
for x in dbCursor:
    print(x)

# use 'cmsc127project' database
dbCursor.execute("USE cmsc127project")

#FRONTEND

# Code reference for changing between frames:
# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
class SampleApp(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # formatting purposes (set font properties)
        self.title_font = tkfont.Font(family="Arial", size=18, weight="bold")   
        self.subtitle_font = tkfont.Font(family = "Arial", size = 12, weight = "bold")

        # pages / frames are in a stack (frames that need to be visible will be raised above other frames)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # for F in (LandingPage, TasksMainPage, AboutPage, PageThree):
        for F in (LandingPage, TasksMainPage, AboutPage):
            page_name = F.__name__                              # get page name
            frame = F(parent=container, controller=self)        # frame
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LandingPage")                          # start with landing page

    # show_frame - function to show a frame for a specific page 
    def show_frame(self, page_name):
        frame = self.frames[page_name]      # frame = frame for the specific page 
        frame.tkraise()                     # raise frame above others 

# LandingPage - landing page for the application (first window)
class LandingPage(Frame): 

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, text="Task Management App", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # button to go to 'view all tasks' page (includes viewing, searching, creating, editing, deleting, and marking tasks as done)
        button1 = Button(self, text="Tasks",
            command=lambda: controller.show_frame("TasksMainPage"))      

        # button to go to 'about the creators' page (includes members and desc of app) 
        button2 = Button(self, text="About",
            command=lambda: controller.show_frame("AboutPage"))    

        # button to exit the program 
        button3 = Button(self, text="Exit",
            command=lambda: controller.destroy())                   

        # formatting purposes (position, width, padding)
        button1.pack(side = "top", fill = "x", pady = 20)
        button2.pack(side = "top", fill = "x", pady = 20)
        button3.pack(side = "top", fill = "x", pady = 20)

# loadData - function to load tasks from database 
def loadData(listbox_category, listbox_tasks): 
    # select all tasks
    dbCursor.execute("SELECT CONCAT(CAST(`duedate` AS CHAR), ': ', tasktitle, ' - ', description) FROM task")
    listbox_tasks.delete(0, END)
    i = 0
    for task in dbCursor: 
        for j in range(len(task)):
            listbox_tasks.insert(END, task[j])

    # select all categories
    dbCursor.execute("SELECT categoryname FROM category")
    listbox_category.delete(0, END)
    i = 0
    for task in dbCursor: 
        for j in range(len(task)):
            listbox_category.insert(END, task[j])

# TasksMainPage - 'tasks' page
class TasksMainPage(Frame): 

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = Frame(self, parent)

        # label for category and task listbox
        label = Label(self, text="All categories \t\t All Tasks", font=controller.subtitle_font)
        label.pack(side="top", fill= 'none', pady=10, anchor = NW)

        # box to list all categories
        listbox_category = Listbox(frame, height=15, width=20)
        listbox_category.pack(side=LEFT)

        # box to list all tasks
        listbox_tasks = Listbox(frame, height=15, width=50)
        listbox_tasks.pack(side=LEFT)

        # scrollbar for tasks list 
        scrollbar_tasks = Scrollbar(frame)
        scrollbar_tasks.pack(side=RIGHT, fill=Y)

        # vertical scrollbar properties
        listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
        scrollbar_tasks.config(command=listbox_tasks.yview)

        # load tasks from database 
        loadDataBtn = Button(self, text="Load data", width=48, command = loadData(listbox_category, listbox_tasks))
        loadDataBtn.pack(side = 'bottom')

        # button to add a task
        addTaskBtn = Button(self, text="Add task", width=48)
        addTaskBtn.pack(side = 'bottom')

        # button to delete a task (NOTE: a task can be selected from the listbox)
        deleteTaskBtn = Button(self, text="Delete task", width=48)
        deleteTaskBtn.pack(side = 'bottom')

        # button to edit a task (NOTE: a task can be selected from the listbox)
        editTaskBtn = Button(self, text = "Edit a task", width=48)
        editTaskBtn.pack(side = 'bottom')

        #button to mark a task as done (NOTE: a task can be selected from the listbox)
        markDoneBtn = Button(self, text = "Mark as done", width=48)
        markDoneBtn.pack(side = 'bottom')

        #button to add a task to a category
        addCategoryBtn = Button(self, text = "Add task to category", width=48)
        addCategoryBtn.pack(side = 'bottom')

        # button to customize view of tasks
        viewTasksByBtn = Button(self, text="View tasks by ...", width=48)
        viewTasksByBtn.pack(side = 'bottom')        

        frame.pack()

# AboutPage - about page 
class AboutPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = 'CMSC 127 project\n\nJamie Mari O. Ciron\nRalph Jason D. Corrales\nAriel Raphael F. Magno\nMarie Sophia Therese T. Nakashima')

        label.pack(side = "top", fill = "x", pady = 10)
        button = Button(self, text = "Go to the main page",
        command=lambda: controller.show_frame("LandingPage"))
        button.pack()

# mainProgram - starts the application
def mainProgram(): 
    if __name__ == "__main__":
        root = SampleApp()
        root.title("127 Task management app")
        root.mainloop()

mainProgram()
