import pandas as pd
import numpy as np
from keras import models
from keras import layers
from keras import regularizers
import matplotlib.pyplot as plt


train_data = pd.read_csv('dataset-0510/train.csv')
test_data = pd.read_csv('dataset-0510/test.csv')

all_features = pd.concat((train_data.iloc[:, 1:-1], test_data.iloc[:, 1:]))
numeric_features = all_features.dtypes[all_features.dtypes != 'object'].index
all_features[numeric_features] = all_features[numeric_features].apply(lambda x: (x - x.mean()) / (x.std()))
# 標準化後，每個特徵的均值變為0，所以可以直接用0來替換缺失值
all_features[numeric_features] = all_features[numeric_features].fillna(0)
# dummy_na=True將缺失值也當作合法的特徵值並為其創建指示特徵
all_features = pd.get_dummies(all_features, dummy_na=True)

n_train = train_data.shape[0]
train_features = np.array(all_features[:n_train].values)
test_features = np.array(all_features[n_train:].values)
train_labels = np.array(train_data.total_price.values).reshape((-1, 1)).ravel()


# 模型定義
def build_model():
	model = models.Sequential()
	model.add(layers.Dense(512, kernel_regularizer=regularizers.l2(0.001), activation='relu', input_shape=(233, )))
	model.add(layers.Dropout(0.5))
	model.add(layers.Dense(512, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
	model.add(layers.Dropout(0.5))
	model.add(layers.Dense(512, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
	model.add(layers.Dropout(0.5))
	model.add(layers.Dense(1))
	model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
	return model



# 拆分驗證，前1000筆訓練，其他驗證
num_val_samples = 1000
num_epochs = 500
all_scores = []
print('processing start')
val_data = train_features[num_val_samples:]
val_targets = train_labels[num_val_samples:]
partial_train_data = train_features[:num_val_samples]
partial_train_targets = train_labels[:num_val_samples]


model = build_model()
history = model.fit(
	partial_train_data,
	partial_train_targets,
	validation_data=(val_data, val_targets),
	epochs=num_epochs,
	batch_size=1,
	verbose=0
)
mae_history = history.history['val_mean_absolute_error']

# 繪製驗證分數
plt.plot(range(1, len(mae_history) + 1), mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

'''
# 排除前100個資料點，繪製驗證分數
def smooth_curve(points, factor=0.9):
	smooth_points = []
	for point in points:
		if smooth_points:
			previous = smooth_points[-1]
			smooth_points.append(previous * factor + point * (1 - factor))
		else:
			smooth_points.append(point)
	return smooth_points

smooth_mae_history = smooth_curve(average_mae_history[100:])

plt.clf()
plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()


# 訓練最終模型(epochs=500)
model = build_model()
model.fit(train_features, train_labels, epochs=500, batch_size=16, verbose=0)

# 測試資料
pred_labels = model.predict(test_features)
model.save('model_2.h5')
pred_id = test_data['building_id']
prediction = pd.DataFrame(pred_labels, columns=['total_price'])
result = pd.concat([pred_id, prediction], axis=1)
print(result)
result.to_csv('submit_test.csv', index=False)
'''





























