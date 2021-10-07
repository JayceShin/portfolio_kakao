# Python 개념 정리

📖 **목차**

[1. Advantage of Python and PEP](#1-Advantage-of-Python-and-PEP)

[2. Call by Value vs Call by reference](#2-Call-by-Value-vs-Call-by-reference)

[3. Main and Name](#3-Main-and-Name)

[4. GIL in Python](#4-GIL-in-Python)

***

## 1 Advantage of Python and PEP

### 1.1 Advantage of Python
1. 변수 데이터 유형을 언급할 필요가 없음   
2. 클래스 정의, 상속 등의 객체지향 방식을 지원, public, private 과 같은 엑세스 지정자 사용하지 않음   
3. 파이썬 개발은 빠른데 실행하는 것은 컴파일 보다 느린 경우가 많음 -> C 언어 확장 기능이 있어 스크립트를 최적화 할 수 있음   
4. 웹 기반 애플리케이션, 테스트 자동화, 데이터 모델링, 빅데이터 분석 등 여러 용도로 사용 가능   

### 1.2 PEP
    최신 Python 코딩 표준으로 읽기 쉬운 코드를 제공하도록 안내함

## 2 Call by Value vs Call by reference

    Python은 passed by assignment

1. passed by assignment : 어떤 값을 전달하느냐에 따라 다름   
2. 불변(int, str) 타입의 객체를 넘기면 call by value   
3. 가변 객체를 넘기면 call by reference      

📌 *call-by-value*
> 값에 의한 호출방식은 함수 호출시 전달되는 변수의 값을 복사하여 함수의 인자로 전달   
복사된 인자는 함수 안에서 지역적으로 사용되는 local value의 특성을 가짐   
따라서 함수 안에서 인자의 값이 변경되어도, 외부의 변수의 값은 변경되지 않음   

📌 *call-by-reference*
> 참조에 의한 호출방식은 함수 호출시 인자로 전달되는 변수의 레퍼런스를 전달 (해당 변수를 가르킴.)   
따라서 함수 안에서 인자의 값이 변경되면, 아규먼트로 전달된 객체의 값도 함께 변경됨   

### code   
```python
def try_to_change_list_reference(the_list):
    print('got', the_list)
    print('got id', id(the_list))
    the_list = ['and', 'we', 'can', 'not', 'lie']
    print('set to', the_list)
    print('set id', id(the_list))

outer_list = ['we', 'like', 'proper', 'English']
print('before, outer_list =', outer_list)
print('before id', id(outer_list))
try_to_change_list_reference(outer_list)
print('after, outer_list =', outer_list)
print('after id', id(outer_list))
```

### output   
```python
before, outer_list = ['we', 'like', 'proper', 'English']
before id 1749281406600
got ['we', 'like', 'proper', 'English']
got id 1749281406600
set to ['and', 'we', 'can', 'not', 'lie']
set id 1749281406792
after, outer_list = ['we', 'like', 'proper', 'English']
after id 1749281406600
```

## 3 Main and Name

### hello.py
```python
print('hello 모듈 시작')
print('hello.py __name__:', __name__)    # __name__ 변수 출력
print('hello 모듈 끝')
```

### main.py
```python
import hello    # hello 모듈을 가져옴
 
print('main.py __name__:', __name__)    # __name__ 변수 출력
```

### output
```python
hello 모듈 시작
hello.py __name__: hello
hello 모듈 끝
main.py __name__: __main__
```

### Result
    hello.py 파일과 main.py 파일의 __name__ 변수 값이 출력

### 3.1 Reason   
1. import로 모듈을 가져오면 해당 스크립트 파일이 한 번 실행   
2. hello 모듈을 가져오면 hello.py 안의 코드가 실행   
3. hello.py의 name 변수에는 'hello'가 들어가고, main.py의 name 변수에는 'main'   

### 3.2 Interpretation   
1. name 은 모듈의 이름이 저장되는 변수이며 import로 모듈을 가져왔을 때 모듈의 이름이 들어감   
2. 파이썬 인터프리터로 스크립트 파일을 직접 실행했을 때는 모듈의 이름이 아니라 '__main__'이 들어감   
3. name 변수를 통해 현재 스크립트 파일이 시작점인지 모듈인지 판단   
4. if name == 'main':은 현재 스크립트 파일이 프로그램의 시작점이 맞는지 판단하는 작업   

## 4 GIL in Python

### 4.1 Compiler vs Interpreter

1. 컴파일 언어   
   - 소스 코드를 기계어로 컴파일해서 실행파일을 만들고 실행   

2. 인터프리터 언어   
   - 코드를 한줄씩 읽어 내려가면서 실행
