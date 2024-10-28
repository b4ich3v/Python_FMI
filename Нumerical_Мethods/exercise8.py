import sympy as sp

x = sp.symbols('x')
f = 1 / (1 + x)
x0, x1 = 0, 1
point_to_evaluate = 0.75

f_second_derivative = sp.diff(f, x, 2)
f_second_derivative_simplified = sp.simplify(f_second_derivative)

omega = (x - x0) * (x - x1)

def max_f_second_derivative_in_interval():
    critical_points = sp.solveset(sp.diff(f_second_derivative_simplified, x), x, domain=sp.Interval(x0, x1))
    critical_points = list(critical_points) + [x0, x1]
    max_f_second_derivative = max(
        abs(f_second_derivative_simplified.subs(x, point).evalf()) for point in critical_points)
    return max_f_second_derivative

def interpolation_error_at_point(point):
    omega_at_point = abs(omega.subs(x, point).evalf())
    max_f_second_derivative = max_f_second_derivative_in_interval()
    error = max_f_second_derivative / 2 * omega_at_point
    return error

def max_interpolation_error_in_interval():
    x_vals = [x0, 0.5, x1]
    max_omega = max(abs(omega.subs(x, val).evalf()) for val in x_vals)
    max_f_second_derivative = max_f_second_derivative_in_interval()
    max_error = max_f_second_derivative / 2 * max_omega
    return max_error

print(interpolation_error_at_point(point_to_evaluate))
print( max_interpolation_error_in_interval())
