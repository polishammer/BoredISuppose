import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QComboBox


class GraphingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MatLab?")
        self.setGeometry(100, 100, 1200, 800)  # Increased window size

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter equation (e.g., x**2 or sin(x) + cos(y)):", self)
        self.layout.addWidget(self.label)

        self.equation_input = QLineEdit(self)
        self.layout.addWidget(self.equation_input)

        range_layout = QHBoxLayout()

        self.x_range_label = QLabel("X Range (-2 to 2):", self)
        self.x_range_input = QLineEdit("-2,2", self)
        range_layout.addWidget(self.x_range_label)
        range_layout.addWidget(self.x_range_input)

        self.y_range_label = QLabel("Y Range (-2 to 2):", self)
        self.y_range_input = QLineEdit("-2,2", self)
        range_layout.addWidget(self.y_range_label)
        range_layout.addWidget(self.y_range_input)

        self.layout.addLayout(range_layout)

        self.resolution_label = QLabel("Resolution (e.g., 50):", self)
        self.resolution_input = QLineEdit("50", self)
        self.layout.addWidget(self.resolution_label)
        self.layout.addWidget(self.resolution_input)

        self.graph_type_label = QLabel("Select Graph Type:", self)
        self.layout.addWidget(self.graph_type_label)

        self.graph_type_dropdown = QComboBox(self)
        self.graph_type_dropdown.addItems(["2D Contour", "3D Mesh", "Pcolor"])
        self.layout.addWidget(self.graph_type_dropdown)

        self.plot_button = QPushButton("Plot", self)
        self.plot_button.clicked.connect(self.plot_graph)
        self.layout.addWidget(self.plot_button)

        self.figure, self.ax = plt.subplots(figsize=(10, 8))  # Increased figure size
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def plot_graph(self):
        equation = self.equation_input.text()
        graph_type = self.graph_type_dropdown.currentText()

        try:
            x_range = list(map(float, self.x_range_input.text().split(',')))
            y_range = list(map(float, self.y_range_input.text().split(',')))
            resolution = int(self.resolution_input.text())

            x = np.linspace(x_range[0], x_range[1], resolution)
            y = np.linspace(y_range[0], y_range[1], resolution)
            X, Y = np.meshgrid(x, y)

            Z = eval(equation, {"x": X, "y": Y, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp,
                                "log": np.log})

            self.figure.clear()
            if graph_type == "2D Contour":
                self.ax = self.figure.add_subplot(111)
                cp = self.ax.contourf(X, Y, Z, cmap='viridis')
                self.figure.colorbar(cp)
                self.ax.set_xlabel("X")
                self.ax.set_ylabel("Y")
            elif graph_type == "3D Mesh":
                from mpl_toolkits.mplot3d import Axes3D
                self.ax = self.figure.add_subplot(111, projection='3d')
                self.ax.plot_surface(X, Y, Z, cmap='viridis')
                self.ax.set_xlabel("X")
                self.ax.set_ylabel("Y")
                self.ax.set_zlabel("Z")
            elif graph_type == "Pcolor":
                self.ax = self.figure.add_subplot(111)
                pc = self.ax.pcolormesh(X, Y, Z, shading='auto', cmap='viridis')
                self.figure.colorbar(pc)
                self.ax.set_xlabel("X")
                self.ax.set_ylabel("Y")

            self.canvas.draw()
        except Exception as e:
            self.label.setText(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphingApp()
    window.show()
    sys.exit(app.exec_())
