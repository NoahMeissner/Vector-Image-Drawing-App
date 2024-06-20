## Vector Image Drawing App

Draw Simple Vector Graphics with Vector Drawing App. You can use a User Interface to draw Bezier Cuvres, Lines and Polygons. Save and Open filters withe ease for quick adjustments and refinements.
All Functions are self implemented, w

https://github.com/NoahMeissner/Vector-Image-Drawing-App/assets/108337767/5b030321-795a-4c49-b635-ae71a3b3a89a

### Implemenation Details
**Bresenham's Algorithm:**
- Used to draw lines by setting individual pixels in a straight path between two points with integer coordinates.
- This algorithm ensures efficient and accurate rendering of lines, avoiding floating-point arithmetic.
**De Casteljau's Algorithm:**
- Employed to create segments of Bézier curves, which are used for smooth and scalable curve generation.
- This recursive algorithm constructs Bézier curves by iteratively subdividing control points.
**Flood Fill Algorithm:**
- Applied to fill polygons or areas with a specified color by setting each pixel inside the boundary.
- This algorithm is commonly used in paint programs and for boundary-defined color filling.
**Tkinter for UI Elements:**
- Tkinter is utilized to create and manage various user interface elements such as buttons, labels, and canvases.
- This Python library allows for the creation of interactive and graphical applications.
**Tkinter create_rectangle for Pixel Manipulation:**
- Tkinter's create_rectangle method is used to set pixels individually to draw shapes and lines.
- Unlike higher-level drawing functions like create_line, create_rectangle can be used to set each pixel's color manually.
**NumPy for Pixel Matrices:**
- NumPy is used to store and manipulate pixel matrices efficiently.
- This library provides a convenient and powerful way to handle large arrays of pixel data for image processing.



### Control
- Left Click: Draw Points
- Press E: Switch to Edit Mode
- Press X: Hide Control Points
- Press C: Refresh Canvas

### Usage:
**Graphical Interface**: 
```
python3 main.py
```


### Installation
```
pip install tkinter

pip install numpy
```
