import matplotlib.pyplot as plt
import pandas as pd

p = [
    [int(input("ENTER X1: ")), int(input("ENTER Y1:"))],
    [int(input("ENTER X2: ")), int(input("ENTER Y2:"))]
    ]
dx = -(p[0][0]-p[1][0])
dy = -(p[0][1]-p[1][1])
step = 0
x = [p[0][0]]
y = [p[0][1]]
x_ = x[0]
y_ = y[0]
if abs(dx) > abs(dy):
    step = abs(dx)
else:
    step = abs(dy)

m = dy/dx

for i in range(step):
    x_ = (x_ + (dx/step))
    x.append(round(x_))
    y_ = (y_ + (dy/step))
    y.append(round(y_))

xy_table = pd.DataFrame({'x': x, 'y':y})
plt.title("Line Drawn From DDA algorithm")
plt.plot(x, y)