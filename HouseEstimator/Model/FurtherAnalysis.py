import os

import pandas as pd
import matplotlib.pyplot as plt
import os


df_house = pd.read_csv("Data.csv")
df_house.columns = ['link', 'location', 'area', 'room', 'year', 'price']

# print(os.getcwd())

room_number = sorted(set(df_house['room'][df_house['room'] < 8]))
tenyears = sorted(set(df_house['year'][df_house['year'] % 4 == 0]))
allyears = sorted(set(df_house['year'][(1370 < df_house['year']) & (df_house['year'] < 1400)]))

# prices = [list((df_house['price'][df_house['room'] == _class]/100000000000)) for _class in room_number]
# plt.figure()
# plt.title('Boxplot of Price base on room number')
# plt.boxplot(prices, labels=room_number)
# plt.ylabel("for real 'price' multiply to 10000000000")
# plt.show()

# areas = [list((df_house['area'][df_house['room'] == _class])) for _class in room_number]
# plt.figure()
# plt.title('Boxplot of Area base on room number')
# plt.boxplot(areas, labels=room_number)
# plt.ylabel("Area")
# plt.show()


# prices = [list((df_house['price'][df_house['year'] == _class]/100000000000)) for _class in tenyears]
# plt.figure()
# plt.title('Boxplot of Price base on year')
# plt.boxplot(prices, labels=tenyears)
# plt.ylabel("price")
# plt.show()

# plt.figure()
# plt.title("Hist of year")
# plt.hist(df_house['year'], bins=40)
# plt.ylabel("frequncy")
# plt.xlabel("year")
# plt.show()


# plt.figure()
# plt.title("Hist of location")
# plt.hist(df_house['location'], bins=50, color='y')
# plt.ylabel("frequncy")
# plt.xlabel("location")
# plt.show()

# plt.figure()
# plt.title("area VS price")
# plt.scatter(df_house["area"], df_house["price"])
# plt.xlabel("area")
# plt.ylabel("price")
# plt.show()

# plt.figure()
# plt.title("year VS price")
# plt.scatter(df_house["year"], df_house["price"], color='r')
# plt.xlabel("year")
# plt.ylabel("price")
# plt.show()


# pricelist = [((df_house['price'][df_house['year'] == _class].max()
#                - (df_house['price'][df_house['year'] == _class].min()), _class)) for _class in allyears]
#
#
# pricesince = []
# yearsince = []
#
# for _tuple in pricelist:
#     pricesince.append(_tuple[0])
#     yearsince.append(_tuple[1])
#
# plt.figure()
# plt.title("price changes since 1370 with their (max - min)")
# plt.plot(yearsince, pricesince)
# plt.xlabel('year')
# plt.ylabel('price')
# plt.show()


# pricelist2 = [(df_house['price'][df_house['year'] == _class].mean()/1000000000, _class) for _class in allyears]
#
# pricesince = []
# yearsince = []
#
# for _tuple in pricelist2:
#     pricesince.append(_tuple[0])
#     yearsince.append(_tuple[1])
#
# plt.figure()
# plt.title("price changes since 1370 with their average")
# plt.plot(yearsince, pricesince, c='g')
# plt.xlabel('year')
# plt.ylabel('for real price multiply to 1000000000')
# plt.show()
