# Python 개념 정리

📖 **목차**

[1. Advantage of Python and PEP](#1-Advantage-of-Python-and-PEP)

[2. Call by Value vs Call by reference](#2-Call-by-Value-vs-Call-by-reference)

[3. Main and Name](#3-Main-and-Name)

[4. Python Working Concept](#4-Python-Working-Concept)

[5. GIL](#5-GIL)

[6. Python Memory Management](#6-Python-Memory-Management)

[7. JIT and PyPy](#7-JIT-and-PyPy)
***

## 1 Advantage of Python and PEP

### 1.1 Advantage of Python
1. 변수 데이터 유형을 언급할 필요가 없음   
2. 클래스 정의, 상속 등의 객체지향 방식을 지원, public, private 과 같은 엑세스 지정자 사용하지 않음   
3. 파이썬 개발은 빠른데 실행하는 것은 컴파일 보다 느린 경우가 많음 -> C 언어 확장 기능이 있어 스크립트를 최적화 할 수 있음   
4. 웹 기반 애플리케이션, 테스트 자동화, 데이터 모델링, 빅데이터 분석 등 여러 용도로 사용 가능   

### 1.2 PEP
    최신 Python 코딩 표준으로 읽기 쉬운 코드를 제공하도록 안내함

***

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
***

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

***

## 4 Python Working Concept

### 4.1 Compiler vs Interpreter

1. Compile language  
   - 소스 코드를 전체를 기계어로 변환하여 실행   
   - 소스코드 변한 후 에러 보고   

2. Interpret language   
   - 소스코드가 인터프리터에 의해 직접 해석(중간코드로 변환)되어 실행   
   - 각 행마다 실행하는 도중 에러 보고      

### 4.2 Python Works   

    Python은 소스코드를 Bytecode로 컴파일한 다음 인터프리터가 실행함

📌 *Python is Compile lang vs Interpreter lang?*   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/136414137-f55185e7-a7b4-4fbf-b112-8b822e9d26ab.PNG" height="400px" width="750px"></p>   

> 표준 파이썬 구현체인 CPython의 인터프리터는 소스코드를 Bytecode로 컴파일 후 처리   
통상적으로 인터프리터 언어라고 하지만 이는 반쪽짜리 정답

📌 *Implementation?* 
> 구현체란 인터페이스(Interface)를 구현한 클래스라는 뜻이며, 구현 클래스 혹은 실체 클래스 라고도 함

📌 *Interface?* 
> 1. 인터페이스란 상수(static final)와 추상 메서드(abstract method)의 집합   
> 2. 생성자를 가질 수 없으며 따라서 객체화가 불가능   
> 3. 다중상속을 지원하며, 구현체에 여러개의 인터페이스를 구현할 수 있음

📌 *Abstract class?* 
> 1. 추상클래스는 실체 클래스의 공통적인 부분을 추출해 규경을 잡아놓은 추상적인 클래스
> 2. 메서드의 내용이 추상적이기 때문에 객체를 생성할 수 없음
> 3. 추상클래스와 실체 클래스는 상속 관계

***

## 5 GIL

### 5.1 Single Thread vs Multi Thread   

<p align="center"><img src="https://user-images.githubusercontent.com/31294995/136414152-3f355c39-6b2d-4ffd-a91b-2e0a154648cf.PNG" height="450px" width="750px"></p>   

1. Single Thread  
   - 단일 쓰레드를 사용하는 프로세스는 별도로 쓰레드 관리를 하지 않아 코딩이 용이   
   - 작업시간이 낭비되는 경우가 생김   

2. Multi Thread   
   - 하나의 프로세스에 여러개의 쓰레드를 사용하여 작업을 처리   
   - 프로세스를 병렬 처리하여 향상된 사용자 응답 제공 및 자원을 효율적으로 사용함   
   - Context switching 및 동기화 문제가 있음      

📌 *Multi-core Programming?*   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/136414151-3ba83e1a-81eb-4341-85f6-a7e8948201cc.PNG" height="250px" width="750px"></p>   

### 5.2 GIL(Global Interpreter Lock)    
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/136414145-403d133a-bf6a-43b4-84d9-f4eb9ed0f362.PNG" height="250px" width="750px"></p>   

    하나의 thread에 모든 자원을 허락하고 그 후에는 Lock을 걸어 다른 thread의 실행을 막음   
    즉, Single Thread로 동작하는 뮤텍스의 역할

📌 *Why use GIL?*   
> Python의 reference count를 통한 메모리 관리 때문
> Multi thread일 경우 reference count를 관리하기 위해 모든 객체에 lock이 필요
> 이러한 비효율을 막기 위해 하나의 Lock을 통해 모든 객체들의 동기화를 해결

📌 *Mutex vs Semaphore?*
> 1. Semaphore : 동기화 대상이 하나 이상   
> 2. Mutex : 동기화 대상이 하나   
> GIL은 Single Thread Concept이기 때문에 Mutex가 옳은 표현

📌 *How to use Parallel Programming in python?*
> 1. 다른 Python 사용
>     - GIL이 아닌 Jypthon, IronPython
> 2. Multi Processing 사용
> 3. 업무의 분할
>     - CPU가 바쁘게 계산하는 일들은 numpy 같은 라이브러리로 GIL 바깥에서 구현
> 4. 기다리기..

📌 *고찰*
> 1. 프로젝트의 덩치가 커지면 다른 Python은 현실적으로 사용 불가   
> 2. Multi processing으로 처리하면 IPC를 통한 통신에 비용이 많이 발생   
> 3. GIL 바깥에서 사용하기에는 매우 제한적 (순수 python 만 사용 등..)   
> 결국 GIL이 python의 발목을 잡는다..

***

## 6 Python Memory Management

### 6.1 Reference Counting

    모든 객체는 참조 당할 때 Reference Count를 증가시키고 참조가 없어질 때 감소   
    Count가 0이 되면 객체가 메모리에서 해제

📌 *Problem in Reference Counting*
> 자기 참조 객체는 더이상 접근할 수 없지만 Reference Count는 계속 1인 상황   
> 즉, 메모리를 해제하지 못함 = Garbage 상태   

### 6.2 Garbage Collector

    Stop the World를 통해 모든 객체를 전수조사하여 Memory management 수행   
    Reference Counting의 자기 참조 문제를 해결함   

📌 *GC 수행과정*
> 1. 새로운 객체가 생성되면 메모리와 0세대에 객체를 할당   
>     - 이 때, 객체수가 0세대 임계값보다 크면 GC 호출   
> 2. 호출된 GC는 0, 1, 2세대 모두 검사하며 2세대부터 역순으로 진행함

📌 *Memory area*   
<p align="center"><img src="https://user-images.githubusercontent.com/31294995/136414149-20e65e06-5140-48a3-a26b-0a8eee78aef5.PNG" height="450px" width="400px"></p>   

> 1. Code
>     - 실행할 프로그램의 코드가 저장   
>     - 코드 영역에 저장된 명령어를 CPU가 하나씩 처리   
> 2. Data
>     - 전역변수와 정적변수를 저장하는 공간   
>     - 프로그램 할당
> 3. Stack
>     - 지역변수와 매개변수를 저장하는 공간
>     - 함수의 호출과 함께 할당되며 호출 완료시 소멸
>     - 컴파일 타임에 미리 결정
> 4. Heap
>     - 동적 할당으로 생성되는 공간
>     - 사용자가 공간의 크기를 직접 관리
>     - 런타임에 사용자가 결정

📌 *Heap in Python*
> C, C++, Java의 경우 malloc 함수를 통해 동적 할당을 사용
> Python은 동적할당 기능이 없음
> 즉, 사용자가 메모리 할당 범위를 조정하지 않음   
> Why? 자동 메모리 관리를 해주기 때문
> Python Memory Manager가 포인터를 움직여 힙 영역의 메모리 할당 범위와 내부 버퍼 조정
> 이는 C API를 통해 동적 관리하는 것
> 메모리 할당에 있어 OS의 과부하를 줄여주는 방식


***
## 7 JIT and PyPy
### 7.1 JIT

1. 인터프리터   
바이트코드 명령어를 하나씩 읽어서 해석하고 실행한다. 하나씩 해석하고 실행하기 때문에 바이트코드 하나하나의 해석은 빠른 대신 인터프리팅 결과의 실행은 느리다는 단점을 가지고 있다.
흔히 얘기하는 인터프리터 언어의 단점을 그대로 가지는 것이다. 즉, 바이트코드라는 ‘언어’는 기본적으로 인터프리터 방식으로 동작한다. (python 과 동치)

2. JIT(Just-In-Time) 컴파일러   
인터프리터의 단점을 보완하기 위해 도입된 것이 JIT 컴파일러이다. 인터프리터 방식으로 실행하다가 적절한 시점에 바이트코드 전체를 컴파일하여 네이티브 코드로 변경하고, 이후에는 해당 메서드를 더 이상 인터프리팅하지 않고 네이티브 코드로 직접 실행하는 방식이다.
    
### 7.2 PyPy
