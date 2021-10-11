# 매출 예측

    ⭐ 코로나 및 다양한 외부 요인을 반영한 일매출 예측치를 산출하기 위해 프로젝트를 수행하게 되었습니다.

📖 **목차**

[1. 프로젝트 개요](#1-프로젝트-개요)

[2. 데이터 수집 및 전처리](#2-데이터-수집-및-전처리)

[3. 모델링](#3-모델링)

[4. 수행 결과](#4-수행-결과)
***
## 1 프로젝트 개요

### 1.1 배경

경영자들은 일매출 예측치와 현재 매출액을 비교하는 화면을 통해 경영 및 평가 지표로 삼고 있습니다. 이러한 배경속에 20년 3월 코로나 사태때 백화점 식품관 매출이 감소하면서 일매출 예측치에 한참 못미치는 달성률을 보였고, 해당 부서에서 일매출 예측치에 대한 문의가 들어오게 되었습니다. 따라서 로직을 확인하여보니 단순히 3개년 매출의 평균을 산출하고 있었고, 이는 현상황을 반영하지 못한다고 판단하여 데이터를 기준으로한 매출 예측치를 새로 산출하고자 하였습니다.    
ex) 2021년 9월 26일의 매출 예측치 = (2018년 9월 26일 매출액 + 2019년 9월 26일 매출액 + 2020년  9월 26일 매출액)/3

![매출_비교](https://user-images.githubusercontent.com/31294995/134776808-85fce0b9-b3c0-4a6b-a93e-c5abeb81c0d0.jpg)

### 1.2 목표

    매출 예측치가 최근 경향을 반영하지 못하기 때문에 데이터 기반의 매출 목표치를 산출하는 것을 목표로 하였습니다.

***
## 2 데이터 수집 및 전처리

### 2.1 데이터 수집

    포스 DB에서 최근 3년의 매출 데이터를 수집하였습니다.
    이외로 백화점 휴점일, 백화점 행사 그리고 공휴일 데이터를 수집하여 데이터 분석에 사용하였습니다.

2.1 총 매출액
포스 매출 데이터에서 식품관에 해당하는 품목들로 구성하여 일매출 합계를 산출하였습니다.     

2.2 행사
지점에서 발생한 행사들 중 일반 고객에게 적용되는 범위의 행사들을 추출 하였습니다.   

***
## 3 모델링

    시계열 데이터의 예측문제이기 때문에 통계적 방법과 기계학습 방법 두 가지로 접근하였습니다.

### 3.1 Statistics Modeling

    3월 일매출을 Target으로 예측하였고, 데이터는 일자와 총 매출액 두 가지를 사용하였습니다.

3.1.1 Simple Moving Average   
단순이동평균은 특정 기간 동안의 data를 단순 평균하여 계산합니다. 따라서 그 기간 동안의 data를 대표하는 값이 이동평균 안에는 그 동안의 data 움직임을 포함하고 있습니다. 이동평균의 특징인 지연(lag)이 발생하며 수학적으로 n/2 시간 만큼의 지연이 발생합니다. 단순이동평균은 모든 데이터의 중요도를 동일하다고 간주합니다.

```python
def make_sma_arr(dataframe, col, start, window):
    result = pd.DataFrame(columns = ['index','r2'])
    result2 = dataframe.copy()

    for i in range(start,window+1):
        pred = pd.DataFrame()
        sma_month = pd.DataFrame()

        sma_month['MA'] = pd.Series.rolling(dataframe[col],window=i, center=False).mean()
        pred['pred'] = sma_month['MA'].shift(1)
        st = pred.apply(pd.Series.first_valid_index)
        y = dataframe[col][st[0]:]
        y_pred = sma_month['MA'][st[0]:]
        #rmse = mean_squared_error(y, y_pred)**0.5
        r2 = r2_score(y,y_pred)
        result = result.append({'index': "{0:.0f}".format(i),'r2':"{0:.03f}".format(r2)}, ignore_index=True)
        result2.insert(i, str(i)+"ma",sma_month['MA'])
    
    return result, result2
    
# 이동평균 window size 2, 3, 4
result, result2 = make_sma_arr(df_date_sum, 'SALE_AMT',2,4)    
```

3.1.2 Exponential Moving Average   
지수이동평균은 가중이동평균 중의 하나로 단순이동평균보다 최근의 데이터에 높은 가중치를 부여하는 방법입니다.

```python
def make_emw_arr(dataframe, col, start, window):
    result = pd.DataFrame(columns = ['index','r2'])
    result2 = dataframe.copy()

    for i in range(start,window+1):
        pred = pd.DataFrame()
        sma_month = pd.DataFrame()

        sma_month['MA'] = dataframe[col].ewm(span=i).mean().values
        pred['pred'] = sma_month['MA'].shift(1)
        st = pred.apply(pd.Series.first_valid_index)
        y = dataframe[col][st[0]:]
        y_pred = sma_month['MA'][st[0]:]
        #rmse = mean_squared_error(y, y_pred)**0.5
        r2 = r2_score(y,y_pred)
        result = result.append({'index': "{0:.0f}".format(i),'r2':"{0:.03f}".format(r2)}, ignore_index=True)
        result2.insert(i, str(i)+"ew",sma_month['MA'])
    
    return result, result2
    
# 단순지수평활 window size 2, 3, 4
result, result2 = make_emw_arr(df_date_sum, 'SALE_AMT',2,4)
```

3.1.3 Simple Exponential Smoothing   
trend나 seasonality 반영을 하지 못하며 level 정도만 수평선으로 나오게 됩니다.

```python
ssm1=SimpleExpSmoothing(df_date_sum.SALE_AMT).fit(smoothing_level=0.05,optimized=False)
ssm2=SimpleExpSmoothing(df_date_sum.SALE_AMT).fit(smoothing_level=0.3,optimized=False)
ssm0=SimpleExpSmoothing(df_date_sum.SALE_AMT).fit()
y_pred0 = ssm0.fittedvalues
y_pred1 = ssm1.fittedvalues
y_pred2 = ssm2.fittedvalues
```

3.1.3 Holt-Winter's Exponential Smoothing   
trend로 데이터를 예측하기 위해 Simple Exponential Smoothing에서 확장한 것입니다. 예측을 위한 식 외에 level smoothing을 위한 식과 trend smoothing을 위한 식이 포함됩니다. 생성된 예측은 선형적으로 나타나기 때문에 예측 범위가 멀어질 수록 over-forecast 되는 경향이 있다.

```python
holt_fit0=Holt(df_date_sum.SALE_AMT).fit(smoothing_level=0.8,smoothing_slope=0.3) #holt additive model
holt_fit1=Holt(df_date_sum.SALE_AMT,exponential=True).fit(smoothing_level=0.8,smoothing_slope=0.3) #holt exponential model
holt_fit2=Holt(df_date_sum.SALE_AMT,damped=True).fit(smoothing_level=0.8,smoothing_slope=0.3) #holt damped trend
y = result2.SALE_AMT
y_pred0 = holt_fit0.fittedvalues
y_pred1 = holt_fit1.fittedvalues
y_pred2 = holt_fit2.fittedvalues
```
### 3.2 ARIMA

    시계열 예측 모델인 ARIMA를 통해 매출액을 예측하였습니다.

3.2.1 데이터 분해   
일 매출 예측이기 때문에 주기를 1로 두었고, 이로인해 별다른 특징을 파악하지 못하였습니다.

```python
decomposition = sm.tsa.seasonal_decompose(df['SALE_AMT'], model='additive', freq=1)
fig = decomposition.plot()
fig.set_size_inches(10,10)
plt.show()
```
![arima_분해](https://user-images.githubusercontent.com/31294995/136822429-07462004-56d2-425e-ab12-58cf4dfc5e27.PNG)   

3.2.2 Stationarity 파악   
ARIMA 모델을 사용하기 위해서는 데이터가 Stationary 해야 하기 때문에 ACF, PACF plot를 살펴보았습니다.   

```python
fig, ax = plt.subplots(1,2,figsize=(10,5))
fig.suptitle('Raw Data')
sm.graphics.tsa.plot_acf(train_data.values.squeeze(), lags=30, ax=ax[0])
sm.graphics.tsa.plot_pacf(train_data.values.squeeze(), lags=30, ax=ax[1])
```
![ARIMA_ACF](https://user-images.githubusercontent.com/31294995/136822426-b2ac7935-b024-493d-900c-d14887e8110e.PNG)   

3.2.3 Differencing   
앞서 살펴본 ACF 그래프가 조금 애매하였기 때문에 Differencing을 통해 Data를 Statinary하도록 변형하였습니다.   

```python
diff_train_data = train_data.copy()
diff_train_data = diff_train_data['SALE_AMT'].diff()
diff_train_data = diff_train_data.dropna()
```
![arima_diff](https://user-images.githubusercontent.com/31294995/136822424-fb9857d9-929a-4577-83a2-0ddae5f73651.PNG)   

![arima_diff_acf](https://user-images.githubusercontent.com/31294995/136822421-4ee248ea-f07e-4879-b993-f749f69cd850.PNG)   

lag가 1일때 눈에 띄게 감소하였기 때문에 확실한 Stationary를 갖고 있다고 판단하였습니다.

3.2.4 Sequential Search   
마지막으로 Best Parameter를 찾기 위해 순차적 접근을 진행하였습니다.

```python
p = range(0,4)
d = range(1,2)
q = range(0,3)
pdq = list(itertools.product(p,d,q))
aic=[]

for i in pdq:
    model = ARIMA(train_data.values, order=i)
    model_fit = model.fit()
    print(f'ARIMA: {i} >> AIC : {round(model_fit.aic,2)}')
    aic.append(round(model_fit.aic,2))
```

### 3.3 Prophet

    시계열 예측 모델인 Prophet을 사용하였으며 데이터의 조건을 달리하며 실험하였습니다.

3.3.1 Boundary   
Outlier를 제거하기위해 금액별 Sorting을 하였고, 상위 1개/ 하위 4개를 제거하도록 Boundary를 지정하였습니다.   
![매출_소팅](https://user-images.githubusercontent.com/31294995/134778585-55047d0e-e92f-41cb-93c7-c0c874df69ca.PNG)

3.3.2 Basic   
다른 조건 없이 일자/ 매출액 두 가지 변수로 매출액을 예측하였습니다.

```python
df_ml['cap'] = 10000000
df_ml['floor'] = 3000000
model =  Prophet.Prophet(growth='logistic') 
model.fit(df_ml);
```

3.3.3 Change Point   
입력된 데이터들의 추세를 조정하는 인자로 탐색을 통해 찾은 최적값 0.01로 설정하였습니다. 추가적인 추세변경점으로 코로나 일자를 넣었으나 결과에 영향은 없었습니다.

```python
df_ml['cap'] = 10000000
df_ml['floor'] = 3000000
model =  Prophet.Prophet(changepoint_prior_scale=0.01) 
model.fit(df_ml);
```

3.3.4 Holiday   
앞서 수집한 공휴일을 redday로 행사일을 evntday로 설정하여 데이터를 형성하였고, 각 Boundary를 주어 해당되는 일자에 전반적으로 영향을 미치도록 하였습니다.

```python
redday = pd.DataFrame({
  'holiday': 'redday',
  'ds': pd.to_datetime(df_hol['DS']),
  'lower_window': 0,
  'upper_window': 1,
})
evntday = pd.DataFrame({
  'holiday': 'evntday',
  'ds': pd.to_datetime(df_evnt['EVNT_START_YMD']),
  'lower_window': 0,
  'upper_window': 1,
})
holidays = pd.concat((redday, evntday))

df_ml['cap'] = 10000000
df_ml['floor'] = 300000
model =  Prophet.Prophet(changepoint_prior_scale=0.01, holidays=holidays, 
                        yearly_seasonality=10, weekly_seasonality=5, daily_seasonality=False) 
model.fit(df_ml);
```

***
## 4 수행 결과

    Large Sclae의 금액 예측 문제이기 때문에 RMSE가 아닌 R2를 평가 기준으로 삼았습니다. 
    R2는 차이가 클 시 (-) 값이 나올 수 있습니다.

### 4.1 Real Data 

실제 매출 예측치와 매출액의 차이를 계산한 R2 Score입니다.   
**R2: -2.194**   
![매출_실제](https://user-images.githubusercontent.com/31294995/134778589-8acc6c1b-9ee8-48b2-bfd2-0567386e0001.PNG)

### 4.2 Statistics Modeling

4.2.1 Simple Moving Average   
**Best R2: 0.688(window size:2)**   
![매출_이동평균](https://user-images.githubusercontent.com/31294995/134778593-600fc440-d87d-425b-8b13-51b499ce51be.PNG)

4.2.2 Exponential Moving Average   
**Best R2: 0.884(window size:2)**   
![매출_지수평활](https://user-images.githubusercontent.com/31294995/134778592-1296e9c0-05c7-42b3-92d4-245100d796e7.PNG)

4.2.3 Simple Exponential Smoothing   
**Best R2: 0.119(smoothing_level=0.05)**   
![매출_심플](https://user-images.githubusercontent.com/31294995/134778591-8102c2e1-653a-49ea-b747-61483c2af665.PNG)

4.2.4 Holt-Winter's Exponential Smoothing   
**Best R2: 0.119(smoothing_level=0.8, smoothing_slope=0.3)**   
![매출_홀트](https://user-images.githubusercontent.com/31294995/134778590-1f6b13a7-6cfc-46c9-96a5-c46c6fd86960.PNG)

### 4.3 ARIMA

4.3.1 BEST RESULT
![arima_best_result](https://user-images.githubusercontent.com/31294995/136822417-83084886-2a40-4a6f-b16f-6c642d5199e3.PNG)   

4.3.2 Predict Graph & R2 score
**Best R2: -0.33**   
![arima_best_result2](https://user-images.githubusercontent.com/31294995/136822410-5e3111e5-edf9-4bb8-abfb-ce207779d301.PNG)   

### 4.4 Prophet

4.3.1 Basic   
**Best R2: 0.111**   
![매출_베이직](https://user-images.githubusercontent.com/31294995/134778588-4be0d3cf-fbff-42a1-8d37-adc9c10d98fb.PNG)

4.3.2 Change Point   
**Best R2: 0.118**   
![매출_체인지](https://user-images.githubusercontent.com/31294995/134778587-08c9a037-ff2b-4c26-8ca2-24d3c5e587d0.PNG)

4.3.3 Holiday   
**Best R2: 0.119**  
![매출_휴일](https://user-images.githubusercontent.com/31294995/134778586-5e876dbb-abd5-42dc-b8cf-d3da4fa25948.PNG)

### Result

    통계 모형의 지수이동평균법이 가장 높은 정확도를 보였습니다.

📌 **통계적 모델이 기계학습보다 정확도가 월등한 이유?**   
일매출은 변동이 매우 크고 추세(계절성)를 파악하기 어렵기 때문에 단순하며 최근 데이터에 가중치를 준 지수평활법이 높은 결과를 냈다고 생각합니다.

📌 **고찰**   
매출 현황의 추세를 본다면 통계모형으로도 부족하지 않은것으로 보이나 통계모형은 짧은기간의 데이터만 예측한다는 한계점이 있기에 유의미한 변수를 수집해 머신러닝쪽으로 더 정확한 모델을 개발하여  예측 결과에 따른 대응 전략을 수립하는데 유용할 것이라 생각합니다.

***
