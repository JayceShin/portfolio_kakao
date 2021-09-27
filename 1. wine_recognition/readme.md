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

### 2.2 데이터 전처리
    수집한 이미지를 모델 학습을 위한 형태로 바꾸는 작업을 진행하였습니다.

**2.2.1 Labeling**   
와인 라벨 인식을 위한 yolo 모델을 학습하기위하여 각 사진의 라벨에 `label`로 매핑을 시켜주었습니다.   

<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134918464-40184c90-ab82-43ac-a789-736c102ebff7.PNG" height="450x" width="750px"></p>   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134918465-c0ee5454-e203-4b6f-86ed-f0b08b791f13.PNG"></p>   

**2.2.2 Word Dictionary**   
KAKAO OCR API를 통해 와인에 적혀있는 텍스트를 추출하였고, 이를 상품코드와 매핑시켜 단어 사전을 준비하였습니다. 이후 Symspell을 통해 단어를 DB에 있는 기존 상품의 단어와 유사하게 교정하였습니다.

**2.2.3 Image Regularization**   
ResNet을 진행할때는 아래와같이 이미지를 표준화 해주었습니다.  
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935546-f7f52cba-2cd2-4a82-8138-8e5f8e4de7b1.png"></p>

```python
train_meanRGB = [np.mean(x.numpy(), axis=(1,2)) for x, _ in train_ds0]
train_stdRGB = [np.std(x.numpy(), axis=(1,2)) for x, _ in train_ds0]

train_meanR = np.mean([m[0] for m in train_meanRGB])
train_meanG = np.mean([m[1] for m in train_meanRGB])
train_meanB = np.mean([m[2] for m in train_meanRGB])
train_stdR = np.mean([s[0] for s in train_stdRGB])
train_stdG = np.mean([s[1] for s in train_stdRGB])
train_stdB = np.mean([s[2] for s in train_stdRGB])
```

📌 *Why use Symspell?*   
> 기존의 편집거리기준 삽입, 전치, 바꾸기, 삭제의 Peter Norvig 방식은 시간복잡도가 매우 크기 때문에 삭제만을 기준으로 단어사전을 구성해 빠른 연산속도가 장점인 Symspell를 사용하였습니다.
> + 이는 기존보다 1,000배 빠른 것으로 알려져있습니다.
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134921671-47b6705a-6e9f-41be-b961-9fd4ddb69ba0.png" height="450x" width="750px"></p>  

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

    와인의 디테일인 년도, 원산지 등의 단어 기반의 분류를 진행하였습니다 
    
**3.2.1 TF-IDF vectorize**

📌 *vs Count Vector*   
> 와인 라벨에 의미가 없는 단어들이 포함된 경우가 있었기 때문에 Counter Vector 보다는 다른 라벨에서도 나타나 빈도수가 많은 단어에 대한 보정을 해주는 TF-IDF를 사용하였습니다.

📌 *vs Prediction Based Embedding (Word2Vec)*
> 와인 라벨은 문맥적 의미보다는 단어 자체의 중요도가 크기 때문에 횟수 기반 임베딩이 적합하다고 판단하였습니다.

**3.2.2 Logistic Regression**

    OCR로 수집한 단어를 Symspell로 전처리한 데이터를 단어사전으로 구성 후 TF-IDF를 통해 행렬화 하여 학습데이터로 사용하였습니다.   
    목적함수는 multi:softProb를 사용하여 예측의 확률값을 얻고, 이를 다음 모델로 넘어갈지 말지에 대한 판단 기준으로 정하였습니다.

### 3.3 ResNet

    앞선 분류 모델에서 정확도가 낮게 나온 라벨은 와인의 디테일(Text Infomation)이 없는 이미지 라벨입니다.   
    따라서 이미지 분류기로 다시 상품코드를 예측하였습니다.

📌 *vs Other Image Classifier*   
> ResNet은 Image 분류기의 성능을 높여준 기법이긴 하나 최근에는 이보다 성능이 좋은 알고리즘들이 존재합니다. 그럼에도 ResNet을 사용한 이유는 공부한걸 써먹어보자라는 마음이 컸습니다.   
> + 기술적인 연구는 하지 못하였지만 SeResNetXt101로 Pre-train된 Weight를 사용하였을때 향상된 성능을 보임을 확인하였습니다.   

<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134918469-b983f163-4586-4d44-9dd6-8103e4d79c62.PNG" height="450px" width="750px"></p>

***

## 4 수행 결과

### 4.1 Yolo

**4.1.1 train description** 
```python
5 Fold cross validation
label -> "lable"

learning param -> default
lr0=0.01, lrf=0.2, momentum=0.937, weight_decay=0.0005, warmup_epochs=3.0, warmup_momentum=0.8,   
warmup_bias_lr=0.1, box=0.05, cls=0.5, cls_pw=1.0, obj=1.0, obj_pw=1.0, iou_t=0.2, anchor_t=4.0,   
fl_gamma=0.0, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0, translate=0.1, scale=0.5, shear=0.0,   
perspective=0.0, flipud=0.0, fliplr=0.5, mosaic=1.0, mixup=0.0, copy_paste=0.0

batch -> 32/ epoch -> 150

model - 22
1. mAP@.5 = 0.97602 / mAP@.5:95 = 0.72421
model - 24
2. mAP@.5 = 0.9813  / mAP@.5:95 = 0.73432
model - 25
3. mAP@.5 = 0.99102 / mAP@.5:95 = 0.7828
model - 28
4. mAP@.5 = 0.98122 / mAP@.5:95 = 0.77758
model - 29
5. mAP@.5 = 0.90381 / mAP@.5:95 = 0.69221

k-fold result 
mAP@.5 = 0.96674 / mAP@.5:95 = 0.742224

total test
model - 30
train_data - 422
val_data - 106
mAP@.5 = 0.98539 / mAP@.5:95 = 0.82585

```

**4.1.2 train result**   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935529-1e1c75ca-e8d7-442f-a563-0177b1e5aa6e.png" height="450x" width="750px"></p>  

**4.1.3 PR-AUC curve**   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935523-080c8a11-9b42-4b19-b451-dba7d8ea6882.png" height="450x" width="750px"></p>  

📌 *IoU?*   
> Intersection over union의 약자로 객체 검출하는 모델의 정확도를 측정하는 지표입니다. ground-truth bounding box와 predicted bounding box를 통해 계산합니다.   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134954715-e43f1c4f-1a4c-4e48-9b86-a19ee1d641ff.PNG" height="450x" width="750px"></p>  

📌 *PR graph?*   
> confidence threshold 값에 따른 IoU로 계산한 precision과 recall의 값의 변화를 그래프로 표현한 것입니다.
> confidence: 알고리즘이 detect한 것이 정확하다고 나타내는 수치
> precision: 모든 예측된 바운딩 박스들 중에 옳은 것
> recall: 전체 정답 바운딩 박스들 중에서 검출한 것   

📌 *ROC vs PR and AUC*   
> ROC: x-FPR(FP/FP+TN)-1종오류/ y-TPR(TP/TP+FN)
> PR: x-recall/ y-precision
> AUC: 그래프 아래 면적
> ROC AUC: 데이터 균형, 양성(나쁜것)과 음성(좋은것)의 탐지 중요도 비슷
> PR AUC: 데이터 불균형, 양성(나쁜것)의 탐지가 중요할 때

📌 *mAP@.5 vs mAP@.5:95?*   
> AP는 threshold에 따라 그려진 PR graph의 넓이입니다.
> mAP@.5:95는 threshold 0.5와 0.95일때의 AP의 평균입니다.

### 4.2 Logistic Regression   

**4.2.1 Logistic Result**   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935532-db52ec74-58c6-4219-bbf3-15e1dcd367fa.jpg" height="600x" width="750px"></p>   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935533-6f5a9c49-7114-4fe7-9b7c-63efdfd0afc2.PNG" height="100x" width="750px"></p>    

**4.2.2 Xgboost Result**   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935539-242fba42-e9a6-45ee-bac5-f687e98464b9.jpg" height="600x" width="750px"></p>  
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935541-6fdec6c6-2ef7-4a3d-98cd-b1dd5e9b2c3c.PNG" height="100x" width="750px"></p>  

**4.2.3 Xgboost Tuning Result**   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935534-78d95b5e-63f5-45eb-8107-fdd1bf0bd553.jpg" height="600x" width="750px"></p>  
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935536-7f31e7f7-e70f-4c63-8b4e-fb9a1e2bf2e2.PNG" height="100x" width="750px"></p>  

📌  *vs Xgboost Classifier*   
> Xgbclassifier는 일반적으로 Logistic보다 분류의 성능이 좋은 것으로 알려져있습니다. 하지만 모든 경우가 그렇지 않다는 것을 이번 프로젝트를 통해 확인하였습니다.   
> + Hyper Parameter에 대한 최적값 연구를 하지 못한 점이 가장 큰 문제이긴 하나 Logistic만으로도 만족할 F1-Score가 나왔기 때문에 Xgbclassifier를 사용하지 않았습니다.

📌 *Bad Reuslt?*   
> 앞서 예측했던 디테일이 없는 라벨들이 나쁜 결과를 냄을 확인하였습니다.   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935544-ba63f09b-e12f-4710-a852-945be9564103.jpg" height="450x" width="750px"></p>  

📌 *Macro vs Micro vs Weighted?*   
> Macro: mean each label precision   
> Micro: total TP / total FP + total TP   
> Wegithed: mean each label precision with proportion   
> 데이터가 불균형할수록 Micro가 정확한 지표가 됩니다. 데이터가 많은쪽으로 값이 치우치기 때문입니다.

### 4.3 ResNet

**4.3.1 ResNet 50 Result**   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935552-f01991eb-dc25-4548-a7e2-bf79364660c3.jpg" height="450x" width="750px"></p>  
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935554-de9ae139-abb2-4113-836a-5a0f5af648de.jpg" height="450x" width="750px"></p>  

**4.3.2 ResNet 152 Result**   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935548-57c5d3f8-0ea2-4b9d-90c3-a1dc2a17df35.png" height="450x" width="750px"></p>  
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/134935549-f33612f5-dd81-466a-b66a-2f2096daa880.png" height="450x" width="750px"></p>  

📌 *Accuracy vs Loss?*   
> Loss는 틀리게 예측한 경우 얼마나 오류를 범했는가에 대한 값이기 때문에 정확도랑 관계가 없습니다.

📌 *Why explore Loss?*   
> 1. lr이 적절하지 못하게 크다면 optimal minima로 수렴하다가 증가할 수 있습니다.
> 2. batch를 random하게 추출할때 샘플의 분포에 따라 loss가 증가할 수 있습니다.

📌 *Why ResNet 50 better than 152?*   
> 우리가 가진 문제는 단순한데 비해 깊은 네트워크를 형성해 overfitting의 효과가 있을 것이라고 생각합니다.

📌 *decay option?*   
> L2 정규화의 효과를 가짐, 특정 가중치가 비이상적으로 커지는(Outlier에 민감) 상황을 방지하기 때문입니다.

📌 *Adam Optimizer?*   
> 학습한 방향으로 덜 이동하게 learning rate를 줄인다.
