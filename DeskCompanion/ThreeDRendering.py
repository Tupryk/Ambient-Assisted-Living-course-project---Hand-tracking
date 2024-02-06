import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection


class Renderer:
    def __init__(self):
        plt.ion()  # Turn on interactive mode
        self.fig = plt.figure(figsize=(6,6))
        self.ax = self.fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1, frameon=False)

    def draw(self, T):

        collection = PolyCollection(T, closed=True, linewidth=0.1,
                                facecolor="None", edgecolor="black")
        self.ax.clear()
        self.ax.add_collection(collection)
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        plt.pause(0.001)


def rotatePoint(x, y, z, points):
    rotX = np.array([
        [1., 0., 0.],
        [0., np.cos(x), np.sin(x)],
        [0., -np.sin(x), np.cos(x)]
    ])
    rotY = np.array([
        [np.cos(y), 0., -np.sin(y)],
        [0., 1., 0.],
        [np.sin(y), 0., np.cos(y)],
    ])
    rotZ = np.array([
        [np.cos(z), np.sin(z), 0.],
        [-np.sin(z), np.cos(z), 0.],
        [0., 0., 1.],
    ])
    return np.dot(np.dot(np.dot(points, rotX), rotY), rotZ)


class Mesh:
    def __init__(self, file_path: str="./files/poke.obj"):
        V, F = [], []
        with open(file_path) as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                values = line.split()
                if not values:
                    continue
                if values[0] == 'v':
                    V.append([float(x) for x in values[1:4]])
                elif values[0] == 'f':
                    face_indices = []
                    for face_value in values[1:]:
                        # Process each face value to extract the vertex index
                        vertex_index = int(face_value.split('/')[0]) - 1  # Extracting only the vertex index
                        face_indices.append(vertex_index)
                    F.append(face_indices)
        V, self.faces = np.array(V), np.array(F)
        V = (V-(V.max(0)+V.min(0))/2) / max(V.max(0)-V.min(0))

        self.original_V = V.copy()

    def rotate(self, angles):
        V = rotatePoint(*angles, self.original_V)
        T = V[self.faces][...,:2]
        return T
    
    def updateRotation(self, angles):
        V = rotatePoint(*angles, self.original_V)
        self.original_V = V


