import sympy as sp
from sympy import sin, cos, tan, cot, sec, csc, asin,acos,atan,acot,asec,acsc
from sympy.abc import x
from fx_to_gx import FxToGx
from G_Func import g_func


class FixedPointIteration:
    def __init__(self, f_function, x0: float, tol=1e-8, max_iter=100):
        self.f_x = f_function
        self.initial_guess = x0
        self.tol = tol
        self.max_iter = max_iter
        self.possible_g_x_list = FxToGx(self.f_x).g_function_list
        self.converge_able_g_functions = []
        self.actual_roots = sp.solve(self.f_x, x)
        print(f"Actual roots are: {self.actual_roots}")
        for i in range(len(self.actual_roots)):
            if self.actual_roots[i].is_real:
                self.actual_roots[i] = float(self.actual_roots[i])
            else:
                complex_num = complex(self.actual_roots[i])
                self.actual_roots[i] = str(f"{complex_num.real}{complex_num.imag}i")
                print(self.actual_roots[i])

        for g_function in self.possible_g_x_list:
            g_object = g_func(f_function, g_function)
            converge_ability = self.iteration(g_object)
            if converge_ability:
                self.converge_able_g_functions.append(g_object)
            else:
                pass

    def iteration(self, g_object):
        g_function = g_object.g_function
        iteration = 0
        error = self.tol + 1
        root = self.initial_guess

        while error > self.tol and iteration < self.max_iter:
            g_object.add_to_iteration_list(root, error)
            x_next = g_function.evalf(subs={x: root})  # x_(n+1)=g(x_n)
            if error > x_next:
                return False
            error = abs(abs(x_next) - abs(root))  # |x_n-x_(n-1)|
            root = x_next  # x_n
            iteration += 1
            if abs(self.f_x.subs(x, root)) < self.tol:
                # Found a root
                break

        if iteration == self.max_iter:
            # Did not converge
            return False
        return True


if __name__ == "__main__":
    f_x = x**2 - x - 1
    initial_guess = 1.6  # Initial guess for the root
    fpi = FixedPointIteration(f_x, initial_guess, 1e-10, 100)
    for g_object in fpi.converge_able_g_functions:
        g_object.print_iteration_list()
        g_object.plot_iteration()
