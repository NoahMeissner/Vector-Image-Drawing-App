## Vector Image Drawing App

Draw Simple Vector Graphics with Vector Drawing App. You can use a User Interface to draw Bezier Cuvres, Lines and Polygons. Save and Open filters withe ease for quick adjustments and refinements.
All Functions are self implemented, w

https://github.com/NoahMeissner/Vector-Image-Drawing-App/assets/108337767/5b030321-795a-4c49-b635-ae71a3b3a89a

### Implemenation Details
- Bresenham algorithm to draw lines
- De Casteljau algorithm to create segments of bézier curves
- Flood Fill Algorithm to fill Polygons
- tkinter for various ui elements
- tkinter.create_rectangle to set all pixels individually (no helper functions like create_line)
- numpy to store pixel matrices


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
