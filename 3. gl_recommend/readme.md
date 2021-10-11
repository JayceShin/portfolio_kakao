# 회계계정 추천

    ⭐ 회계 웹 포탈 e-Accounting을 운영하며 사용자 오류로 인해 발생하는 전표 재처리건을 줄이고자 해당 프로젝트를 수행하게 되었습니다.

📖 **목차**

[1. 프로젝트 개요](#1-프로젝트-개요)

[2. 데이터 수집 및 전처리](#2-데이터-수집-및-전처리)

[3. 모델링](#3-모델링)

[4. 수행 결과](#4-수행-결과)
***
## 1 프로젝트 개요

### 배경

최근 기업은 단순업무를 처리하는 인력들의 비중을 감소하는 것에 포커스를 맞추어 이를 기업 이익에까지 연결시키고 있는 추세입니다. 
대표적으로 법인카드, 세금계산서 등 회계 전표처리를 기존에는 서무들이 했다면 최근에는 본인이 사용한 내역은 본인이 처리하는 사내 제도들이 여러 기업에서 만들어지고 있습니다. 
하지만 회계 처리에 대한 지식이 없다면 전표 작성시 선택해야할 회계 계정들에 대해 생소할 것이고, 전표를 기한내에 처리해야 하기 때문에 사소하지만 이에 대한 부담은 본인의 업무에까지 영향을 미치게 됩니다.   
또한 회계팀은 월마감시 전표를 일일히 검수하여 잘못 처리된 전표들을 반려하고 처리자에게 재처리요청을 보내야 하기에 단순 업무의 영향도가 커지게 됩니다.
따라서 이를 전표 처리시 회계 계정 과목 추천을 통해 개선하고자 합니다.

### 목표

    전표 작성시 회계 계정을 정확도 순으로 추천하여 단순업무의 부담을 줄이는 것을 목표로 하였습니다.

***
## 2 데이터 수집 및 전처리

### 데이터 수집

    회계 전표처리 DB에서 최근 3년의 법인카드 사용내역 및 전표에 대한 데이터를 수집하였습니다.   
    데이터 수집시 상위 10개의 계정코드가 전체 90%의 분포를 차지하고, 나머지는 sparse하게 나타났기에   
    10개의 계정코드만을 대상으로 진행하였습니다.

![회계_데이터](https://user-images.githubusercontent.com/31294995/134773991-00d80d96-068e-467e-9c82-85a88037f627.PNG)

### 전처리

    Null Data 및 시간 데이터에 대해 전처리를 진행하였습니다.

1. 업종코드   
업종코드가 빈 경우를 살펴보았을 때 자사 백화점에서 사용한 경우였으며, 자사 백화점에서는 법인카드를 식당만 이용할 수 있기에 빈 값을 일반 식당으로 적용하였습니다. 
세부 식당 종류의 코드들에 대해서는 정해주지 않았지만 식당에서 사용한 내역은 회계전표로 귀결될 때 대부분이 업무시식대 계정으로 매핑되기에 문제가 없을 것이라 판단하였습니다. 

2. 사용처   
사용처에 대한 내역에 다수의 빈 값들이 존재함을 확인하였습니다. 이는 해외 사용분으로써 해외의 사업자번호가 사용내역으로 0000000000과 같이 불분명하게 들어오기에 사용처에 대한 정보가 빈 값으로 채워지게 됩니다. 따라서 해당 사업자번호가 000000000으로 되어있는 사용처에 대한 정보들을 임의의 Foreign이라는 변수로 처리하였습니다.

3. 사용일/ 사용시간   
사용내역에는 사용일, 사용 시간에 대한 정보들이 들어있습니다. 
이를 활용하기 위해 사용시간이 전표 계정에 미치는 영향을 파악해보았고, 몇 가지 특징을 추려낼 수 있었습니다. 
가장 강한 특징은 사용 시간에 따라 특정 계정이 많이 사용된다는 것이었습니다. 
주로 점심, 저녁 등의 시간에 사용되면 업무시식대, 저녁 이후시간에는 접대비 그리고 이외 사용시간에는 사무에 관련된 계정들이 사용됨을 확인할 수 있었습니다. 
따라서 시간대를 총 6분류하여 해당 시간마다 labeling을 해주었습니다. 또한 사용일이 말일에 가까워질수록 여러 공과금 계정에 대한 비용계정이 사용되는 빈도가 높아질 것이라 판단하였으므로 사용일 또한 3분류하여 labeling을 진행하였습니다.

4. 금액    
금액은 사용금액, 부가세로 나누어지며 다른 인코딩된 데이터들보다 단위가 크기 때문에 StandardScaler로 조정하였습니다. 이는 평균 0 , 분산 1로 조정하는 효과가 있습니다.

5. 카테고리 변수   
수집한 데이터는 대부분이 카테고리 변수였습니다. 이를 활용하기 위해 인코딩 과정이 필요했으므로 각 모델의 특성에 맞추어 one-hot 또는 label 인코딩을 진행하였습니다.   
Tree 모델에서는 label Encoding을 하였고 Network 모델에서는 one-hot Encoding을 해주었습니다.

***
## 3 모델링

    ML과 NN 방식을 통해 모델을 구성하였습니다.

### 3.1 Machine Learning   

    ML 방식으로는 Random Forest와 XGBClassifier를 사용해 분류기를 구성하였습니다.

1. RandomizerSerach & K-fold    
최적 파라미터값을 찾기 위해 RandomizerSearch를 사용하였습니다. 일반적으로 모든 조합을 찾는 GridSearch보다 성능은 떨어질지 몰라도 조합을 무작위로 추출하는 RandomizerSearch가 시간 면에서 효율적이라고 판단하였기 때문입니다. 또한 검증을 위해 3 fold를 사용하였습니다.

![회계_grid](https://user-images.githubusercontent.com/31294995/134774544-069449ee-868d-4b55-b3da-29a90b5cb1b4.PNG)
ref <https://medium.com/@peterworcester_29377/a-comparison-of-grid-search-and-randomized-search-using-scikit-learn-29823179bc85>

2. Sampling(Under/ Over)   
데이터 분포를 살펴보았을때 아래와 같이 불균형 문제가 있음을 확인하였습니다. 따라서 언더/ 오버 샘플링 과정을 통한 결과도 확인하여 높은 스코어를 선택하도록 하였습니다.

![회계_데이터분포](https://user-images.githubusercontent.com/31294995/134775057-84d31520-3b7a-455b-b51d-9453285a160b.PNG)

```python
#under sample
X_under, y_under = RandomUnderSampler(random_state=0).fit_resample(X_train, y_train)
# over sample
X_samp_smote, y_samp_smote = SMOTE(random_state=4).fit_resample(X_train, y_train)
```

### 3.1.1 Random Forest

1. Hyper Parameter Search   
```python
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
bootstrap = [True, False]

random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
               
rf = RandomForestClassifier()
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
rf_random.fit(X_train, y_train)
rf_random.best_params_
```
[그림]

### 3.1.2 Xgboost

1. Hyper Parameter Search   
```python
min_child_weight =[1, 5, 10]
gamma = [0.5, 1, 1.5, 2, 5]
subsample = [0.6, 0.8, 1.0]
colsample_bytree = [0.6, 0.8, 1.0]
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [3, 4, 5]
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
bootstrap = [True, False]

random_grid = { 'n_estimators': n_estimators,
                'max_features': max_features,
                'max_depth': max_depth,
                'min_samples_split': min_samples_split,
                'min_samples_leaf': min_samples_leaf,
                'bootstrap': bootstrap,
                'min_child_weight' : min_child_weight,
                'gamma' : gamma,
                'subsample' :subsample,
                'colsample_bytree' : colsample_bytree}

xgb = XGBClassifier(learning_rate=0.02, n_estimators=600, objective='multi:softmax', silent=True, nthread=1)
xgb_random = RandomizedSearchCV(estimator = xgb, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
xgb_random.fit(X_train, y_train)
xgb_random.best_params_ 
```
[그림]

### 3.2 MLP


1. Parameter   
학습을 위해 사용한 학습 파라미터들은 아래와 같습니다.

```python
EPOCHS = 50
BATCH_SIZE = 64
LEARNING_RATE = 0.001
NUM_FEATURES = len(X.columns)
NUM_CLASSES = 13
```

2. Network   
분류기 네트워크 구성은 아래와 같습니다.   
 
```python
# 3 Layer  
class MulticlassClassification(nn.Module):
    def __init__(self, num_feature, num_class):
        super(MulticlassClassification, self).__init__()
        
        self.layer_1 = nn.Linear(num_feature, 512)
        self.layer_2 = nn.Linear(512, 128)
        self.layer_3 = nn.Linear(128, 64)
        self.layer_out = nn.Linear(64, num_class) 
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.2)
        self.batchnorm1 = nn.BatchNorm1d(512)
        self.batchnorm2 = nn.BatchNorm1d(128)
        self.batchnorm3 = nn.BatchNorm1d(64)
        
    def forward(self, x):
        x = self.layer_1(x)
        x = self.batchnorm1(x)
        x = self.relu(x)
        
        x = self.layer_2(x)
        x = self.batchnorm2(x)
        x = self.relu(x)
        x = self.dropout(x)
        
        x = self.layer_3(x)
        x = self.batchnorm3(x)
        x = self.relu(x)
        x = self.dropout(x)
        
        x = self.layer_out(x)
        
        return x
```  

***
## 4 수행 결과

    분류 문제이기 때문에 Confusion Matrix를 통해 산출된 Accuracy를 평가 기준으로 삼았습니다.

### Random Forest

### xgboost

1. Basic   
![회계_basic](https://user-images.githubusercontent.com/31294995/134775328-4cb2304c-7f98-4dc3-87e5-8b80241f05d4.png)

2. Under Sampling   
![회계_under](https://user-images.githubusercontent.com/31294995/134775326-3b2b7c31-f384-4089-8c60-b79726cd7409.png)

3. Over Sampling   
![회계_over](https://user-images.githubusercontent.com/31294995/134775324-631a0098-fed4-440d-9c46-a6b964ae345d.png)

### MLP

1. train vs val Accuracy & Loss   
![회계_mlp_train](https://user-images.githubusercontent.com/31294995/134775322-05fcfc07-272f-4af2-9767-9e8af4407dd9.PNG)

2. Confusion Matrix   
![mlp](https://user-images.githubusercontent.com/31294995/134775327-7ce65f6e-a6cd-4706-a8ef-7ef17ba2bf3a.png)

### Result
    XGBClassfier와 기본 데이터를 통해 나온 0.66을 Best 모델로 선정하였습니다.
***
