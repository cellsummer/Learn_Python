import matplotlib as mpl
from matplotlib import pyplot as plt
from yield_curve import YieldCurve

# from prettytable import PrettyTable


def main():
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
    # effective_rates = [0.02, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    curve_1 = YieldCurve(par_rates_1)
    # print(curve_1)
    # curve_1.print_yield_curve()
    # # print(list(itertools.chain(par_rates_1, [par_rates_1[0]])))
    # print(curve_1.get_full_df())
    # print(curve_1.key_tenor_months)

    tenors_x = curve_1.full_tenor_months
    # print(len(x))
    spot_y = curve_1.get_full_spot_rates()
    fwd_y = curve_1.get_full_fwd_rates()
    # print(len(y))

    # fig, ax = plt.subplots()
    # ax.plot(x, y, color="C1")

    # fig.savefig("fig.pdf")
    # fig.show()
    print(plt.style.available)
    # plt.style.use("seaborn-notebook")
    plt.xkcd()
    plt.plot(tenors_x, spot_y, label="spot rates")
    plt.plot(tenors_x, fwd_y, label="forward rates")

    plt.legend()

    plt.show()

    # x = PrettyTable()
    # for [tenor, df] in zip(curve_1.full_tenor_months, curve_1.get_full_spot_rates()):
    #     x.add_row([tenor, df])
    # x.field_names = ["Tenor", "discount factor"]
    # print(x)


if __name__ == "__main__":
    main()
