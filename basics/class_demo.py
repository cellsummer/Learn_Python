from prettytable import PrettyTable
import math

# import numpy as np

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
class Yield_curve:
    def __init__(self, par_rates, tenors=[0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]):
        self.par_rates = par_rates
        self.tenors = tenors
        # self.aey_rates = Yield_curve.convert_to_aey_rates(self.par_rates)
        # if len(self.par_rates) != len(self.tenors):
        #     print("the length of the rates is incosistent with the shape of the curve.")

    # Python's Getter
    @property
    def aey_rates(self):
        return Yield_curve.convert_to_aey_rates(self.par_rates)

    # Python's Setter
    @aey_rates.setter
    def aey_rates(self, aey_rates):
        par_rates = Yield_curve.convert_to_par_rates(aey_rates)
        self.par_rates = par_rates

    # regular method: the first argument is always self (the instance)
    def print_yield_curve(self):
        x = PrettyTable()
        x.field_names = ["Tenor", "BEY Rate"]
        for [tenor, rate] in zip(self.tenors, self.par_rates):
            x.add_row([tenor, rate])
        print(x)

    def print_yield_curve_AEY(self):
        x = PrettyTable()
        x.field_names = ["Tenor", "AEY Rate"]
        for [tenor, rate] in zip(self.tenors, self.par_rates):
            aey_rate = math.pow(1 + 0.5 * rate, 2) - 1
            x.add_row([tenor, aey_rate])
        print(x)

    def add_spread(self, spread):
        new_par_rates = self.par_rates + spread
        return Yield_curve(new_par_rates)

    # special methods
    def __repr__(self):
        return "Yield_curve({}, tenors = {})".format(self.par_rates, self.tenors)

    def __str__(self):
        return "{}".format(self.par_rates)

    def __len__(self):
        return len(self.par_rates)

    # class method: the first argument is always cls (the class)
    # class method is often used as alternative constructor
    @classmethod
    def from_effective_rates(
        cls, effective_rates, tenors=[0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
    ):
        par_rates = []
        for rate in effective_rates:
            par_rate = 2 * (math.pow(1 + rate, 0.5) - 1)
            par_rates.append(par_rate)
        return cls(par_rates)

    # static method: the method doesn't use instance or class
    @staticmethod
    def convert_to_par_rates(effective_rates):
        par_rates = []
        for rate in effective_rates:
            par_rate = 2 * (math.pow(1 + rate, 0.5) - 1)
            par_rates.append(par_rate)
        return par_rates

    @staticmethod
    def convert_to_aey_rates(par_rates):
        aey_rates = []
        for rate in par_rates:
            aey_rate = math.pow(1 + rate / 2, 2) - 1
            aey_rates.append(aey_rate)
        return aey_rates


def main():
    par_rates_1 = [0.02, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    # effective_rates = [0.02, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    curve_1 = Yield_curve(par_rates_1)
    print(curve_1)
    curve_1.print_yield_curve()


if __name__ == "__main__":
    main()

# # spread = 0.01
# # curve_1_aft_spread = curve_1.add_spread(spread)
# # curve_1_aft_spread.print_yield_curve()

# # print(curve_1_aft_spread.aey_rates)
# curve_1.aey_rates = effective_rates
# curve_1.print_yield_curve()

# # setattr / getattr to set and get the class attributes dynamically
# print(getattr(curve_1, "aey_rates"))
