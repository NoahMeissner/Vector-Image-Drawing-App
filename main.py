from tkinter import *
from Point import Point
from CheckPoints import TriggerPoints
from Draw import Draw
from tkinter import Tk, Menu, Button, Canvas, colorchooser
from Save import Save
from tkinter import filedialog
from Open import OpenFile
from config import PolygonOptions, ObjectTypes


def update_control_point(actual_point, pre_point):
    if pre_point is not None:
        mid_x = int((pre_point.get_x() + actual_point.get_x()) / 2)
        mid_y = int((pre_point.get_y() + actual_point.get_y()) / 2)
        actual_point.set_control_point(mid_x, mid_y)
        return actual_point
    else:
        return actual_point


def update_point(actual_point, list_point):
    identification = actual_point.get_id()
    list_final = []
    for i in range(0, len(list_point)):
        if identification == list_point[i].get_id():
            list_final.append(actual_point)
        else:
            list_final.append(list_point[i])
    return list_final


class GraphicalInterface:

    def __init__(self):
        self.filter = PolygonOptions.full
        self.points = []
        self.control_points = []
        self.root = Tk(className='Vector Painter')
        self.root.geometry("800x600")
        self.edit = False
        self.current_line = None
        self.ls_move = []
        menubar = Menu(self.root)
        self.line_color = 'blue'
        self.polygon_color = 'green'

        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=lambda: self.open_image())
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=lambda: self.save_image())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        color_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Color", menu=color_menu)
        color_menu.add_command(label="Line Color", command=lambda: self.color_chooser(ObjectTypes.Line))
        color_menu.add_command(label="Polygon Color", command=lambda: self.color_chooser(ObjectTypes.Rectangle))

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
        self.add_button_color(self.root)

        button_frame = Frame(self.root)
        button_frame.pack(pady=20)

        self.root.mainloop()

    def on_button_click(self, filter_chosen):
        self.filter = filter_chosen
        self.draw_items()

    def color_chooser(self, obj):
        if ObjectTypes.Line == obj:
            color = self.line_color
        else:
            color = self.polygon_color

        line_chooser = colorchooser.askcolor(title="Choose color", color=color)
        color = line_chooser[1]

        if ObjectTypes.Line == obj:
            self.line_color = color
        else:
            self.polygon_color = color
        self.draw_items()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("JSON", ".json")])
        if file_path:
            Save(self.points, file_path, self.line_color, self.polygon_color)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        try:
            data = OpenFile(file_path)
            self.line_color, self.polygon_color, self.points = data.get_data()
            self.draw_items()

        except Exception as e:
            print("Open Process: " + str(e))

    def edit_mode(self, event):
        print("Edit Mode")
        if self.edit:
            self.edit = False
        else:
            self.edit = True

    def shift_canvas_points(self, dx, dy):
        ls_final = []
        for point in self.points:
            if point.get_control_point() is not None:
                control_point = point.get_control_point()
                coord = control_point.get_coordinates()
                control_point.set_coordinates((coord[0] + dx, coord[1] + dy))
                point.set_control_point(control_point.get_x(), control_point.get_y())
            coord = point.get_coordinates()
            point.set_coordinates((coord[0] + dx, coord[1] + dy))
            ls_final.append(point)
        self.points = ls_final
        self.draw_items()

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

    def clear_canvas(self, event):
        if event is not None:
            self.points = []
            self.draw = Draw(self.canvas)
        self.canvas.delete("all")

    def add_button_color(self, frame):
        # Create a button widget
        button_frame = Frame(frame)
        button_frame.pack(pady=20)

        button_full = Button(button_frame, text="FULL", command=lambda: self.on_button_click(PolygonOptions.full))
        button_vertical = Button(button_frame, text="vertical",
                                 command=lambda: self.on_button_click(PolygonOptions.vertical))
        button_horizontal = Button(button_frame, text="horizontal",
                                   command=lambda: self.on_button_click(PolygonOptions.horizontal))
        button_dot = Button(button_frame, text="Dot", command=lambda: self.on_button_click(PolygonOptions.dot))

        # Place the button in the main window
        button_full.pack(side=LEFT, padx=10)
        button_vertical.pack(side=LEFT, padx=10)
        button_dot.pack(side=LEFT, padx=10)
        button_horizontal.pack(side=LEFT, padx=10)

    def on_x_press(self, event):
        self.clear_canvas(None)
        bol = self.draw.get_draw_control_points()
        if bol:
            self.draw.set_draw_control_points(False)
        else:
            self.draw.set_draw_control_points(True)
        self.draw_canvas(True)

    def on_button_press(self, event):
        trigger = TriggerPoints()
        point_trigger = trigger.painted_points(self.points, (event.x, event.y))
        bezier_trigger = trigger.bezier_points(self.points, (event.x, event.y))
        if bezier_trigger == False and not self.edit:
            current_point = Point(event.x, event.y, len(self.points))
            if len(self.points) >= 1:
                pre_point = self.points[-1]
                mid_x = int((pre_point.get_x() + current_point.get_x()) / 2)
                mid_y = int((pre_point.get_y() + current_point.get_y()) / 2)
                current_point.set_control_point(mid_x, mid_y)

            if point_trigger != False:
                current_point.set_polygon(point_trigger[1])
                coordinates = point_trigger[1].get_coordinates()
                current_point.set_coordinates(coordinates)
            self.points.append(current_point)
            self.draw_canvas(False)

    def draw_canvas(self, bol):
        if bol:
            self.canvas = self.draw.draw_all(self.points, self.line_color, self.polygon_color, self.filter)
        else:
            self.canvas = self.draw.draw(self.points, self.line_color, self.polygon_color, self.filter)

    def on_mouse_drag(self, event):
        trigger = TriggerPoints()
        point_trigger = trigger.painted_points(self.points, (event.x, event.y))
        bezier_trigger = trigger.bezier_points(self.points, (event.x, event.y))

        if bezier_trigger and self.edit:
            pre_point, post_point = bezier_trigger
            post_point.set_control_point(event.x, event.y)
            post_point.set_bezier(True)
            update_point(post_point, self.points)
            self.draw_items()

        if point_trigger and self.edit:
            pre_point, actual_point, post_point = point_trigger
            actual_point.set_coordinates([event.x, event.y])
            if pre_point is not None:
                actual_point = update_control_point(actual_point, pre_point)
                self.points = update_point(actual_point, self.points)
            if post_point is not None:
                post_point = update_control_point(post_point, actual_point)
                self.points = update_point(post_point, self.points)
            self.draw_items()

    def on_button_release(self, event):
        self.current_line = None

    def draw_items(self):
        self.clear_canvas(None)
        self.draw_canvas(True)


if __name__ == '__main__':
    interface = GraphicalInterface()
