import pandas as pd
import matplotlib.pyplot as plt


df_house = pd.read_csv("Data.csv")
df_house.columns = ['link', 'location', 'area', 'room', 'year', 'price']


room_number = sorted(set(df_house['room'][df_house['room'] < 8]))

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