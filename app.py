#reference for tkinter: https://pythonexamples.org/python-tkinter-login-form/
#import tkinter
from tkinter import *       
from functools import partial
from tkinter import messagebox 
from tkinter import font as tkfont      # formatting purposes
import datetime                         # for sorting by month
import re                               # for input validation

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
# Code reference for changing between frames:
# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
class SampleApp(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family="Arial", size=18, weight="bold")   # formatting purposes (set font properties)
        self.subtitle_font = tkfont.Font(family = "Arial", size = 12, weight = "bold")
        # pages / frames are in a stack (frames that need to be visible will be raised above other frames)
        # NOTE: self parameter is always needed in the parameter of functions under SampleApp class 
            # self - refers to the current instance of the class & used to access variables that belongs to the class
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # NOTE: always add newly created pages in the parameters
        for F in (LandingPage, TasksMainPage, AboutPage, AllTasksPage, AddTaskPage, EditTaskPage, MarkTaskDonePage, DeleteTaskPage, AllCategoriesPage, AddCategoryPage, ViewCategoryPage, ViewByDatePage, ViewByMonthPage, EditCategoryPage, AddTaskToCategoryPage, DeleteCategoryPage):
            page_name = F.__name__                              # get page name
            frame = F(parent=container, controller=self)        # frame
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("LandingPage")                          # start with landing page

    # show_frame - function to show a frame for a specific page 
    def show_frame(self, page_name):
        frame = self.frames[page_name]      # frame = frame for the specific page 
        frame.tkraise()                     # raise frame above others

    # validateDate - function to check if date is
    def validateDate(date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be [YYYY-MM-DD]")

    # addTask - function to add category to the database (accessible by connector.addTask())
    def addTask(self, title, ddate, desc, dbCursor):
        # early return if title is empty
        if len(title) == 0:
            print("Please input a valid task title.")
            return

        if len(ddate) == 0:
            print("Please input a valid date.")
            return

        SampleApp.validateDate(ddate)
        # select statement to get the maximum value of taskid + 1 (for the id of the to-be-added task)
        dbCursor.execute("SELECT MAX(taskid)+1 FROM task;")     
        for id in dbCursor:     # loop through the result of the select statement 
            tempId = id         # store the value of MAX(taskid) + 1 to tempId; tempId = (<int>,)
        #insert statement 
        insertTask = ("INSERT INTO task (taskid, tasktitle, duedate, description) VALUES (%s, %s, %s, %s);")
        args = tempId[0], title, ddate, desc                  # parameters for %s (tempId[0] will only get the int)
        dbCursor.execute(insertTask, args)       # execute insert statement
        dbConnect.commit()                      # commit changes (insert statement)

        print("Added", title, ddate, desc, "successfully!")

    def editTask(self, oldTitle, newTitle, newStatus, newDDate, newDesc, dbCursor):
        # early return if either input is empty
        if len(oldTitle) == 0 or len(newTitle) == 0:
            print("Please input a valid task title.")
            return

        # retrieves task id to be used for updating task
        findTask = ("SELECT taskid FROM task WHERE tasktitle = (%s);")
        dbCursor.execute(findTask, (oldTitle,))
        taskId = dbCursor.fetchone()

        # early return if task does not exist
        if taskId == None:
            print("Task does not exist.")
            return

        if len(newDDate) == 0:
            print("Please input a valid date.")
            return

        #check if date is valid
        SampleApp.validateDate(newDDate)

        #early return if status != 'Y' or 'y' or 'N' or 'n'
        if newStatus != 'Y' and newStatus != 'N':
            print("Status must be [Y/N]")
            return

        # updates task name and commits changes
        updateTask = "UPDATE task SET tasktitle = (%s), status = (%s), duedate = (%s), description = (%s) WHERE taskid = (%s);" 
        args = newTitle, newStatus, newDDate, newDesc, taskId[0]
        dbCursor.execute(updateTask, args)
        dbConnect.commit()                      

        print("Successfully edited task: " + newTitle, newStatus, newDDate, newDesc)

    def markTaskDone(self, title, dbCursor):
        if len(title) == 0:
            print("Please input a valid task title.")
            return
        
        findTask = ("SELECT taskid FROM task WHERE tasktitle = (%s);")
        dbCursor.execute(findTask, (title,))
        taskId = dbCursor.fetchone()

        if taskId == None:
            print("Task does not exist.")
            return

        markTask = "UPDATE task SET status = 'Y' WHERE taskid = (%s);"
        dbCursor.execute(markTask, taskId)
        dbConnect.commit()

        print("Successfully marked task " + title + " as done.")

    def deleteTask(self, title, dbCursor):
        if len(title) == 0:
            print("Please input a valid task title.")
            return
        
        findTask = ("SELECT taskid FROM task WHERE tasktitle = (%s);")
        dbCursor.execute(findTask, (title,))
        taskId = dbCursor.fetchone()

        if taskId == None:
            print("Task does not exist.")
            return

        deleteTask = "DELETE FROM task WHERE taskid = (%s);"
        args = taskId
        dbCursor.execute(deleteTask, args)
        dbConnect.commit()

        print("Successfully deleted task: " + title)

    # addCategory - function to add category to the database (accessible by connector.addCategory())
    def addCategory(self, name, dbCursor):
        # check if input is empty 
        if len(name) == 0:
            print("Please input a valid category name.")
            messagebox.showinfo("Messagebox", "Please input a valid category name.")
            return
       
        #check if category name already exists
        findCat = ("SELECT categoryid FROM category WHERE categoryname = (%s);")
        dbCursor.execute(findCat, (name,))
        cats = dbCursor.fetchone()

        if cats != None:
            print("Category name already exists.")
            messagebox.showinfo("Messagebox", "Category name exists.")
            return
    
        # select statement to get the maximum value of categoryid + 1 (for the id of the to-be-added category)
        dbCursor.execute("SELECT MAX(categoryid)+1 FROM category;")     
        for id in dbCursor:     # loop through the result of the select statement 
            tempId = id         # store the value of MAX(categoryid) + 1 to tempId; tempId = (<int>,)
        #insert statement 
        insertCat = ("INSERT INTO category (categoryid, categoryname) VALUES (%s, %s);")
        args = tempId[0], name                  # parameters for %s (tempId[0] will only get the int)
        dbCursor.execute(insertCat, args)       # execute insert statement
        dbConnect.commit()                      # commit changes (insert statement)

        print("Added", name, "successfully!")
        messagebox.showinfo("Messagebox", "Added category successfully!")
    
    def editCategory(self, oldName, newName, dbCursor):
    
        # early return if either input is empty
        if len(oldName) == 0 or len(newName) == 0:
            print("Please input a valid category.")
            messagebox.showinfo("Messagebox", "Please input a valid category.")
            return
        
        # checks if new name already exists as another category
        verifyCat = ("SELECT categoryid FROM category WHERE categoryname = (%s);")
        dbCursor.execute(verifyCat, (newName,)) 
        catId = dbCursor.fetchone()

        # early return if new name already exists as another category
        if catId != None:
            print("Category already exists.")
            messagebox.showinfo("Messagebox", "Category already exists. Please replace with a different name.")
            return

        # retrieves category id to be used for updating category name
        findCat = ("SELECT categoryid FROM category WHERE categoryname = (%s);")
        dbCursor.execute(findCat, (oldName,))
        catId = dbCursor.fetchone()

        # early return if category does not exist
        if catId == None:
            print("Category does not exist.")
            messagebox.showinfo("Messagebox", "Category does not exist.")
            return

        # updates category name and commits changes
        updateCat = "UPDATE category SET categoryname = (%s) WHERE categoryid = (%s);" 
        args = newName, catId[0] # retrieves id from returned tuple
        dbCursor.execute(updateCat, args)
        dbConnect.commit() # commits changes to the db       

        # prompts success on terminal and on app
        print("Successfully edited category: " + newName)
        messagebox.showinfo("Messagebox", "Successfully edited category!")
    
    def addTaskToCategory(self, taskName, catName, dbCursor):
        # early return if either input is empty
        if len(taskName) == 0:
            print("Please input a valid task name.")
            return
        if len(catName) == 0:
            print("Please input a valid category name.")
            return

        # retrieves task id to be used for inserting into the category
        findTask = ("SELECT taskid FROM task WHERE tasktitle = (%s);")
        dbCursor.execute(findTask, (taskName,))
        taskId = dbCursor.fetchone()

        # early return if task does not exist
        if taskId == None:
            print("Task does not exist.")
            return
        
        # retrieves category id to be used for updating category name
        findCat = ("SELECT categoryid FROM category WHERE categoryname = (%s);")
        dbCursor.execute(findCat, (catName,))
        catId = dbCursor.fetchone()

        # early return if category does not exist
        if catId == None:
            print("Category does not exist.")
            return
            
        # updates category name and commits changes
        updateCat = "UPDATE task SET categoryid = (%s) WHERE taskid = (%s);" 
        args = catId[0],taskId[0]
        dbCursor.execute(updateCat, args)
        dbConnect.commit()                      

        print("Successfully added task " + taskName + " to " + catName +" category.")
    
    def deleteCategory(self, name, dbCursor):
        # early return if either input is empty
        if len(name) == 0 or name == "no category" :
            print("Please input a valid category.")
            return

        # retrieves category id to be used for deleting the category
        findCat = ("SELECT categoryid FROM category WHERE categoryname = (%s);")
        dbCursor.execute(findCat, (name,))
        catId = dbCursor.fetchone()

        # early return if category does not exist
        if catId == None:
            print("Category does not exist.")
            return

        # deletes all task from the given category
        getTasks = ("DELETE FROM task WHERE categoryid = (%s);")
        dbCursor.execute(getTasks,catId)
        dbConnect.commit()   

        # deletes category and commits changes
        deleteCat = "DELETE FROM category WHERE categoryid = (%s);" 
        dbCursor.execute(deleteCat, catId)
        dbConnect.commit()                      

        print("Successfully deleted category: " + name)

# LandingPage - landing page for the application (first window)
class LandingPage(Frame): 

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # label for the page 
        label = Label(self, text="Task Management App", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        # button to go to 'view all tasks' page (includes viewing, searching, creating, editing, deleting, and marking tasks as done)
        button1 = Button(self, text="Tasks and Categories",
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
        # button to go back to the main page 
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
        self.listbox_tasks = Listbox(frame, height=15, width=70)
        self.listbox_tasks.pack(side=LEFT)
        # scrollbar for tasks list 
        scrollbar_tasks = Scrollbar(frame)
        scrollbar_tasks.pack(side=RIGHT, fill=Y)
        # vertical scrollbar properties
        self.listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
        scrollbar_tasks.config(command=self.listbox_tasks.yview)

        # button to customize view of tasks by day
        viewTasksByBtn = Button(self, text="View by date", width=48)
        viewTasksByBtn = Button(self, text="View by date", width=48, command=lambda: controller.show_frame("ViewByDatePage"))
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')

        # button to customize view of tasks by month
        viewTasksByBtn = Button(self, text="View by month", width=48)
        viewTasksByBtn = Button(self, text="View by month", width=48, command=lambda: controller.show_frame("ViewByMonthPage"))
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')

        # button to delete a task 
        deleteTaskBtn = Button(self, text="Delete a task", width=48, command=lambda: controller.show_frame("DeleteTaskPage"))
        deleteTaskBtn.pack(side = 'bottom', fill = 'x')
        # NOTE: implement feat only if there is still time (else, delete since it isn't stated in the required feats)
        # #button to search for a task
        # searchTaskBtn = Button(self, text = "Search for a task", width=48)
        # searchTaskBtn.pack(side = 'bottom', fill = 'x')
        #button to mark a task as done 
        markDoneBtn = Button(self, text = "Mark task as done", width=48, command=lambda: controller.show_frame("MarkTaskDonePage"))
        markDoneBtn.pack(side = 'bottom', fill = 'x')

        # button to edit a task 
        editTaskBtn = Button(self, text = "Edit a task", width=48)
        editTaskBtn = Button(self, text = "Edit a task", width=48, command=lambda: controller.show_frame("EditTaskPage"))
        editTaskBtn.pack(side = 'bottom', fill = 'x')

        # button to add a task
        addTaskBtn = Button(self, text="Add task", width=48, command=lambda: controller.show_frame("AddTaskPage"))
        addTaskBtn.pack(side = 'bottom', fill = 'x') 
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("TasksMainPage"))
        menubutton.pack(anchor = NE)
        frame.pack()
        self.after(1000, self.taskUpdate)   # for every 1000 milliseconds, update the page
    # update page (update list of tasks)
    def taskUpdate(self):
        # select all tasks
        dbCursor.execute("SELECT CONCAT(DATE_FORMAT(duedate, '%M-%d-%Y'), ': ', tasktitle, ' - ', description, ' | Status: ', status) FROM task;")
        self.listbox_tasks.delete(0, END)                   # remove data in the listbox display               
        for task in dbCursor:                               # iterate over the results of the select statement
            for j in range(len(task)):                      
                self.listbox_tasks.insert(END, task[j])     # insert categories in the listbox display
        self.after(1000, self.taskUpdate)                   # for every 1000 milliseconds, update the page

#AddTaskPage - page to add a task 
class AddTaskPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("AllTasksPage"))
        menubutton.pack(anchor = NE)
        label = Label(self, text="Add a task", font=controller.title_font)
        label.pack(side="top", pady=10)
        label1 = Label(self, text="Task title")
        label1.pack()
        taskTitle = Entry(self)
        taskTitle.pack()
        label2 = Label(self, text="Due date (YYYY-MM-DD)")
        label2.pack()
        taskDDate = Entry(self)
        taskDDate.pack()
        label3 = Label(self, text="Description")
        label3.pack()
        taskDesc = Entry(self)
        taskDesc.pack()
        buttonAddTask = Button(self, text="Add task", command=lambda: controller.addTask(taskTitle.get(), taskDDate.get(), taskDesc.get(), dbCursor))
        buttonAddTask.pack()
    
class EditTaskPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("AllTasksPage"))
        menubutton.pack(anchor = NE)

        label = Label(self, text="Edit a task", font=controller.title_font)
        label.pack(side="top", pady=10)

        # takes the original task name
        label1 = Label(self, text="Old task title")
        label1.pack()
        oldTask = Entry(self)
        oldTask.pack()

        # takes the new task name
        label2 = Label(self, text="New task title")
        label2.pack()
        newTask = Entry(self)
        newTask.pack()

        # takes the new task status
        label3 = Label(self, text="New task status (Y/N)")
        label3.pack()
        newStatus = Entry(self)
        newStatus.pack()

        # takes the new task due date
        label4 = Label(self, text="New due date (YYYY-MM-DD)")
        label4.pack()
        newDDate = Entry(self)
        newDDate.pack()

         # takes the new task due date
        label5 = Label(self, text="New description")
        label5.pack()
        newDesc = Entry(self)
        newDesc.pack()

        # proceeds to the editCategory function on button click
        buttonEditTask = Button(self, text="Edit task", command=lambda: controller.editTask(oldTask.get(), newTask.get(), newStatus.get(), newDDate.get(), newDesc.get(), dbCursor))
        buttonEditTask.pack()

class MarkTaskDonePage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("AllTasksPage"))
        menubutton.pack(anchor = NE)

        label = Label(self, text="Mark a task as done", font=controller.title_font)
        label.pack(side="top", pady=10)

        # takes the task name
        label1 = Label(self, text="Task title")
        label1.pack()
        title = Entry(self)
        title.pack()

        # proceeds to the markTaskDone function on button click
        markDoneBtn = Button(self, text="Mark task", command=lambda: controller.markTaskDone(title.get(), dbCursor))
        markDoneBtn.pack()

class DeleteTaskPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("AllTasksPage"))
        menubutton.pack(anchor = NE)

        label = Label(self, text="Delete a task", font=controller.title_font)
        label.pack(side="top", pady=10)

        # takes the original task name
        label1 = Label(self, text="Enter title")
        label1.pack()
        title = Entry(self)
        title.pack()

        # proceeds to the deleteTask function on button click
        buttonDeleteTask = Button(self, text="Delete task", command=lambda: controller.deleteTask(title.get(), dbCursor))
        buttonDeleteTask.pack()

#AllCategoriesPage - view all categories page
class AllCategoriesPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        frame = Frame(self, parent)
        # box to list all categories
        self.listbox_category = Listbox(frame, height=15, width=70)
        self.listbox_category.pack(side=LEFT)
        # scrollbar for categories list 
        scrollbar_category = Scrollbar(frame)
        scrollbar_category.pack(side=RIGHT, fill=Y)
        # vertical scrollbar properties
        self.listbox_category.config(yscrollcommand=scrollbar_category.set)
        scrollbar_category.config(command=self.listbox_category.yview)
        # NOTE: implement feat only if there is still time (else, delete since it isn't stated in the required feats)
        # #button to search for a category
        # searchCategoryBtn = Button(self, text = "Search for a category", width=48)
        # searchCategoryBtn.pack(side = 'bottom', fill = 'x')
        # button to delete a category 
        deleteCategoryBtn = Button(self, text="Delete a category", width=48, command=lambda: controller.show_frame("DeleteCategoryPage"))
        deleteCategoryBtn.pack(side = 'bottom', fill = 'x')
        #button to add a task to a category
        addTaskCategoryBtn = Button(self, text = "Add a task to a category", width=48, command=lambda: controller.show_frame("AddTaskToCategoryPage"))
        addTaskCategoryBtn.pack(side = 'bottom', fill = 'x')

        # button to edit a category
        editCategoryBtn = Button(self, text = "Edit a category", width=48, command=lambda: controller.show_frame("EditCategoryPage"))
        editCategoryBtn.pack(side = 'bottom', fill = 'x')

        # button to customize view of tasks by category
        viewTasksByBtn = Button(self, text="View a category", width=48)
        viewTasksByBtn = Button(self, text="View a category", width=48, command=lambda: controller.show_frame("ViewCategoryPage"))
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')  

        # button to add a category
        addCategoryBtn = Button(self, text="Add a category", width=48, command=lambda: controller.show_frame("AddCategoryPage"))
        addCategoryBtn.pack(side = 'bottom', fill = 'x' )   
        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("TasksMainPage"))
        menubutton.pack(anchor = NE)
        frame.pack()
        self.after(1000, self.categoryUpdate)   # for every 1000 milliseconds, update the page
    # update page (update list of categories)
    def categoryUpdate(self):
        dbCursor.execute("SELECT categoryname FROM category;")      # select all categories
        self.listbox_category.delete(0, END)                        # remove data in the listbox display
        for category in dbCursor:                                   # iterate over the results of the select statement 
            for j in range(len(category)):
                self.listbox_category.insert(END, category[j])      # insert categories in the listbox display
        self.after(1000, self.categoryUpdate)                               # for every 1000 milliseconds, update the page

#AddCategoryPage - page to add a category 
class AddCategoryPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("AllCategoriesPage"))
        menubutton.pack(anchor = NE)
        label = Label(self, text="Add a category", font=controller.title_font)
        label.pack(side="top", pady=10)
        label1 = Label(self, text="Category name")
        label1.pack()
        catName = Entry(self)
        catName.pack()
        buttonAddCat = Button(self, text="Add category", command=lambda: controller.addCategory(catName.get(), dbCursor))
        buttonAddCat.pack()

#ViewCategoryPage - sorts all tasks by category
class ViewCategoryPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = Frame(self, parent)

        # label and input box for category to be viewed
        label1 = Label(self, text="Category name")
        label1.pack()
        catName = Entry(self)
        catName.pack()

        # calls viewCategory and displays tasks under category inputted
        buttonAddCat = Button(self, text="View category", command=lambda: self.viewCategory(catName.get(), dbCursor))
        buttonAddCat.pack()

        # box to list all tasks
        self.listbox_tasks = Listbox(frame, height=15, width=70)
        self.listbox_tasks.pack(side=LEFT)

        # scrollbar for tasks list 
        scrollbar_tasks = Scrollbar(frame)
        scrollbar_tasks.pack(side=RIGHT, fill=Y)

        # vertical scrollbar properties
        self.listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
        scrollbar_tasks.config(command=self.listbox_tasks.yview)

        # button to delete a task 
        deleteTaskBtn = Button(self, text="Delete a task", width=48)
        deleteTaskBtn.pack(side = 'bottom', fill = 'x')

        # NOTE: implement feat only if there is still time (else, delete since it isn't stated in the required feats)
        # #button to search for a task
        # searchTaskBtn = Button(self, text = "Search for a task", width=48)
        # searchTaskBtn.pack(side = 'bottom', fill = 'x')

        #button to mark a task as done 
        markDoneBtn = Button(self, text = "Mark task as done", width=48, command=lambda: controller.show_frame("MarkTaskDonePage"))
        markDoneBtn.pack(side = 'bottom', fill = 'x')

        # button to edit a task 
        editTaskBtn = Button(self, text = "Edit a task", width=48)
        editTaskBtn.pack(side = 'bottom', fill = 'x')

        # button to add a task
        addTaskBtn = Button(self, text="Add task", width=48)
        addTaskBtn.pack(side = 'bottom', fill = 'x') 

        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("TasksMainPage"))
        menubutton.pack(anchor = NE)

        frame.pack()

    def viewCategory(self, name, dbCursor):

        # clears the listbox 
        self.listbox_tasks.delete(0, END)                                       

        # early return if input is empty on button click
        if len(name) == 0:
            self.listbox_tasks.insert(END, "Please enter a valid category.") 
            return
        
        checkCat = ("SELECT c.categoryid FROM category c WHERE categoryname = (%s)")
        dbCursor.execute(checkCat,(name,))
        result = dbCursor.fetchall()

        if result == []:
            self.listbox_tasks.insert(END, "Category does not exist. Please enter another category.") 
            return

        # retrieves the categoryid from category table and checks if it holds any tasks
        searchCat = ("SELECT t.categoryid FROM task t WHERE t.categoryid IN (SELECT c.categoryid FROM category c WHERE categoryname = (%s));")
        dbCursor.execute(searchCat,(name,))
        result = dbCursor.fetchall()

        # early return if category does not exist
        if result == []:
            self.listbox_tasks.insert(END, "Category does not have any tasks.") 
            return

        # retrieves all tasks from the category
        viewId = result[0][0]
        viewCat = ("SELECT CONCAT(DATE_FORMAT(duedate, '%M-%d-%Y'), ': ', tasktitle, ' - ', description, ' | Status: ', status) FROM task WHERE categoryid = (%s);")
        dbCursor.execute(viewCat,(viewId,))
        output = dbCursor.fetchall()

        self.listbox_tasks.insert(END, "Tasks under category: " + name) 

        # inserts tasks into the listbox
        for task in output:                               
            for j in range(len(task)):                  
                self.listbox_tasks.insert(END, task[j])     

#ViewByDatePage - sorts all tasks by date
class ViewByDatePage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = Frame(self, parent)

        # label and input box for category to be viewed
        label1 = Label(self, text="Enter date (yyyy-mm-dd):")
        label1.pack()
        date = Entry(self)
        date.pack()

        # calls viewByDate to view tasks within the date specified
        buttonViewDate = Button(self, text="Sort", command=lambda: self.viewByDate(date.get(), dbCursor))
        buttonViewDate.pack()

        # box to list all tasks
        self.listbox_tasks = Listbox(frame, height=15, width=70)
        self.listbox_tasks.pack(side=LEFT)

        # scrollbar for tasks list 
        scrollbar_tasks = Scrollbar(frame)
        scrollbar_tasks.pack(side=RIGHT, fill=Y)

        # vertical scrollbar properties
        self.listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
        scrollbar_tasks.config(command=self.listbox_tasks.yview)

        # button to customize view of tasks by day
        viewTasksByBtn = Button(self, text="View by date", width=48, command=lambda: controller.show_frame("ViewByDatePage"))
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')

        # button to customize view of tasks by month
        viewTasksByBtn = Button(self, text="View by month", width=48, command=lambda: controller.show_frame("ViewByMonthPage"))
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')

        # button to delete a task 
        deleteTaskBtn = Button(self, text="Delete a task", width=48, command=lambda: controller.show_frame("DeleteTaskPage"))
        deleteTaskBtn.pack(side = 'bottom', fill = 'x')

        # NOTE: implement feat only if there is still time (else, delete since it isn't stated in the required feats)
        # #button to search for a task
        # searchTaskBtn = Button(self, text = "Search for a task", width=48)
        # searchTaskBtn.pack(side = 'bottom', fill = 'x')

        #button to mark a task as done 
        markDoneBtn = Button(self, text = "Mark task as done", width=48, command=lambda: controller.show_frame("MarkTaskDonePage"))
        markDoneBtn.pack(side = 'bottom', fill = 'x')

        # button to edit a task 
        editTaskBtn = Button(self, text = "Edit a task", width=48, command=lambda: controller.show_frame("EditTaskPage"))
        editTaskBtn.pack(side = 'bottom', fill = 'x')

        # button to add a task
        addTaskBtn = Button(self, text="Add task", width=48, command=lambda: controller.show_frame("AddTaskPage"))
        addTaskBtn.pack(side = 'bottom', fill = 'x') 

        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("TasksMainPage"))
        menubutton.pack(anchor = NE)

        frame.pack()

    def viewByDate(self, date, dbCursor):

        self.listbox_tasks.delete(0, END)        

        # uses regex to check input
        valid = re.search("[2][0-9]{3}\-((0[1-9])|(1[0-2]))\-(([0][1-9])|([12][0-9])|([3][01]))", date)                             

        # early return if input is empty
        if len(date) == 0 or not valid:
            self.listbox_tasks.insert(END, "Please enter a valid date.") 
            return

        # retrieves tasks for the given date
        viewByDate = ("SELECT CONCAT(DATE_FORMAT(duedate, '%M-%d-%Y'), ': ', tasktitle, ' - ', description, ' | Status: ', status) FROM task WHERE duedate = (%s);")
        dbCursor.execute(viewByDate,(date,))
        output = dbCursor.fetchall()

        # early return if month does not contain any tasks
        if output == []:
            self.listbox_tasks.insert(END, "There are no tasks for this date.") 
            return

        # converts the numeric date into its string equivalent
        dateObj = datetime.datetime.strptime(date, "%Y-%m-%d")
        fullDate = dateObj.strftime("%B %d %Y")
        self.listbox_tasks.insert(END, "Tasks for " + fullDate + ":") 

        # inserts tasks into the listbox
        for task in output:     
            for j in range(len(task)):              
                self.listbox_tasks.insert(END, task[j])   

#ViewByMonthPage - sorts all tasks by month
class ViewByMonthPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = Frame(self, parent)

        # label and input box for category to be viewed
        label1 = Label(self, text="Enter month (mm):")
        label1.pack()
        date = Entry(self)
        date.pack()

        # calls viewByMonth to view tasks within the month specified
        buttonViewMonth = Button(self, text="Sort", command=lambda: self.viewByMonth(date.get(), dbCursor))
        buttonViewMonth.pack()

        # box to list all tasks
        self.listbox_tasks = Listbox(frame, height=15, width=70)
        self.listbox_tasks.pack(side=LEFT)

        # scrollbar for tasks list 
        scrollbar_tasks = Scrollbar(frame)
        scrollbar_tasks.pack(side=RIGHT, fill=Y)

        # vertical scrollbar properties
        self.listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
        scrollbar_tasks.config(command=self.listbox_tasks.yview)

        # button to customize view of tasks by day
        viewTasksByBtn = Button(self, text="View by date", width=48, command=lambda: controller.show_frame("ViewByDatePage"))
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')

        # button to customize view of tasks by month
        viewTasksByBtn = Button(self, text="View by month", width=48, command=lambda: controller.show_frame("ViewByMonthPage"))
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')

        # button to delete a task 
        deleteTaskBtn = Button(self, text="Delete a task", width=48, command=lambda: controller.show_frame("DeleteTaskPage"))
        deleteTaskBtn.pack(side = 'bottom', fill = 'x')

        # NOTE: implement feat only if there is still time (else, delete since it isn't stated in the required feats)
        # #button to search for a task
        # searchTaskBtn = Button(self, text = "Search for a task", width=48)
        # searchTaskBtn.pack(side = 'bottom', fill = 'x')

        #button to mark a task as done 
        markDoneBtn = Button(self, text = "Mark task as done", width=48, command=lambda: controller.show_frame("MarkTaskDonePage"))
        markDoneBtn.pack(side = 'bottom', fill = 'x')

        # button to edit a task 
        editTaskBtn = Button(self, text = "Edit a task", width=48, command=lambda: controller.show_frame("EditTaskPage"))
        editTaskBtn.pack(side = 'bottom', fill = 'x')

        # button to add a task
        addTaskBtn = Button(self, text="Add task", width=48, command=lambda: controller.show_frame("AddTaskPage"))
        addTaskBtn.pack(side = 'bottom', fill = 'x') 

        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("TasksMainPage"))
        menubutton.pack(anchor = NE)

        frame.pack()

    def viewByMonth(self, date, dbCursor):

        self.listbox_tasks.delete(0, END)       
        
        # uses regex to check input
        valid = re.search("(^0[1-9]$)|(^1[0-2]$)", date)                                   

        # early return if input is empty
        if len(date) == 0 or not valid:
            self.listbox_tasks.insert(END, "Please enter a valid date.")  
            return

        # retrieves tasks for the given month
        viewByMonth = ("SELECT CONCAT(DATE_FORMAT(duedate, '%M-%d-%Y'), ': ', tasktitle, ' - ', description, ' | Status: ', status) FROM task WHERE MONTH(duedate) = (%s);")
        dbCursor.execute(viewByMonth,(date,))
        output = dbCursor.fetchall()

        # early return if month does not contain any tasks
        if output == []:
            self.listbox_tasks.insert(END, "There are no tasks for this month.") 
            return

        # converts the numeric date into its string equivalent
        dateObj = datetime.datetime.strptime(date, "%m")
        month = dateObj.strftime("%B")
        self.listbox_tasks.insert(END, "Tasks for the month of " + month + ":") 

        # inserts tasks into the listbox
        for task in output:     
            for j in range(len(task)):              
                self.listbox_tasks.insert(END, task[j])  

#EditCategoryPage - edits category name
class EditCategoryPage(Frame): 
    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller

        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("AllCategoriesPage"))
        menubutton.pack(anchor = NE)

        label = Label(self, text="Edit a category", font=controller.title_font)
        label.pack(side="top", pady=10)

        # takes the original category name
        label1 = Label(self, text="Old category name")
        label1.pack()
        oldCat = Entry(self)
        oldCat.pack()

        # takes the new category name
        label2 = Label(self, text="New category name")
        label2.pack()
        newCat = Entry(self)
        newCat.pack()

        # proceeds to the editCategory function on button click
        buttonEditCat = Button(self, text="Edit category", command=lambda: controller.editCategory(oldCat.get(), newCat.get(), dbCursor))
        buttonEditCat.pack()

class AddTaskToCategoryPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("AllCategoriesPage"))
        menubutton.pack(anchor = NE)

        label = Label(self, text="Add a task to a Category", font=controller.title_font)
        label.pack(side="top", pady=10)

        # takes the task name
        label1 = Label(self, text="Task name")
        label1.pack()
        taskname = Entry(self)
        taskname.pack()

        # takes the category name
        label2 = Label(self, text="Name of category")
        label2.pack()
        catname = Entry(self)
        catname.pack()

        # proceeds to the addTaskToCategory function on button click
        buttonEditCat = Button(self, text="Add task into category", command=lambda: controller.addTaskToCategory(taskname.get(), catname.get(), dbCursor))
        buttonEditCat.pack()

class DeleteCategoryPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("AllCategoriesPage"))
        menubutton.pack(anchor = NE)

        label = Label(self, text="Delete a category", font=controller.title_font)
        label.pack(side="top", pady=10)

        # takes the original task name
        label1 = Label(self, text="Enter category name")
        label1.pack()
        catname = Entry(self)
        catname.pack()

        # proceeds to the deleteCategory function on button click
        buttonDeleteCategory = Button(self, text="Delete category", command=lambda: controller.deleteCategory(catname.get(), dbCursor))
        buttonDeleteCategory.pack()

# AboutPage - about page 
class AboutPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = 'CMSC 127 project\n\nJamie Mari O. Ciron\nRalph Jason D. Corrales\nAriel Raphael F. Magno\nMarie Sophia Therese T. Nakashima')
        # button to go to the main page
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
