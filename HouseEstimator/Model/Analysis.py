from sklearn import preprocessing
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


df = pd.read_csv('Data.csv')
df.columns = ['link', 'location', 'area', 'room', 'year', 'price']
df = df.dropna()
records = df.values
print(len(records))
le = preprocessing.LabelEncoder()
x, y = records[:, 1:5], records[:, 5]
locations = [s[0] for s in x]
le.fit(locations)
for i in range(len(x)):
    x[i][0] = (le.transform([x[i][0]]))[0]
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
reg = LinearRegression()
reg.fit(X_train, y_train)
y_predictions = reg.predict(X_test)
print("R-squared :", r2_score(y_test, y_predictions))

name = "houseestimator.pkl"
print(reg.predict(np.array([32, 99, 1, 1395]).reshape(1, -1)))

with open(name, 'wb') as file:
    pickle.dump(reg, file)