from tkinter import *
import tkinter as tk
from Point import Point
from enum import Enum
from Check_Trigger_Control_Points import TriggerPoints
from Draw import Draw
from tkinter import Tk, Menu, Button, Canvas
import numpy as np


class Filter(Enum):
    Full = 1,
    Lines = 2,
    ChessBoard = 3,


class Object_Types(Enum):
    Line = 1,
    Rectangle = 2,
    Circle = 3,
    Refresh = 4



class GraphicalInterface:


    def __init__(self):
        self.points = []
        self.control_points = []
        self.root = Tk(className='Vector Painter')
        self.root.geometry("800x600")
        self.edit = False
        menubar = Menu(self.root)

        self.line_color = 'blue'
        self.polygon_color = 'green'

        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=lambda: self.open_image())
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=lambda: self.open_image())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        color_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Color", menu=color_menu)
        color_menu.add_command(label="Choose Color", command=lambda: self.choose_color())

        self.canvas = Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)
        self.draw = Draw(self.canvas)


        # Bind mouse events to methods
        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.root.bind('<KeyPress-x>', self.on_x_press)
        self.root.bind('<KeyPress-e>', self.edit_mode)
        self.root.bind('<KeyPress-c>', self.clear_canvas)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)
        self.canvas.bind('<ButtonRelease-3>', self.move_release)

        self.canvas.bind('<B3-Motion>', self.on_mouse_wheel_button_press)
        self.canvas.bind("<FocusIn>", self.on_focus_in)
        self.ls_move = []

        self.current_line = None

        button_frame = Frame(self.root)
        button_frame.pack(pady=20)



        button_line = Button(button_frame, text="Lines", command=lambda: self.on_button_click(Object_Types.Line))
        button_rectangle = Button(button_frame, text="Rectangle",
                                  command=lambda: self.on_button_click(Object_Types.Rectangle))
        button_circle = Button(button_frame, text="Circle", command=lambda: self.on_button_click(Object_Types.Circle))
        button_refresh = Button(button_frame, text="Refresh",
                                command=lambda: self.on_button_click(Object_Types.Refresh))

        # Place the button in the main window
        button_line.pack(side=LEFT, padx=10)
        button_rectangle.pack(side=LEFT, padx=10)
        button_circle.pack(side=LEFT, padx=10)
        button_refresh.pack(side=LEFT, padx=10)

        self.root.mainloop()

    def edit_mode(self, event):
        if self.edit:
            self.edit = False
        else:
            self.edit = True

    def on_focus_in(self, event):
        self.canvas.focus_set()

    def shift_canvas_points(self, dx, dy):
        ls_final = []
        for point in self.points:
            control_point = None
            if point.get_control_Point() is not None:
                control_point = point.get_control_Point()
                coord = control_point.coordinates()
                control_point.set_coordinates((coord[0] + dx, coord[1] + dy))
                point.set_control_Point(control_point.X(), control_point.Y())
            coord = point.coordinates()
            point.set_coordinates((coord[0] + dx, coord[1] + dy))
            ls_final.append(point)
        self.points = ls_final
        self.clear_canvas(None)
        self.draw_canvas(True)

    def on_mouse_wheel_button_press(self, event):
        if len(self.ls_move) > 1:
            old = self.ls_move[-1]
            self.ls_move.append((event.x, event.y))
            dx = event.x - old[0]
            dy = event.y - old[1]
            self.shift_canvas_points(dx, dy)
        else:
            self.ls_move.append((event.x, event.y))


    def move_release(self, event):
        self.ls_move = []


    #TODO Color Menu noch machen
    def choose_color(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Color Input")
        dialog.geometry("300x200")
        self.add_button_color(dialog)

    def clear_canvas(self, event):
        if event is not None:
            self.points = []
            self.draw = Draw(self.canvas)
        self.canvas.delete("all")

    def add_button_color(self, frame):
        # Create a button widget
        button_frame = Frame(frame)
        button_frame.pack(pady=20)

        button_full = Button(button_frame, text="FULL", command=lambda: self.on_button_click(Filter.Full))
        button_lines = Button(button_frame, text="LINES", command=lambda: self.on_button_click(Filter.Lines))
        button_chess = Button(button_frame, text="CHESS Board", command=lambda: self.on_button_click(Filter.ChessBoard))

        # Place the button in the main window
        button_full.pack(side=LEFT, padx=10)
        button_lines.pack(side=LEFT, padx=10)
        button_chess.pack(side=LEFT, padx=10)

    def on_button_click(self, type):
        if type == Object_Types.Refresh:
            self.clear_canvas(None)
        print(type)

    def on_x_press(self, event):
        print("x press")
        self.clear_canvas(None)
        bol = self.draw.get_draw_control_points()
        if bol:
            self.draw.set_draw_control_points(False)
        else:
            self.draw.set_draw_control_points(True)
        self.draw_canvas(True)


    def on_button_press(self, event):
        radius = 1  # Radius des Punkts
        # Save the starting point
        trigger = TriggerPoints()
        point_trigger = trigger.painted_points(self.points,(event.x, event.y))
        bezier_trigger = trigger.bezier_points(self.points, (event.x, event.y))
        if bezier_trigger == False and not self.edit:
            current_point = Point(event.x, event.y, len(self.points))
            if len(self.points) >= 1:
                pre_point = self.points[-1]
                mid_x = int((pre_point.X() + current_point.X()) / 2)
                mid_y = int((pre_point.Y() + current_point.Y()) / 2)
                current_point.set_control_Point(mid_x, mid_y)
            print(current_point.coordinates())

            if point_trigger != False:
                current_point.set_polygon(point_trigger[1])
                print("Polygon")
            self.points.append(current_point)
            self.draw_canvas(False)
        else:
            print("Bewegen")

    def draw_canvas(self, bol):
        if bol:
            self.canvas = self.draw.draw_all(self.points, self.line_color, self.polygon_color)
        else:
            self.canvas = self.draw.draw(self.points, self.line_color, self.polygon_color)

    def update_point(self, actual_point, list_point):
        id = actual_point.get_id()
        list_final = []
        for i in range(0,len(list_point)):
            if id == list_point[i].get_id():
                list_final.append(actual_point)
            else:
                list_final.append(list_point[i])
        return list_final

    def update_control_point(self, actual_point, pre_point):
        if pre_point is not None:
            mid_x = int((pre_point.X() + actual_point.X()) / 2)
            mid_y = int((pre_point.Y() + actual_point.Y()) / 2)
            actual_point.set_control_Point(mid_x, mid_y)
            return actual_point
        else:
            return actual_point

    def on_mouse_drag(self, event):
        trigger = TriggerPoints()
        point_trigger = trigger.painted_points(self.points, (event.x, event.y))
        bezier_trigger = trigger.bezier_points(self.points, (event.x, event.y))

        if bezier_trigger and self.edit:
            print('Bezier Triggered')
            pre_point, post_point = bezier_trigger
            post_point.set_control_Point(event.x, event.y)
            post_point.set_bezier(True)
            self.update_point(post_point,self.points)
            self.clear_canvas(None)
            self.draw_canvas(True)


        if point_trigger and self.edit:
            pre_point, actual_point, post_point = point_trigger
            actual_point.set_coordinates([event.x, event.y])
            if pre_point is not None:
                actual_point = self.update_control_point(actual_point, pre_point)
                self.points = self.update_point(actual_point, self.points)
            if post_point != None:
                post_point = self.update_control_point(post_point, actual_point)
                self.points = self.update_point(post_point, self.points)
            self.clear_canvas(None)
            self.draw_canvas(True)



    def on_button_release(self, event):
        self.current_line = None


if __name__ == '__main__':
    interface = GraphicalInterface()
