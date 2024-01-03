import sympy as sp
from sympy import sin, cos, tan, cot, sec, csc, asin,acos,atan,acot,asec,acsc
import numpy as np
from sympy.abc import x
from fixed_point import FixedPointIteration

if __name__ == "__main__":
    # Example use case for FixedPointIteration.
    f_x = x ** 2 - x - 1
    initial_guess = 1.6
    tol = 1e-10
    max_iter = 100
    fpi = FixedPointIteration(f_x, initial_guess, tol, max_iter)
    print(fpi.converge_able_g_functions)
    for g_object in fpi.converge_able_g_functions:
        g_object.print_iteration_list()
        g_object.plot_iteration()
