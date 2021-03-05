import itertools

# import class_demo as yc
import operator

counter = itertools.count()

# don't use counter, use next(counter) instead
# print(next(counter))

switch = itertools.cycle(["On", "Off"])

repeat = itertools.repeat(2)

# map takes arguments as iterables
squares = map(pow, range(10), repeat)
# itertools.starmap takes arguments as list of tuples
squares = itertools.starmap(pow, [(0, 2), (1, 2), (3, 2)])

# print(list(squares))
# print(next(switch))
# print(next(switch))
# print(next(switch))

# par_rates_1 = [0.02, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
# curve_1 = yc.Yield_curve(par_rates_1)

# print(list(zip(counter, par_rates_1)))


def discount_df(x, df):
    pv_sum = 0
    pvs = itertools.starmap(operator.mul, zip(x, df))
    pv_sum = sum(pvs)
    return pv_sum


def discount_spot(x, rates, months):
    pv_sum = 0
    df = [pow(1 + rate, -month / 12) for (rate, month) in zip(rates, months)]
    pv_sum = discount_df(x, df)

    return pv_sum


def get_spot_rates(fwd_rates, months):
    months_start = itertools.chain([0], months)
    months_delta = [
        month - month_start for (month, month_start) in zip(months, months_start)
    ]
    accum_factors_period = [
        pow(1 + fwd_rate, month_delta / 12)
        for (fwd_rate, month_delta) in zip(fwd_rates, months_delta)
    ]
    accum_factors = itertools.accumulate(accum_factors_period, operator.mul)
    spot_rates = [
        pow(accum_factor, 12 / month) - 1
        for (accum_factor, month) in zip(accum_factors, months)
    ]
    return spot_rates


def discount_fwd(x, rates, months):
    spot_rates = get_spot_rates(rates, months)
    pv_sum = discount_spot(x, spot_rates, months)
    return pv_sum


cashflows = [100, 200, 300]
df = [0.9, 0.8, 0.7]
rates = [0.04, 0.03, 0.06]
t = [12, 24, 48]

# pv = discount(cashflows, df)
# pv = discount(cashflows, rates, t)
# print(pv)

print(discount_spot(cashflows, rates, t))
print(discount_fwd(cashflows, rates, t))
# for item in pv:
#     print(item)
