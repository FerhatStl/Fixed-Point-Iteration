import numpy as np
from flask import Flask, request, render_template
import sympy as sp
from sympy.abc import x
from fixed_point import FixedPointIteration

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        f_x = sp.sympify(request.form['f_x'])
        initial_guess = float(request.form['initial_guess'])
        tol = float(request.form['tol'])
        max_iteration = int(request.form['max_iteration'])

        fpi = FixedPointIteration(f_x, initial_guess, tol, max_iteration)
        g_objects = fpi.converge_able_g_functions
        actual_roots = fpi.actual_roots
        possible_g_x_list = fpi.possible_g_x_list
        found_root = g_objects[-1].get_root_list()[-1] if g_objects else None

        sections = []
        for g_object in g_objects:
            # Get the data for the plot
            root_list = g_object.get_root_list()
            f = sp.lambdify(x, f_x)
            x_values = np.linspace(float(min(root_list)) - 5, float(max(root_list)) + 5, 1000)
            y_values = f(x_values)
            y_roots = [f(root) for root in root_list]

            # Create a section
            section = {
                'g_function': str(g_object.g_function),
                'iteration_list': g_object.iteration_list,
                'x_values': x_values.tolist(),
                'y_values': y_values.tolist(),
                'root_list': root_list,
                'y_roots': y_roots
            }
            sections.append(section)

        return render_template('main_page.html', sections=sections, actual_roots=actual_roots,
                               possible_g_x_list=possible_g_x_list, found_root=found_root)

    return render_template('main_page.html')


if __name__ == "__main__":
    app.run(debug=True)
