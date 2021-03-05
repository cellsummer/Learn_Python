from prettytable import PrettyTable
from scipy.interpolate import interp1d
import math
import itertools
import operator
import numpy as np

# classes
class YieldCurve:
    def __init__(self, par_rates):
        self.par_rates = par_rates
        self.tenors = np.array([0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
        self.last_tenor = 30
        self.tenor_months = 12 * self.tenors
        self.full_tenor_months = np.arange(self.last_tenor * 12 + 1)
        self.key_tenor_months = [0, 3] + list(range(6, self.last_tenor * 12 + 1, 6))

    # Python's Getter
    @property
    def aey_rates(self):
        return YieldCurve.convert_to_aey_rates(self.par_rates)

    # Python's Setter
    @aey_rates.setter
    def aey_rates(self, aey_rates):
        par_rates = YieldCurve.convert_to_par_rates(aey_rates)
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

    def get_key_yield_curve(self):
        """convert the ten point curve to the key rate curve by linear interpolation"""
        temp_par_rates = list(itertools.chain(self.par_rates[0:1], self.par_rates))
        temp_tenor_months = list(itertools.chain([0], self.tenor_months))
        par_rates_interp = interp1d(temp_tenor_months, temp_par_rates)
        key_par_rates = par_rates_interp(self.key_tenor_months)
        return key_par_rates

    def get_key_df(self):
        """calculate the key rate discouting factor using the key yield curve"""
        key_par_rates = self.get_key_yield_curve()
        key_dfs = []
        sum_df = 0
        for rate, tenor in zip(key_par_rates, self.key_tenor_months):
            if tenor > 3:
                key_dfs.append((1 - rate / 2 * sum_df) / (1 + rate / 2))
                sum_df = sum(key_dfs)

        key_dfs.insert(0, pow(1 + key_par_rates[0] / 2, -0.5))
        key_dfs.insert(0, 1.0)
        return key_dfs

    def get_key_fwd_rate(self):
        """calculate the key forward rate using the key yield discounting factors"""
        key_dfs = self.get_key_df()
        key_fwd_rates = []
        for df, df_6, tenor in zip(key_dfs, key_dfs[1:], self.key_tenor_months):
            if 360 > tenor > 3:
                fwd_rate = pow(df / df_6, 2) - 1
                key_fwd_rates.append(fwd_rate)
                # print(f"{tenor}:{df}:{df_6}:{fwd_rate}")
        # cash rate and 3-month rate
        # print(f"cash rate:{cash_rate}")
        key_fwd_rates.insert(0, pow(key_dfs[1] / key_dfs[2], 4) - 1)
        key_fwd_rates.insert(0, pow(key_dfs[0] / key_dfs[1], 4) - 1)
        # extrapolate
        key_fwd_rates.append(key_fwd_rates[-1])
        return key_fwd_rates

    def get_full_fwd_rates(self):
        """calcualte the full forward rates by interpolating key forward rates"""
        key_fwd_rates = self.get_key_fwd_rate()
        full_fwd_rates_interp = interp1d(
            self.key_tenor_months, key_fwd_rates, kind="previous"
        )
        return full_fwd_rates_interp(list(range(361)))

    def get_full_df(self):
        """calcualte the full discounting factors using the full fwd rates"""
        single_mth_df = [pow(1 + fwd, -1 / 12) for fwd in self.get_full_fwd_rates()]
        full_df = list(itertools.accumulate(single_mth_df, operator.mul))
        full_df.insert(0, 1.0)
        return full_df

    def get_full_spot_rates(self):
        """get full spot rates using the full discounting factors"""
        full_dfs = self.get_full_df()
        spot_rates = [
            pow(df, -12 / tenor) - 1
            for df, tenor in zip(full_dfs[1:], self.full_tenor_months[1:])
        ]
        spot_rates.insert(0, None)
        return spot_rates

    def add_spread(self, spread):
        new_par_rates = self.par_rates + spread
        return YieldCurve(new_par_rates)

    # special methods
    def __repr__(self):
        return "YieldCurve({}, tenors = {})".format(self.par_rates, self.tenors)

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
    par_rates_1 = np.loadtxt("yield_curve_01.txt", delimiter=",")
    np.set_printoptions(precision=7)
    print(par_rates_1)
    # # effective_rates = [0.02, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    curve_1 = YieldCurve(par_rates_1)
    print(curve_1.get_full_spot_rates())
    # curve_1.print_yield_curve()
    # # # print(list(itertools.chain(par_rates_1, [par_rates_1[0]])))
    # print(curve_1.get_full_df())
    # print(curve_1.key_tenor_months)
    # print(par_rates_1[2:])

    # x = PrettyTable()
    # for [tenor, df] in zip(curve_1.full_tenor_months, curve_1.get_full_spot_rates()):
    #     x.add_row([tenor, df])
    # x.field_names = ["Tenor", "discount factor"]
    # print(x)


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
