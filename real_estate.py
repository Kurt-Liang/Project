import sklearn.model_selection as ms
import sklearn.ensemble as se
import numpy as np
import pandas as pd

# 讀取csv檔
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# 獲取id以外的特徵，把train和test合在一起做處理
all_features = pd.concat((train_data.iloc[:, 1:-1], test_data.iloc[:, 1:]))
# 獲取類型不等於object的特徵
numeric_features = all_features.dtypes[all_features.dtypes != 'object'].index
# 將所有特徵標準化，均值變為0
all_features[numeric_features] = all_features[numeric_features].apply(lambda x: (x - x.mean()) / (x.std()))
# 標準化後，每個特徵的均值變為0，所以可以直接用0來替換缺失值
all_features[numeric_features] = all_features[numeric_features].fillna(0)
# dummy_na=True將缺失值也當作合法的特徵值並為其創建指示特徵
all_features = pd.get_dummies(all_features, dummy_na=True)

# 獲取train的數量
n_train = train_data.shape[0]
# 將原本合在一起的train和test分開
train_features = np.array(all_features[:n_train].values)
test_features = np.array(all_features[n_train:].values)
# 和train_features對應的結果
train_labels = np.array(train_data.total_price.values).reshape((-1, 1)).ravel()

params = [
	{'max_features': ['auto'], 'max_depth': [7, 8, 9], 'min_samples_split': [5, 6, 7]}
]
# 用網格式搜索找出f1分數最高的搭配
model = ms.GridSearchCV(se.RandomForestRegressor(n_estimators=1000, random_state=3), params, cv=5)
# 模型訓練
model.fit(train_features, train_labels)

print('===start===')
pred_y = model.predict(test_features)
# 獲取test裡的所有id
pred_id = test_data['building_id']
# 將結果變成一個列
prediction = pd.DataFrame(pred_y, columns=['total_price'])
# 將兩個列合起來輸出成csv檔
result = pd.concat([pred_id, prediction], axis=1)
print(result)
result.to_csv('submit_test.csv', index=False)
