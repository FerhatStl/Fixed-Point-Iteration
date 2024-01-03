import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from sympy.abc import x


class g_func:
    def __init__(self, f_function, g_function):
        self.f_x = f_function
        self.g_function = g_function
        self.iteration_list = []

    def add_to_iteration_list(self, root, error):
        self.iteration_list.append([root, error])

    def get_root_list(self):
        root_list = []
        for iteration in self.iteration_list:
            root_list.append(float(iteration[0]))
        return root_list

    def get_iteration_list(self):
        return self.iteration_list

    def print_iteration_list(self):
        for i in range(len(self.iteration_list)):
            print(f"iteration {i+1}: Root = {self.iteration_list[i][0]} Error = {self.iteration_list[i][1]}")

    def plot_iteration(self):
        root_list = self.get_root_list()
        # Create a function from the sympy expression

        f = sp.lambdify(x, self.f_x)
        # Create a range of x values for plotting the function
        x_vals = np.linspace(float(min(root_list)) - 5, float(max(root_list)) + 5, 1000)
        y_vals = f(x_vals)
        # Create a list of y values corresponding to the roots
        y_roots = [f(x) for x in root_list]
        # Plot the function
        plt.plot(x_vals, y_vals, label='f(x)', color='blue')
        # Plot the roots
        plt.scatter(root_list, y_roots, label='Iteration Points', color='red')

        # Add labels, title and legend
        plt.title("Fixed Point Iteration")
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()

        # Show the plot
        plt.show()

