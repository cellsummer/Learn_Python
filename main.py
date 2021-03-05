from prettytable import PrettyTable
import matplotlib.pyplot as plt
import scipy.interpolate
from yield_curve import YieldCurve
import pandas as pd
import os
import sys

# functions
# positional arguments and keyword arguments


# def student_info(*args, **kwargs):
#     print(args)
#     print(kwargs)


# course = ["Math", "Art"]
# info = {"name": "John", "age": 22}

# print(*course)
# # wrong way of using this function
# # student_info(course, info)
# # */** will unpack the list/tuple, and dictionaries
# student_info(*course, **info)

# classes
# class Yield_curve:
#     def __init__(self, par_rates, tenors=[0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]):
#         self.par_ratesdt = par_ratesdt
#         self.tenors = tenors
#         if len(self.par_ratesdt) != len(self.tenors):
#             print("the length of the rates is incosistent with the shape of the curve.")

#     def print_yield_curve(self):
#         x = PrettyTable()
#         x.field_names = ["Tenor", "Rate"]
#         for [tenor, rate] in zip(self.tenors, self.par_rates):
#             x.add_row([tenor, rate])
#         print(x)
#
par_rates_1 = [
    0.0421,
    0.0437,
    0.0451,
    0.0469,
    0.0480,
    0.0506,
    0.0534,
    0.0552,
    0.0591,
    0.0624,
]
tenors = [3, 6, 12, 24, 36, 60, 84, 120, 240, 360]
curve_1 = YieldCurve(par_rates_1)
curve_1.print_yield_curve()
df = pd.DataFrame(
    zip(curve_1.key_tenor_months, curve_1.get_key_fwd_rate()),
    columns=["Tenor", "Rates"],
)
print(df)

key_fwd_rates = curve_1.get_key_fwd_rate()
key_tenors = curve_1.key_tenor_months

plt.style.use("seaborn")

fig, axs = plt.subplots(1, 2, sharey=True)

axs[0].plot(tenors, par_rates_1, label="par rates", color="C4", marker="X")
axs[0].legend()
axs[1].plot(key_tenors, key_fwd_rates, label="key fwd rates")
axs[1].legend()
plt.show()

# name = "Joe"
# gender = "male"

# print(f"{name} is a {gender}")
# par_rates_interp = scipy.interpolate.interp1d(tenors, par_rates_1)
# # full_par_rates = [par_rates_interp(month) for month in range(3, 361)]
# full_par_rates = par_rates_interp(range(3, 361))
# print(full_par_rates)
# # print(par_rates_interp(4))

