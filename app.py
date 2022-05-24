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

        self.title_font = tkfont.Font(family="Arial", size=18, weight="bold")   # formatting purposes (set font properties)
        self.subtitle_font = tkfont.Font(family = "Arial", size = 12, weight = "bold")

        # pages / frames are in a stack (frames that need to be visible will be raised above other frames)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # for F in (LandingPage, TasksMainPage, AboutPage, PageThree):
        for F in (LandingPage, TasksMainPage, AboutPage, AllTasksPage, AllCategoriesPage):
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

# loadTasks - function to load all tasks from database 
def loadTasks(listbox_tasks): 
    # select all tasks
    dbCursor.execute("SELECT CONCAT(CAST(`duedate` AS CHAR), ': ', tasktitle, ' - ', description, ' | Status: ', status) FROM task")
    listbox_tasks.delete(0, END)
    i = 0
    for task in dbCursor: 
        for j in range(len(task)):
            listbox_tasks.insert(END, task[j])

# loadTasks - function to load all categories from database 
def loadCategories(listbox_category): 
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

        # button to view all tasks
        allTasksBtn = Button(self, text="View all tasks", width=48, command=lambda: controller.show_frame("AllTasksPage"))
        allTasksBtn.pack(side = 'top', fill = 'x', pady = 60)  

        # button to view all categories
        allCategoriesBtn = Button(self, text="View all categories", width=48, command=lambda: controller.show_frame("AllCategoriesPage"))
        allCategoriesBtn.pack(side = 'top', fill = 'x', pady = 60)  

        menubutton = Button(self, text = "Go back to the main page", command=lambda: controller.show_frame("LandingPage"))
        menubutton.pack(side = 'top', fill = 'x', pady = 60)

        frame.pack()

#AllTasks - view all tasks page
class AllTasksPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = Frame(self, parent)

        # box to list all tasks
        listbox_tasks = Listbox(frame, height=15, width=70)
        listbox_tasks.pack(side=LEFT)

        # scrollbar for tasks list 
        scrollbar_tasks = Scrollbar(frame)
        scrollbar_tasks.pack(side=RIGHT, fill=Y)

        # vertical scrollbar properties
        listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
        scrollbar_tasks.config(command=listbox_tasks.yview)

        # button to customize view of tasks
        viewTasksByBtn = Button(self, text="View tasks by ...", width=48)
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')

        #button to add a task to a category
        addCategoryBtn = Button(self, text = "Add task to category", width=48)
        addCategoryBtn.pack(side = 'bottom', fill = 'x')

        #button to search for a task
        searchTaskBtn = Button(self, text = "Search for a task", width=48)
        searchTaskBtn.pack(side = 'bottom', fill = 'x')

        #button to mark a task as done (NOTE: a task can be selected from the listbox)
        markDoneBtn = Button(self, text = "Mark as done", width=48)
        markDoneBtn.pack(side = 'bottom', fill = 'x')

        # button to edit a task (NOTE: a task can be selected from the listbox)
        editTaskBtn = Button(self, text = "Edit a task", width=48)
        editTaskBtn.pack(side = 'bottom', fill = 'x')

        # button to delete a task (NOTE: a task can be selected from the listbox)
        deleteTaskBtn = Button(self, text="Delete task", width=48)
        deleteTaskBtn.pack(side = 'bottom', fill = 'x')

        # button to add a task
        addTaskBtn = Button(self, text="Add task", width=48)
        addTaskBtn.pack(side = 'bottom', fill = 'x') 

        # load tasks from database 
        loadDataBtn = Button(self, text="Load data", width=48, command = loadTasks(listbox_tasks))
        loadDataBtn.pack(side = 'bottom', fill = 'x')     

        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("TasksMainPage"))
        menubutton.pack(anchor = NE)

        frame.pack()

#AllCategoriesPage - view all categories page
class AllCategoriesPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = Frame(self, parent)

        # box to list all tasks
        listbox_category = Listbox(frame, height=15, width=70)
        listbox_category.pack(side=LEFT)

        # scrollbar for tasks list 
        scrollbar_category = Scrollbar(frame)
        scrollbar_category.pack(side=RIGHT, fill=Y)

        # vertical scrollbar properties
        listbox_category.config(yscrollcommand=scrollbar_category.set)
        scrollbar_category.config(command=listbox_category.yview)

        # button to customize view of tasks by category
        viewTasksByBtn = Button(self, text="View tasks by category", width=48)
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')    

        # load tasks from database 
        loadDataBtn = Button(self, text="Load data", width=48, command = loadCategories(listbox_category))
        loadDataBtn.pack(side = 'bottom', fill = 'x')  

        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("TasksMainPage"))
        menubutton.pack(anchor = NE)

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
