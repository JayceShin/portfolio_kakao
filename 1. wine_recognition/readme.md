# 와인샵 재고조사 프로젝트
 

    ⭐ 와인샵 실재고조사 업무를 AI 및 ML 기술을 통해 개선하고자 하였습니다.


📖 **목차**

[1. 프로젝트 개요](#1-프로젝트-개요)

[2. 데이터 수집 및 전처리](#2-데이터-수집-및-전처리)

[3. 모델링](#3-모델링)

[4. 수행 결과](#4-수행-결과)

***

## 1 프로젝트 개요

### 1.1 배경
백화점 내 갤러리아 소속의 지점들은 분기마다 실재고조사를 진행합니다. 이때 바이어들은 재고조사시 모든 와인의 바코드를 PDA로 스캔하여 전산화 시킵니다. 와인샵의 경우 매장에 전시된 와인은 약 1,300종이기 때문에 4명의 직원이 약 7~8 시간의 작업을 통해  재고조사를 수행합니다. 이는 단순업무이지만 와인은 온도에 민감하고 내구성이 좋지 않기 때문에 업무의 강도가 올라가게 됩니다. 따라서 저는 와인 라벨을 인식하고 분류하는 모델을 통해 이를 개선하고자 하였습니다.

<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134918492-e913dce0-34f1-4fe9-8987-9a8b2118117a.png"></p>

### 1.2 목표
    와인 라벨 인식 및 분류 모델을 통한 재고조사의 간편화

***

## 2 데이터 수집 및 전처리

### 2.1 데이터 수집
    갤러리아 한남지점 비노 494에 전시된 일부(26종)의 와인에 대해 각 와인당 약 30장의 사진을 찍었습니다.

<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134918677-9fc8dc73-9f99-4437-918b-d47fcd079eae.jpg" height="300px" width="500px"></p>

### 2.2 데이터 전처리
    수집한 이미지를 모델 학습을 위한 형태로 바꾸는 작업을 진행하였습니다.

**2.2.1 Labeling**   
와인 라벨 인식을 위한 yolo 모델을 학습하기위하여 각 사진의 라벨에 `label`로 매핑을 시켜주었습니다.   

<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134918464-40184c90-ab82-43ac-a789-736c102ebff7.PNG" height="509x" width="846px"></p>
![와인_라벨인식](https://user-images.githubusercontent.com/31294995/134918464-40184c90-ab82-43ac-a789-736c102ebff7.PNG)
![와인_라벨링결과](https://user-images.githubusercontent.com/31294995/134918465-c0ee5454-e203-4b6f-86ed-f0b08b791f13.PNG)

**2.2.2 Word Dictionary**   
KAKAO OCR API를 통해 와인에 적혀있는 텍스트를 추출하였고, 이를 상품코드와 매핑시켜 단어 사전을 준비하였습니다. 이후 Symspell을 통해 단어를 DB에 있는 기존 상품의 단어와 유사하게 교정하였습니다.

📌 *Why use Symspell?*   

***

## 3 모델링
    Obejcet Detection과 logistic 및 image 분류기를 연결하여 하나의 모델로 구성하였습니다.
    
Step1. Object Detection(Yolo) -> 와인 라벨 추출   
Step2. 추출한 이미지 -> OCR -> 추출 단어 교정(Symspell) -> 상품코드 예측(Logistic)   
Step3. 추출한 이미지 -> 이미지 분류 및 상품코드 예측(ResNet)   
    
### 3.1 Yolo

    Yolo V5 모델을 학습시킨 뒤 이미지가 들어오면 와인의 라벨을 Crop 하도록 설계하였습니다.
 
📌 *vs Other Obeject detecting model (R-CNN, Fast R-CNN, Faster R-CNN)*   

> Yolo model은 1 step의 object detect 모델이므로 다른 2 step 모델에 비해 정확도는 부족할 수 있으나 속도에 이점이 있습니다.
> 제공할 서비스는 real time으로 활용할 수 있어야 함으로 Yolo를 선택하였습니다.   
> + 사용하기도 가장 쉽기 때문이기도 합니다.

📌 *Why detect only 'Label'?*   

> b-box를 통해 객체를 찾는 Object detect 모델 특성상 작은 픽셀의 디테일(년도, 원산지 등)로 구분되는 와인의 특징을 잡아낼 지 의문이었기에 현 단계에서 라벨만 추출한 뒤 다음 단계에서 분류를 진행하는 것을 목표로 하였습니다.   
> + 실제 Label이 아닌 상품코드 단위로 학습을 시켰을시 Accuracy가 떨어짐을 확인했습니다.

### 3.2 Logistic

    OCR로 수집한 단어를 Symspell로 전처리한 데이터를 학습데이터로 분류 모델을 사용하였습니다.   
    목적함수는 multi:softProb를 사용하여 예측의 확률값을 얻고, 이를 다음 모델로 넘어갈지 말지에 대한 판단 기준으로 정하였습니다.
    
**3.2.1 TF-IDF vectorize**

📌 *vs Count Vector*   
> 와인 라벨에 의미가 없는 단어들이 포함된 경우가 있었기 때문에 Counter Vector 보다는 다른 라벨에서도 나타나 빈도수가 많은 단어에 대한 보정을 해주는 TF-IDF를 사용하였습니다.

📌 *vs Prediction Based Embedding (Word2Vec)*
> 와인 라벨은 문맥적 의미보다는 단어 자체의 중요도가 크기 때문에 횟수 기반 임베딩이 적합하다고 판단하였습니다.

**3.2.2 Logistic Regression**

📌  *vs Xgboost Classifier*   
> Xgbclassifier는 일반적으로 Logistic보다 분류의 성능이 좋은 것으로 알려져있습니다. 하지만 모든 경우가 그렇지 않다는 것을 이번 프로젝트를 통해 확인하였습니다.   
> + Hyper Parameter에 대한 최적값 연구를 하지 못한 점이 가장 큰 문제이긴 하나 Logistic만으로도 만족할 F1-Score가 나왔기 때문에 Xgbclassifier를 사용하지 않았습니다.

### 3.3 ResNet

    앞선 분류 모델에서 정확도가 낮게 나온 라벨은 와인의 디테일(Text Infomation)이 없는 이미지 라벨입니다.   
    따라서 이미지 분류기로 다시 상품코드를 예측하였습니다.

📌 *vs Other Image Classifier*   
> ResNet은 Image 분류기의 성능을 높여준 기법이긴 하나 최근에는 이보다 성능이 좋은 알고리즘들이 존재합니다. 그럼에도 ResNet을 사용한 이유는 공부한걸 써먹어보자라는 마음이 컸습니다.   
> + 기술적인 연구는 하지 못하였지만 SeResNetXt101로 Pre-train된 Weight를 사용하였을때 향상된 성능을 보임을 확인하였습니다.   

![와인_복잡도](https://user-images.githubusercontent.com/31294995/134918469-b983f163-4586-4d44-9dd6-8103e4d79c62.PNG)

***

## 4 수행 결과

### 4.1 Yolo

**학습조건**   
total image : 528   
cross validation : 5 K fold   
image size : 1024 * 1024   
epoch : 150   
batch : 32   


### 4.2 Logistic Regression

**학습조건**

### 4.3 ResNet

**학습조건**
