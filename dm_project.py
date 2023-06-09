# -*- coding: utf-8 -*-
"""dm_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yDtycXFT55PhFf3zz44hoOlvoaLLGO0c

Importing Libraries
"""

import numpy as n
import pandas as pd
from matplotlib import pyplot as plt 
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report,confusion_matrix,roc_curve, auc,RocCurveDisplay

from google.colab import drive
drive.mount('/content/gdrive')

"""Read the dataset"""

d=pd.read_csv("/content/gdrive/My Drive/Data_Mining/train_data.csv")
d.info()

d.describe()

"""Finding correlations between features with target attribute"""

correlation=d.corr()
plt.figure(figsize=(6,6),facecolor="pink")
abs(correlation['price_range']).sort_values(ascending=True)[:-1].plot.barh()
plt.title('Correlation between Price range and other columns',fontsize=25)
plt.show()

"""DATA PREPROCESSING"""

d = d.drop(['clock_speed','n_cores','m_dep'], axis = 1)

d.info()

df = pd.DataFrame(d, columns=['battery_power', 'blue', 'dual_sim', 'fc', 'four_g', 'int_memory', 'mobile_wt', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi', 'price_range'])

import seaborn as sns
sns.set(style="white")
corr = df.corr()
mask = n.triu(n.ones_like(corr, dtype=bool))
f, ax = plt.subplots(figsize=(16, 6))
cmap = sns.diverging_palette(230, 20, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})

plt.hist(df['ram'], bins=20,color='red')
plt.xlabel('RAM')
plt.ylabel('Frequency')
plt.title('RAM Distribution')
plt.show()

sns.boxplot(x=df['talk_time'],color='purple')
plt.xlabel('Talk Time')
plt.title('Talk Time Distribution')
plt.show()

sns.histplot(df, x='fc', kde=True)
plt.xlabel('Front Camera Pixels')
plt.title('Distribution of Front Camera Pixels')
plt.show()

sns.countplot(x=df['price_range'], hue=df['dual_sim'])
plt.xlabel('Price Range')
plt.ylabel('Number of Phones')
plt.title('Dual SIM Availability for each Price Range')
plt.show()

sns.pairplot(df[['battery_power', 'ram', 'px_height', 'px_width', 'price_range']], hue="price_range", diag_kind="hist")
plt.show()

plt.scatter(df['price_range'],df['ram'],color='green')
plt.xlabel('Price range')
plt.ylabel('RAM')
plt.xlim(-1,4)
plt.title('RAM vs price')
plt.show()

plt.hist(df['int_memory'], bins=10, color='orange')
plt.xlabel('Internal Memory (in GB)')
plt.ylabel('Frequency')
plt.title('Distribution of Internal Memory')
plt.show()

sns.countplot(x=d["touch_screen"],data=d)

print("3G\n",d['three_g'].value_counts(),'\n')
print("4G\n",d['four_g'].value_counts(),'\n')

three_g = [1523, 477]
four_g = [1043, 957]
labels = ['1', '0']
fig, ax = plt.subplots()
width=0.2
ax.bar(n.arange(len(labels)) - width/2, three_g, width, label='3G')
ax.bar(n.arange(len(labels)) + width/2, four_g, width, label='4G')
ax.set_xticks(n.arange(len(labels)))
ax.set_xticklabels(labels)
ax.set_xlabel('Type')
ax.set_ylabel('Count')
ax.set_title('Comparison of 3G and 4G')
ax.legend()
plt.show()

sns.histplot(x=d["ram"],data=d)
plt.title("Number of devices according to RAM size")

x_variable=d.drop("price_range",axis=1)
y_variable=d["price_range"]

"""Splitting the dataset into train and test sets"""

x_train,x_test,y_train,y_test=train_test_split(x_variable,y_variable,test_size=0.2,random_state=42)

print('x_train values : ', x_train.shape)
print('x_test values : ', x_test.shape)
print('y_train values : ', y_train.shape)
print('y_test values : ', y_test.shape)

"""Logistic Regression"""

lr=LogisticRegression(max_iter=50000, solver='saga')
lr.fit(x_train,y_train)

predicted_value=lr.predict(x_test)
print(predicted_value)

lr_accuracy = metrics.accuracy_score(y_test,predicted_value)*100
print("Accuracy score:",lr_accuracy,"%")

print("Classification Report for Logistic Regression")
print(classification_report(y_test, predicted_value))
print("--------------------------------------------------------")
conf_matrix = confusion_matrix(y_test, predicted_value)
sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='g')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix for logistic Regression')
plt.show()

"""KNN Classifier"""

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(x_train, y_train)

knn_predicted_value=knn.predict(x_test)
print(knn_predicted_value)

knn_accuracy = metrics.accuracy_score(y_test,knn_predicted_value)*100
print("Accuracy score:",knn_accuracy,"%")

print("Classification Report for K-Nearest Neighbor")
print(classification_report(y_test, knn_predicted_value))
print("--------------------------------------------------------")
conf_matrix = confusion_matrix(y_test, knn_predicted_value)
sns.heatmap(conf_matrix, annot=True, cmap='viridis', fmt='g')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix for KNN')
plt.show()

"""Random Forest"""

rf = RandomForestClassifier(max_depth=2, random_state=0)
rf.fit(x_train,y_train)

rf_predict_value=rf.predict(x_test)
print(rf_predict_value)

rf_accuracy = metrics.accuracy_score(y_test,rf_predict_value)*100
print("Accuracy score:",rf_accuracy,"%")

print("Classification Report for Random Forest")
print(classification_report(y_test, rf_predict_value))
print("--------------------------------------------------------")
conf_matrix = confusion_matrix(y_test, rf_predict_value)
sns.heatmap(conf_matrix, annot=True, cmap='Purples', fmt='g')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix for Random Forest')
plt.show()

"""Decision Tree"""

dt = DecisionTreeClassifier(random_state=0)
dt.fit(x_train,y_train)

dt_predict_value=rf.predict(x_test)
print(dt_predict_value)

dt_accuracy = metrics.accuracy_score(y_test,dt_predict_value)*100
print("Accuracy score:",dt_accuracy,"%")

print("Classification Report for Decision Tree")
print(classification_report(y_test, dt_predict_value))
print("--------------------------------------------------------")
conf_matrix = confusion_matrix(y_test, dt_predict_value)
sns.heatmap(conf_matrix, annot=True, cmap='PuRd', fmt='g')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix for Decision Tree')
plt.show()

"""Models with their Accuracy scores"""

models = pd.DataFrame({
    
    'Model': ['Logistic Regression','K-Nearest Neighbor','Random Forest','Decision Tree'],
    'Scores':[lr_accuracy,knn_accuracy,rf_accuracy,dt_accuracy]                  
                      })
models.sort_values(by='Scores', ascending=False)

models.sort_values(by='Scores',ascending=False).plot(kind='bar', color=['green'],title="Model Performance using accuracy score\n1- KNN\n2-Random Forest\n3-Decision Tree\n0-Logistic Regression")



"""Compared to all four models KNN is having highest accuracy"""

