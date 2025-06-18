from IPython import get_ipython
from IPython.display import display
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings 
from lazypredict.Supervised import LazyClassifier, LazyRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

df = pd.read_csv(r'D:\NAM 3\Ki II\Đồ án II\dataset\du_lieu_da_xu_ly (1).csv', encoding='utf-8')
categorical_cols = ['title', 'chipset', 'GPU', 'sim_slot', 'operating_system']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le  # lưu lại encoder nếu cần sử dụng lại
categorical_cols = ['title', 'chipset', 'GPU', 'sim_slot', 'operating_system']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le  # lưu lại encoder nếu cần sử dụng lại

# Bước 3: Tạo tập train/test
X = df.drop(['price','title'], axis=1)   # Giả sử bạn muốn dự đoán giá
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = LazyRegressor()
models, predictions = clf.fit(X_train, X_test, y_train, y_test)
# In ra các mô hình và điểm số đánh giá
print(models)
# Bước 5: In kết quả
print(models)

clf = LazyClassifier()
models, predictions = clf.fit(X_train, X_test, y_train, y_test)
# In ra các mô hình và điểm số đánh giá
print(models)
# Bước 5: In kết quả
print(models)