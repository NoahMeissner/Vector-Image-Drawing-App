import matplotlib.pyplot as plt
import numpy as np
def de_casteljau(points, t):
    if len(points) == 1:
        return points[0]
    else:
        new_points = []
        for i in range(len(points) - 1):
            x = (1 - t) * points[i][0] + t * points[i+1][0]
            y = (1 - t) * points[i][1] + t * points[i+1][1]
            new_points.append((x, y))
        return de_casteljau(new_points, t)

# Function to calculate the entire Bézier curve
def bezier_curve(control_points, num_points=100):
    return [de_casteljau(control_points, t) for t in np.linspace(0, 1, num_points)]

points = [(0, 0), (1, 2), (4, 3)]
t = 0.5
point_on_curve = de_casteljau(points, t)

# Calculate the entire Bézier curve
bezier_points = bezier_curve(points)

# Plotting
plt.figure(figsize=(8, 6))

# Plot control points and lines connecting them
control_points = np.array(points)
plt.plot(control_points[:, 0], control_points[:, 1], 'ro-', label='Control Points')

# Plot Bézier curve
bezier_points = np.array(bezier_points)
plt.plot(bezier_points[:, 0], bezier_points[:, 1], 'b-', label='Bézier Curve')

# Highlight the point on the Bézier curve for t
plt.plot(point_on_curve[0], point_on_curve[1], 'go', label=f'Point on Curve (t={t})')

# Labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Bézier Curve using De Casteljau Algorithm')
plt.legend()
plt.grid(True)
plt.show()