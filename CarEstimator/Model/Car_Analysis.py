from sklearn import preprocessing
import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestClassifier


df = pd.read_csv('CarData.csv')
df = df.dropna()
df = df[df['mileage'] != '-']
df['mileage'] = df['mileage'].astype('int')
df['price'] = df['price'].astype('int')
records = df[['brand','model','mileage','year','body_status','price']].values
# # print(len(records))
le = preprocessing.LabelEncoder()
x, y = records[:, 0:5], records[:, 5]
# print(x,y)
brand = [s[0] for s in x]
le.fit(brand)
for i in range(len(x)):
    x[i][0] = (le.transform([x[i][0]]))[0]
model = [s[1] for s in x]
le.fit(model)
for i in range(len(x)):
    x[i][1] = (le.transform([x[i][1]]))[0]
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
y_train = y_train.astype('int')
rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)
rf.fit(X_train, y_train)
y_predictions = rf.predict(X_test)
print("R-squared :", r2_score(y_test, y_predictions))
name = "carestimator.pkl"
name1 = "car_lableencoder.pkl"
# print(reg.predict(np.array([32, 99, 1, 1395]).reshape(1, -1)))

with open(name, 'wb') as file:
    pickle.dump(rf, file)

with open(name1, 'wb') as file:
    pickle.dump(le, file)