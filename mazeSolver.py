import collections
import math
import time
import tkinter
from collections import deque
from queue import Queue
import random
from tkinter import *
button_list = []

color_time_counter = 0  # counter for time to update the buttons that show the path
count_for_location = 0  # marks for location and destination (1 loc. and 1 dest.)
count_for_destination = 0
submit_location_clicked = False  # marks if specific buttons have been clicked
submit_obstacles_clicked = False
submit_destination_clicked = False
submit_find_path_clicked = False
submit_erase_clicked = False


def on_drag_unbind():  # function to reset the bind
    for button in button_list:
        button.unbind('<B1-Motion>')


def update_button_spread(node):  # for showing spreading of bfs
    global color_time_counter
    if button_list[node].cget('bg') != "#098a04" and button_list[node].cget('bg') != "#e0c810":
        button_list[node].after(color_time_counter, lambda: button_list[node].config(bg='#a962f0'))
        color_time_counter += 8


def update_button_visualize(node): # for showing the path in visualize algo mode
    global color_time_counter
    button_list[node].after(color_time_counter, lambda: button_list[node].config(bg='white'))
    color_time_counter += 50


def update_button(node):  # updates the buttons where the path is
    global color_time_counter
    button_list[node].after(color_time_counter, lambda: button_list[node].config(bg='#a962f0'))
    color_time_counter += 80


def button_click(x):  # decides which color the click will do after pressing the buttons from the bar
    global count_for_location, count_for_destination, submit_destination_clicked, submit_location_clicked, submit_obstacles_clicked, submit_erase_clicked
    if submit_location_clicked and count_for_location == 0:
        button_list[x].config(bg="#098a04")
        count_for_location = 1
        submit_obstacles_clicked = False
        on_drag_unbind()

    elif submit_destination_clicked and count_for_destination == 0:
        on_drag_unbind()
        button_list[x].config(bg="#e0c810")
        count_for_destination = 1
        submit_obstacles_clicked = False

    elif submit_obstacles_clicked and not submit_erase_clicked: # bind for all buttons obstacles
        for i, element in enumerate(button_list):
            if element.cget('bg') != "#098a04" and element.cget('bg') != "#e0c810":
                element.bind('<B1-Motion>', on_drag_obstacle)
        submit_erase_clicked = False

    elif submit_erase_clicked and not submit_obstacles_clicked:
        for i, element in enumerate(button_list):
            if button_list[x].cget('bg') != "#098a04" and button_list[x].cget('bg') != "#e0c810":
                element.bind('<B1-Motion>', on_drag_erase)
                button_list[x].config(bg="#b0f7ed")
        submit_obstacles_clicked = False


def on_drag_obstacle(event): # function to color button when click-hovering them
    x, y = main_window.winfo_pointerxy()
    btn = main_window.winfo_containing(x, y)
    if btn in button_list and btn.cget('bg') != "#098a04" and btn.cget('bg') != "#e0c810":
        btn.config(bg="#2d3030")


def on_drag_erase(event): # function to color button when click-hovering them
    x, y = main_window.winfo_pointerxy()
    btn = main_window.winfo_containing(x, y)
    if btn in button_list and btn.cget('bg') != "#098a04" and btn.cget('bg') != "#e0c810":
        btn.config(bg="#b0f7ed")


# function for the submit location button to color the location
def submit_location_click():
    global submit_location_clicked
    submit_location_clicked = True


# function for the submit destination button to color the destination
def submit_destination_click():
    global submit_destination_clicked
    submit_destination_clicked = True


# function for the submit obstacles button to color the obstacles
def submit_obstacles_click():
    global submit_obstacles_clicked, submit_erase_clicked
    submit_obstacles_clicked = True
    submit_erase_clicked = False


# function to erase the obstacles
def submit_erase_obstacles():
    global submit_erase_clicked, submit_obstacles_clicked
    submit_erase_clicked = True
    submit_obstacles_clicked = False


# function that calls the bread first search algo just for the path
def submit_find_path():
    global submit_location_clicked, submit_destination_clicked, submit_find_path_clicked
    if submit_location_clicked and submit_destination_clicked and not submit_find_path_clicked:
        submit_find_path_clicked = True
        breadth_first_search()


# function that calls the bread first search algo for visualization
def visualize_algo():
    global submit_location_clicked, submit_destination_clicked, submit_find_path_clicked
    if submit_location_clicked and submit_destination_clicked and not submit_find_path_clicked:
        submit_find_path_clicked = True
        breadth_first_search_visualize()


#  gets the location and the destination
def get_loc_dest():
    loc = -1
    dest = -1
    if submit_location_clicked and submit_destination_clicked:
        for i, button in enumerate(button_list):
            if button_list[i].cget('bg') == "#098a04":
                loc = i
            if button_list[i].cget('bg') == "#e0c810":
                dest = i
    return loc, dest


def breadth_first_search():
    if submit_location_clicked and submit_destination_clicked:
        def search(grid, i, j, queue, visited, parent, level, u):
            if i < len(grid) and j - 1 >= 0 and (i, j - 1) not in visited:
                queue.put((i, j - 1))
                parent[(i, j - 1)] = (i, j)
                level[(i, j - 1)] = level[u] + 1
                visited[(i, j - 1)] = True
                node_path[(i, j - 1)] = node_path[(i, j)] + [(i, j - 1)]
            if i - 1 >= 0 and j < len(grid[i]) and (i - 1, j) not in visited:
                queue.put((i - 1, j))
                parent[(i - 1, j)] = (i, j)
                level[(i - 1, j)] = level[u] + 1
                visited[(i - 1, j)] = True
                node_path[(i - 1, j)] = node_path[(i, j)] + [(i - 1, j)]
            if i < len(grid) and j + 1 < len(grid[i]) and (i, j + 1) not in visited:
                queue.put((i, j + 1))
                parent[(i, j + 1)] = (i, j)
                level[(i, j + 1)] = level[u] + 1
                visited[(i, j + 1)] = True
                node_path[(i, j + 1)] = node_path[(i, j)] + [(i, j + 1)]
            if i + 1 < len(grid) and j < len(grid[i]) and (i + 1, j) not in visited:
                queue.put((i + 1, j))
                parent[(i + 1, j)] = (i, j)
                level[(i + 1, j)] = level[u] + 1
                visited[(i + 1, j)] = True
                node_path[(i + 1, j)] = node_path[(i, j)] + [(i + 1, j)]

        path = []  # list of tuples
        count = 0
        grid = []
        visited = {}
        parent = {}
        level = {}
        node_path = {}
        for i in range(27):
            grid.append([])
            for j in range(41):
                grid[i].append(count)
                count += 1

        # will mark the obstacles from gird labeling them as visited in my dictionary
        obstacles = []
        for i, button in enumerate(button_list):
            if button.cget('bg') == "#2d3030":
                obstacles.append(i)
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] in obstacles:
                    visited[(i, j)] = True

        # transforming the number of location and destination into tuples with coordinates
        loc, dest = get_loc_dest()
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if loc == grid[i][j]:
                    start = (i, j)
                if dest == grid[i][j]:
                    dest = (i, j)

        visited[start] = True
        parent[start] = None
        level[start] = 0
        node_path[start] = [start]
        queue = Queue()
        queue.put(start)

        while not queue.empty():
            u = queue.get()
            i = u[0]
            j = u[1]
            search(grid, i, j, queue, visited, parent, level, u)
            if dest in visited and visited[dest]:
                break

        if dest in node_path:
            path_d = {}  # storing the number of the buttons by coordinates
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    path_d[(i, j)] = grid[i][j]

            for i, element in enumerate(node_path[dest]):
                if element != start and element != dest:
                    update_button(path_d[element])
        else:
            error_window = Toplevel()
            error_window.geometry("675x450")
            error_window.resizable(False, False)
            error_window.title('Error!!')
            error_window.config(bg="#d7c5ed")
            error_window.iconbitmap(r'maze_wfD_icon.ico')
            startframe = tkinter.Frame(error_window)
            canvas = tkinter.Canvas(startframe, width=1280, height=720)
            startframe.pack()
            canvas.pack()

            # Escape / raw string literal
            image_book = tkinter.PhotoImage(file=r"errorbackground.png")
            error_window.one = image_book  # to prevent the image garbage collected.
            canvas.create_image((0, 0), image=image_book, anchor='nw')
            label_error = Label(error_window, text=f"Fix the location and the destination in the maze!!!", bg="#d7c5ed",
                                font=('Abadi Bold', 16)).place(x=100, y=100)
    else:
        error_window = Toplevel()
        error_window.geometry("675x450")
        error_window.resizable(False, False)
        error_window.title('Error!!')
        error_window.config(bg="#d7c5ed")
        error_window.iconbitmap(r'maze_wfD_icon.ico')
        startframe = tkinter.Frame(error_window)
        canvas = tkinter.Canvas(startframe, width=1280, height=720)
        startframe.pack()
        canvas.pack()

        # Escape / raw string literal
        image_book = tkinter.PhotoImage(file=r"errorbackground.png")
        error_window.one = image_book  # to prevent the image garbage collected.
        canvas.create_image((0, 0), image=image_book, anchor='nw')
        label_error = Label(error_window, text=f"Fix the location and the destination in the maze!!!", bg="#d7c5ed",
                              font=('Abadi Bold', 16)).place(x=100, y=100)


def breadth_first_search_visualize():
    if submit_location_clicked and submit_destination_clicked:
        def search(grid, i, j, queue, visited, parent, level, u, path_d):
            if i < len(grid) and j - 1 >= 0 and (i, j - 1) not in visited:
                queue.put((i, j - 1))
                parent[(i, j - 1)] = (i, j)
                level[(i, j - 1)] = level[u] + 1
                visited[(i, j - 1)] = True
                node_path[(i, j - 1)] = node_path[(i, j)] + [(i, j - 1)]
                update_button_spread(path_d[(i, j-1)])
            if i - 1 >= 0 and j < len(grid[i]) and (i - 1, j) not in visited:
                queue.put((i - 1, j))
                parent[(i - 1, j)] = (i, j)
                level[(i - 1, j)] = level[u] + 1
                visited[(i - 1, j)] = True
                node_path[(i - 1, j)] = node_path[(i, j)] + [(i - 1, j)]
                update_button_spread(path_d[(i-1, j)])
            if i < len(grid) and j + 1 < len(grid[i]) and (i, j + 1) not in visited:
                queue.put((i, j + 1))
                parent[(i, j + 1)] = (i, j)
                level[(i, j + 1)] = level[u] + 1
                visited[(i, j + 1)] = True
                node_path[(i, j + 1)] = node_path[(i, j)] + [(i, j + 1)]
                update_button_spread(path_d[(i, j + 1)])
            if i + 1 < len(grid) and j < len(grid[i]) and (i + 1, j) not in visited:
                queue.put((i + 1, j))
                parent[(i + 1, j)] = (i, j)
                level[(i + 1, j)] = level[u] + 1
                visited[(i + 1, j)] = True
                node_path[(i + 1, j)] = node_path[(i, j)] + [(i + 1, j)]
                update_button_spread(path_d[(i+1, j)])

        path = []  # list of tuples
        count = 0
        grid = []
        visited = {}
        parent = {}
        level = {}
        node_path = {}
        for i in range(27):
            grid.append([])
            for j in range(41):
                grid[i].append(count)
                count += 1

        # will mark the obstacles from gird labeling them as visited in my dictionary
        obstacles = []
        for i, button in enumerate(button_list):
            if button.cget('bg') == "#2d3030":
                obstacles.append(i)
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] in obstacles:
                    visited[(i, j)] = True

        # transforming the number of location and destination into tuples with coordinates
        loc, dest = get_loc_dest()
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if loc == grid[i][j]:
                    start = (i, j)
                if dest == grid[i][j]:
                    dest = (i, j)
        path_d = {}  # storing the number of the buttons by coordinates
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                path_d[(i, j)] = grid[i][j]

        visited[start] = True
        parent[start] = None
        level[start] = 0
        node_path[start] = [start]
        queue = Queue()
        queue.put(start)

        while not queue.empty():
            u = queue.get()
            i = u[0]
            j = u[1]
            search(grid, i, j, queue, visited, parent, level, u, path_d)
            if dest in visited and visited[dest]:
                break

        if dest in node_path:
            for i, element in enumerate(node_path[dest]):
                if element != start and element != dest:
                    update_button_visualize(path_d[element])
    else:
        error_window = Toplevel()
        error_window.geometry("675x450")
        error_window.resizable(False, False)
        error_window.title('Error!!')
        error_window.config(bg="#d7c5ed")
        error_window.iconbitmap(r'maze_wfD_icon.ico')
        startframe = tkinter.Frame(error_window)
        canvas = tkinter.Canvas(startframe, width=1280, height=720)
        startframe.pack()
        canvas.pack()

        # Escape / raw string literal
        image_book = tkinter.PhotoImage(file=r"errorbackground.png")
        error_window.one = image_book  # to prevent the image garbage collected.
        canvas.create_image((0, 0), image=image_book, anchor='nw')
        label_error = Label(error_window, text=f"Fix the location and the destination in the maze!!!", bg="#d7c5ed",
                              font=('Abadi Bold', 16)).place(x=100, y=100)


def clear_funct():  # clears the screen for another path finding
    global submit_location_clicked, submit_destination_clicked, submit_obstacles_clicked, count_for_location, count_for_destination, color_time_counter, submit_find_path_clicked, submit_erase_clicked
    submit_location_clicked = False
    submit_destination_clicked = False
    submit_obstacles_clicked = False
    submit_find_path_clicked = False
    submit_erase_clicked = False
    count_for_location = 0
    count_for_destination = 0
    color_time_counter = 0

    for button in button_list:
        button.config(bg="#b0f7ed")
        button.unbind('<B1-Motion>')


def random_funct():  # creates random obstacles on the map
    for i in range(180):
        number = random.randrange(1107)
        if button_list[number].cget('bg') != "#098a04" and button_list[number].cget('bg') != "#e0c810" and button_list[number].cget('bg') != "#2d3030":
            button_list[number].config(bg="#2d3030")


main_window = Tk()
main_window.resizable(False, False)
main_window.geometry("1066x780")
main_window.title('Maze Solver')
main_window.iconbitmap(r'maze_wfD_icon.ico')

label1 = Label(main_window, bg="#85e0ff", width=840, height=200).place(x=0, y=700)
count = 0
pixel = PhotoImage(width=1, height=1)  # to make the buttons smaller with the help of image as background pixels

# #93f5e7
# #a4f5e9
# #b0f7ed
for i in range(27):
    for j in range(41):
        button_list.append(Button(main_window, image=pixel,compound="c",relief=RAISED,font=('Abadi Bold', 14),bg="#b0f7ed", fg="white",width=20, height=20, command=lambda x=count: button_click(x)))
        button_list[count].grid(row=i, column=j)
        count += 1


button_location = Button(main_window, text="Location",relief=RAISED,font=('Abadi Bold', 14),bg="#439fe6", fg="white", command=submit_location_click).place(x=120, y=720)
button_obstacles = Button(main_window, text="Obstacles",relief=RAISED,font=('Abadi Bold', 14),bg="#439fe6", fg="white", command=submit_obstacles_click).place(x=360, y=720)
button_destination = Button(main_window, text="Destination",relief=RAISED,font=('Abadi Bold', 14),bg="#439fe6", fg="white",command=submit_destination_click).place(x=230, y=720)
button_find_path = Button(main_window, text="Find path",relief=RAISED,font=('Abadi Bold', 14),bg="#439fe6", fg="white", command=submit_find_path).place(x=680, y=720)
button_clear = Button(main_window, text="Clear",relief=RAISED,font=('Abadi Bold', 14),bg="#439fe6", fg="white", command=clear_funct).place(x=900, y=720)
button_random = Button(main_window, text="Random",relief=RAISED,font=('Abadi Bold', 14),bg="#439fe6", fg="white", command=random_funct).place(x=480, y=720)
button_erase = Button(main_window, text="Erase",relief=RAISED,font=('Abadi Bold', 14),bg="#439fe6", fg="white",command=submit_erase_obstacles).place(x=590, y=720)
button_visualize = Button(main_window, text="Visualize",relief=RAISED,font=('Abadi Bold', 14),bg="#439fe6", fg="white", command=visualize_algo).place(x=790, y=720)
main_window.mainloop()
