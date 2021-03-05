import numpy as np
import math
from prettytable import PrettyTable
import pandas as pd

from yield_curve import YieldCurve
from enum import Enum, unique


@unique
class Frequency(Enum):
    Annual = 1
    Semi_Annual = 2
    Quarterly = 4
    Monthly = 12


class BondFeatures:
    def __init__(self, tenor, coupon_rate, coupon_freq=Frequency.Semi_Annual):
        self.tenor = tenor
        self.coupon_freq = coupon_freq
        self.coupon_rate = coupon_rate

    def __repr__(self):
        return f"BondFeatures(tenor = {self.tenor}, coupon = {self.coupon_rate:.3f}, coupon_freq = {self.coupon_freq})"

    __str__ = __repr__


class InforceVolume:
    def __init__(self, notional, book_value, market_value):
        self.notional = notional
        self.book_value = book_value
        self.market_value = market_value

    def __repr__(self):
        return f"InforceVolume(notional = {self.notional}, book_value = {self.book_value}, market_value = {self.market_value})"

    __str__ = __repr__


class BondAssumptions:
    pass


class Bond:
    def __init__(self, features, inforce, assumptions):
        assert isinstance(features, BondFeatures), "Wrong bond features argument!"
        assert isinstance(inforce, InforceVolume), "Wrong bond inforce volume argument!"
        assert isinstance(
            assumptions, BondAssumptions
        ), "Wrong bond assumptions argument!"

        self.features = features
        self.assumptions = assumptions
        self.inforce = inforce

    def __repr__(self):
        return f"Bond(features = {self.features}, assumptions = {self.assumptions}, inforce = {self.inforce})"

    __str__ = __repr__

    @property
    def tenor(self):
        return self.features.tenor

    @property
    def par_value(self):
        return self.inforce.notional

    @property
    def coupon_rate(self):
        return self.features.coupon_rate

    @property
    def coupon_freq(self):
        return self.features.coupon_freq

    @property
    def maturity_amnt(self):
        return self.par_value

    @property
    def coupon_amnt(self):
        return self.par_value * self.coupon_rate / self.coupon_freq.value / 100

    def calc_market_vals(self, yield_curve, pivot_mth=0):
        # assert isinstance(yield_curve, YieldCurve) 'Wrong yield_curve input in calc_market_vals'
        pass

    def illustration(self):
        """cashflow illustration"""
        cfs = self.calc_pricing_cfs()
        self.print_as_table(cfs)
        return

    def calc_pricing_cfs(self, yrs_to_project=None):
        """calculate the pricing/projection cashflows, returns a dataframe"""
        if yrs_to_project is None:
            yrs_to_project = self.tenor

        mths_to_project = int(yrs_to_project * 12)

        mths = np.arange(mths_to_project + 1)
        # asset core cashflows
        coupons = self.coupon_amnt * (
            (mths % (12 / self.coupon_freq.value) == 0)
            & (mths <= self.tenor * 12)
            & (mths > 0)
        )
        maturity = self.maturity_amnt * (mths == (self.tenor * 12))
        asset_inflows = coupons + maturity
        asset_outflows = np.zeros(mths_to_project + 1)

        # use column oriented data structures for populating the datframe
        cfs = {}
        cfs["pol_m"] = mths
        cfs["coupons"] = coupons
        cfs["maturity"] = maturity
        cfs["asset_inflows"] = asset_inflows
        cfs["asset_outflows"] = asset_outflows

        return_columns = [
            "pol_m",
            "coupons",
            "maturity",
            "asset_inflows",
            "asset_outflows",
        ]

        results = pd.DataFrame(data=cfs, columns=return_columns)

        return results

    def pivot_cfs(self, pivot_mth, yrs_to_project=None):
        """calculate the pricing/projection cashflows as of pivot date, returns a dataframe"""

        if yrs_to_project is None:
            yrs_to_project = self.tenor - pivot_mth / 12

        mths_to_project = int(yrs_to_project * 12)

        proj_mths = np.arange(mths_to_project + 1)
        cfs = self.calc_pricing_cfs(pivot_mth / 12 + yrs_to_project)
        pivot_cfs = cfs.loc[cfs.pol_m >= pivot_mth].copy()
        # print(type(pivot_cfs))
        pivot_cfs.insert(0, "proj_m", proj_mths, True)
        return pivot_cfs

    @staticmethod
    def print_as_table(data, columns=None):
        assert isinstance(
            data, pd.DataFrame
        ), "Wrong data format in print_as_table(data, columns = None)"

        if columns is None:
            columns = data.columns

        x = PrettyTable()
        x.field_names = columns
        for row in data.itertuples(index=False):
            x.add_row(row)
        print(x)
        return


def main():
    bond_features_1 = BondFeatures(10, 3.5)
    bond_inforce_1 = InforceVolume(1_000, 1_000, 1_000)
    assumptions_null = BondAssumptions()
    print(bond_features_1)
    # print(isinstance(bond_features_1, BondFeatures))
    print(bond_inforce_1)
    bond_1 = Bond(bond_features_1, bond_inforce_1, assumptions_null)
    # print(bond_1)
    # print(f"the par value of this bond is {bond_1.par_value}")
    # print(f"the payment frequency of this bond is {bond_1.coupon_freq}")
    # # print(float(Frequency.Semi_Annual.value))
    # print(f"the coupon amount of this bond for each payment is {bond_1.coupon_amnt}")
    # print(bond_1.calc_pricing_cfs(10))
    bond_1.illustration()
    bond_1.print_as_table(bond_1.pivot_cfs(pivot_mth=12, yrs_to_project=20))


if __name__ == "__main__":
    main()
