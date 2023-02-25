import cv2
import numpy as np

lower = [4, 150, 150]
upper = [6, 179, 255]

for h in range(lower[0], upper[0] + 1):
    for s in range(lower[1], upper[1] + 1, 10):
        for v in range(lower[2], upper[2] + 1, 10):
            color = np.array([h, s, v])
            colors = np.zeros((400, 400, 3), dtype = np.uint8)
            height = len(colors)
            width = len(colors[0])
            for y in range(height):
                for x in range(width):
                    colors[y][x][0] = color[0]
                    colors[y][x][1] = color[1]
                    colors[y][x][2] = color[2]

            colors = cv2.cvtColor(colors, cv2.COLOR_HSV2BGR)
            text = str(h) + ', ' + str(s) + ', ' + str(v)
            cv2.imshow('color', colors)
            print(text)
            cv2.waitKey(1)