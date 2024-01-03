from sympy.abc import x
import sympy as sp
from sympy import sin, cos, tan, cot, sec, csc, asin,acos,atan,acot,asec,acsc


class FxToGx:
    def __init__(self, f_function):
        self.equation = sp.simplify(f_function)
        self.g_function_list = []
        self.sections = self.equation.as_ordered_terms()
        print("Sections are: " + str(self.sections))
        self.g_function_list = self.leave_x_alone(self.equation, self.g_function_list, True)

    def leave_x_alone(self, equation, eq_list, first_time=False):
        sections = equation.as_ordered_terms()
        equation_list = eq_list
        returning_equation_list = []

        for section in sections:
            section_string = str(section)
            local_eq_list = []
            if not first_time:
                diff = equation - section
                for i in range(len(equation_list)):
                    new_eq = equation_list[i] - diff
                    local_eq_list.append(new_eq)
            else:
                dummy_equation = equation - section
                local_eq_list.append(dummy_equation)

            if "x" in section_string:
                section_string, local_eq_list = negativity_inspection(section_string, local_eq_list, first_time)
                section_string, local_eq_list = a_part_inspection(section_string, local_eq_list)
                is_exist, section_string, local_eq_list = trigonometric_inspection(section_string, local_eq_list)
                if is_exist:
                    # if true
                    new_eq = sp.sympify(section_string)
                    local_eq_list = self.leave_x_alone(new_eq, local_eq_list, False)
                else:
                    section_string, local_eq_list = power_inspection(section_string, local_eq_list)
                print(f"{local_eq_list} is added to returning.")
                returning_equation_list.extend(local_eq_list)
            else:
                print(f"Section: {section_string} is just number. It wont be handled by this translator.")

        return returning_equation_list


def negativity_inspection(chosen_section_string, equation_list, first_time=False):
    new_string = chosen_section_string
    # If it is negative it will go as positive to other side
    if chosen_section_string[0] == "-":
        new_string = chosen_section_string[1:]  # remove the negative sign
        if not first_time:
            for i in range(len(equation_list)):
                equation_list[i] = -1 * equation_list[i]
    else:
        if first_time:
            for i in range(len(equation_list)):
                equation_list[i] = -1 * equation_list[i]
    return new_string, equation_list


def a_part_inspection(chosen_section_string, equationlist):
    new_string = chosen_section_string
    index_of_first_star = chosen_section_string.find('*')
    index_of_first_x = chosen_section_string.find('x')
    if index_of_first_star != -1 and index_of_first_star < index_of_first_x:
        # It has a part
        a_part = chosen_section_string[:index_of_first_star]
        try:
            a_part = float(a_part)
        except ValueError:
            return chosen_section_string, equationlist

        for i in range(len(equationlist)):
            equationlist[i] = equationlist[i] / float(a_part)
        new_string = chosen_section_string[index_of_first_star:]
    return new_string, equationlist


def trigonometric_inspection(chosen_section_string, equationlist):
    new_string = chosen_section_string
    last_bracket_index = chosen_section_string.rfind(')')
    is_exist = False

    if last_bracket_index != -1 and last_bracket_index + 1 < len(chosen_section_string):
        # It must have power of something
        new_string, equation_list = power_inspection(chosen_section_string, equationlist)

    if chosen_section_string.find("sin") != -1:
        inside_of_brackets = chosen_section_string[
                             chosen_section_string.find('(') + 1:chosen_section_string.find(')')]
        new_string = inside_of_brackets
        for i in range(len(equationlist)):
            equationlist[i] = asin(equationlist[i])
        is_exist = True

    elif chosen_section_string.find("cos") != -1:
        inside_of_brackets = chosen_section_string[
                             chosen_section_string.find('(') + 1:chosen_section_string.find(')')]
        new_string = inside_of_brackets
        for i in range(len(equationlist)):
            equationlist[i] = acos(equationlist[i])
        is_exist = True

    elif chosen_section_string.find("tan") != -1:
        inside_of_brackets = chosen_section_string[
                             chosen_section_string.find('(') + 1:chosen_section_string.find(')')]
        new_string = inside_of_brackets
        for i in range(len(equationlist)):
            equationlist[i] = atan(equationlist[i])
        is_exist = True

    elif chosen_section_string.find("cot") != -1:
        inside_of_brackets = chosen_section_string[
                             chosen_section_string.find('(') + 1:chosen_section_string.find(')')]
        new_string = inside_of_brackets
        for i in range(len(equationlist)):
            equationlist[i] = acot(equationlist[i])
        is_exist = True

    elif chosen_section_string.find("sec") != -1:
        inside_of_brackets = chosen_section_string[
                             chosen_section_string.find('(') + 1:chosen_section_string.find(')')]
        new_string = inside_of_brackets
        for i in range(len(equationlist)):
            equationlist[i] = asec(equationlist[i])
        is_exist = True

    elif chosen_section_string.find("csc") != -1:
        inside_of_brackets = chosen_section_string[
                             chosen_section_string.find('(') + 1:chosen_section_string.find(')')]
        new_string = inside_of_brackets
        for i in range(len(equationlist)):
            equationlist[i] = acsc(equationlist[i])
        is_exist = True

    return is_exist, new_string, equationlist


def power_inspection(chosen_section_string, equation_list):
    new_string = chosen_section_string
    splitten = chosen_section_string.split("**")
    dummy_equation_list = []
    if len(splitten) != 1:
        power_part = splitten[-1]
        index_of_power_part = chosen_section_string.find(power_part)
        power_part = float(power_part)
        if power_part == "0":
            # It is a constant
            for i in range(len(equation_list)):
                equation_list[i] = 1
        else:
            if power_part % 2 == 0:
                # It is an even power
                for i in range(len(equation_list)):
                    equation_list[i] = equation_list[i] ** (1 / power_part)
                    extra_equation = -1 * equation_list[i]
                    dummy_equation_list.append(extra_equation)
            else:
                # It is an odd power
                for i in range(len(equation_list)):
                    equation_list[i] = equation_list[i] ** (1 / power_part)
            equation_list.extend(dummy_equation_list)
        new_string = chosen_section_string[:index_of_power_part + 2]
    else:
        pass
    return new_string, equation_list


if __name__ == "__main__":
    f_x = x ** 2 - x - 1
    f_x_to_g_x = FxToGx(f_x)
    print(f_x_to_g_x.g_function_list)
