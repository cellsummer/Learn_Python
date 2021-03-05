from QuantLib import *

# 1. Date class: useful for defining month end
date = Date(31, 3, 2015)
date_2 = date + Period(2, Months)

print(date_2 - date)
print(date)
print(date + Period(2, Months))

# 2. Calendar class: useful for asset pricing. Calculate business dates
cn_calendar = China()
# excluding weekends and holidays
print(cn_calendar.advance(date, Period(50, Days)))
# normal date operation
print(date + Period(50, Days))

# 3. InterestRate class
annual_rate = 0.05
day_count = Thirty360()
compound_type = Compounded
frequency = Annual
interest_rate = InterestRate(annual_rate, day_count, compound_type, frequency)

print(interest_rate.compoundFactor(Date(31, 12, 2009), Date(31, 12, 2011)))
# print(pow(1 + 0.05 / 12, 12) - 1)

