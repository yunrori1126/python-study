# python-study
python 공부 내용을 담은 repo입니다.

# 1. Decorator

다른 사람이 짠 소스코드를 보다보면 가끔 '@' 기호를 볼 수 있는데, 이 기호가 무슨 의미를 가지고 있는지 알지 못한채 그냥 넘어간 적이 많을 것이다. 바로 답부터 말하자면, '@' 기호는 데코레이터(decorator)라는 파이썬 객체를 호출할 때 사용되는 기호이다. 데코레이터라는 이름에서도 알 수 있듯이, 이 객체는 특정한 파이썬 객체를 꾸며주는 역할을 한다.

데코레이터가 꾸며주는 파이썬 객체는 함수이며, 데코레이터는 이미 존재하는 파이썬 함수의 구조를 바꾸지 않으면서 함수에 부수적인 기능을 추가해준다. 데코레이터는 일반적으로 꾸며주고자 하는 함수를 정의하기에 앞서 호출된다.

그럼 이제 본격적으로 데코레이터가 무엇이며, 왜 필요한지, 그리고 어떻게 사용할 수 있는지에 대해 차근차근 알아보도록 하자.


### 데코레이터가 필요한 이유는 무엇일까?

데코레이터는 함수가 매번 실행될때마다 반복적으로 수행해야 하는 수고를 덜어주는 역할을 한다.
가령, 어떤 함수의 수행시간을 알고 싶다면 그 함수의 처음과 끝에 `time.time()` 함수를 사용하여 처음에 돌려받은 `time.time()`값과 함수 마지막에 돌려받은 `time.time()`값의 차이를 계산해주어야 한다. 

아래와 같이 말이다.
```python
def plus_func(first_arg, second_art):
    result = fisrt_arg + second_arg
    print("the result is {0}".format(result))

start = time.time()
plus_func(3,4)
end = time.time()
print('plus_func %2.2f usec' % int((end - start) * 1000000))
```

하지만 이렇게 수행시간을 계산해야 하는 함수가 100개가 넘어간다면 어떨까? 100개가 넘는 함수를 수행할때마다 저런 수고를 100번 넘게 거쳐야 될텐데, 이는 굉장히 번거로운 작업이 될 것이다. 바로 이럴 때 데코레이터를 사용할 수 있다.

만약 어떤 함수를 수행할 때마다 수행시간을 계산하여 출력하고 싶다면, 수행시간을 계산해주는 역할을 하는 데코레이터를 정의해주면 된다. 가령 함수 수행시간을 계산해주는 데코레이터를 `get_time_counsmed`라는 이름으로 정의를 했다면, 꾸며주고자 하는 함수인 `plus_func`를 정의하기에 앞서 호출해주면 된다.
그 뒤, `plus_func` 함수를 수행하면 수행시간이 출력되는 것을 확인할 수 있다.

```python
@get_time_consumed
def plus_func(first_arg, second_arg):
    result = fisrt_arg + second_arg
    print("the result is {0}".format(result))

plus_func(3, 4)
```
```
>>> the reulst is 7
>>> 'plus_func' 84.00 usec
```

### 데코레이터를 정의하기 전에 알아야 할 사실들?

데코레이터를 정의하기에 앞서 파이썬에서 함수라는 객체가 갖는 성질이 무엇인지 간단하게 알아야 될 사실이 몇가지 있다.

[FACT 1] 함수 안에서 또 다른 함수를 정의하게 되면, 안에 있는 함수는 밖에 있는 함수의 변수들을 가져와서 사용할 수 있다.
[FACT 2] 함수를 파이썬 변수에 할당할 수 있다.
[FACT 3] 함수는 또다른 함수를 반환할 수 있다.

```python
def decorator(function):
    # [FACT 1] 'decorator'라는 함수 안에서 정의된 'wrapper' 함수에서
    # 'decorator'함수에서 사용되는 변수인 'function'을 사용할 수 있다.
    def wrapper():
        # [FACT 2] 'function'이라는 파이썬 함수를 'func'라는 변수에 할당할 수 있다.
        func = function()
        make_uppercase = func.upper()
        return make_uppercase
    
    # [FACT 3] 'decorator' 함수는 'wrapper' 함수를 리턴할 수 있다.
```

위의 세 가지 사실을 받아들이고 나면 이제 데코레이터를 정의할 준비가 되었다.

### 데코레이터를 정의해보자!
#### 1. 위에서 사용한 `get_time_consumed`라는 데코레이터를 정의해보자.

```python
def get_time_consumed(func):
    def wrapper(func_arg1, func_arg2): # wrapper 함수의 인자로 func 함수의 인자를 전달
        start = time.time()
        reulst = func(func_arg1, func_arg2)
        end = time.time()
        print('%r %2.4f usec' % (func.name, (end - start) * 1000000))

        return result
    return wrapper # wrapper 함수 자체를 반환
```

`wrapper` 함수의 인자로 전달된 `func_arg1`, `func_arg2`는 데코레이터가 호출되면 `func` 함수의 인자로 전달된다.

위에서 정의한 `get_time_consumed` 데코레이터를 활용하여 우리는 `plus_func`라는 함수를 꾸며줄 수 있게 된다. (즉, `plus_func`함수를 실행하게 되면 함수 수행시간을 자동으로 출력할 수 있게 된다.)

```python
#-- case 1 --#
def plus_func(first_arg, second_arg):
    result = sum((first_arg, second_arg))
    print('the result is {0}.format(result))
decorated_plus_func = get_time_consumed(plus_func)
decorated_plus_func(3, 4)

#-- case 2 --#
@get_time_consumed
def plus_func(first_arg, second_arg):
    result = fisrt_arg + second_arg
    print("the result is {0}".format(result))

plus_func(3, 4)
```

case 1과 같이 `get_time_consumed` 함수 안의 인자로 `plus_func`함수를 전달해줄 수 있고,
case 2과 같이 '@'기호를 사용하여 `get_time_consumed` 함수를 데코레이터로 호출할 수도 있다.

```
>>> the result is 7
>>> 'plus_func' 73.1945 usec
```
case 1과 case 2는 동일한 결과를 내놓는다.
case 2와 같이 get_time_consumed를 데코레이터로 호출하게 되는 것의 의미는 사실상 case 1의 코드를 실행하는 것과 완벽하게 동치이기 때문이다.


#### 2. 이번에는 범용적으로 사용 가능한 decorator를 정의해보자.

사실 위에서 정의한 `get_time_consumed`라는 데코레이터는 꾸밈을 받는 함수(이 경우 `plus_func`)가 인자로 딱 두개를 전달받을 때에만 사용할 수 있기 때문에 범용성이 떨어진다.

즉, `plus_func` 함수가 딱 두개의 인자를 필요로 하기 때문에 `get_time_consumed` 데코레이터를 사용해도 에러가 나지 않았던 것이다.

만약 우리가 정의한 `plus_func` 함수가 사실은 3개, 4개, 혹은 그 이상의 인자를 전달받는 함수라면 `get_time_onsumed` 데코레이터를 사용할 수 없게 된다. 따라서 범용적으로 사용이 가능한 데코레이터를 만들어주기 위해서는 데코레이터 안의 `wrapper` 함수를 정의할 때 `*args` 또는 `**kwargs`를 인자로 전달받게 만드는 것이 좋다.

```python
def get_time_consumed_general(func):
    def wrapper(*args):
        start = time.time()
        result = func(*args)
        end = time.time()
        print('%r %2.4f usec' % (func.name, (end - start) * 1000000))

        return result
    return wrapper

@get_time_consumed_general
def plus_func(*args):
    result = sum(args)
    print('the result is {0}'.format(result))
```
```python
plus_func(3, 4, 5)
```
```
>>> the result is 12
>>> 'plus_func' 39.5775 usec
```
```python
plus_func(3, 4, 5, 6)
```
```
>>> the result is 18
>>> 'plus_func' 117.7788 usec
```

#### 3. decorator에 인자를 넣어보자!
decorator 그 자체로 인자를 필요로 하는 경우가 있는데, 이에 해당하는 decorator를 만들어보자.

만약 데코레이터를 이용해 함수의 수행시간을 출력할 때, milliseconds로 출력할지, microseconds로 출력할지, 아니면 그냥 seconds로 출력할지 선택하고자 한다면 어떻게 해야할까?
데코레이터 자체가 이러한 선택지들(milliseconds/microseconds/seconds)를 인자로 받으면 좋을 것 같은데, 어떻게 데코레이터에게 인자를 전달해줄 수 있을까?

데코레이터에게 인자를 전달해주기 위해선 데코레이터를 감싸고 있는 하나의 함수를 더 정의해주어야 한다. 즉, 데코레이터를 decorate 해줄 수 있는 함수를 데커레이터의 상위레벨에서 정의해주어야 한다는 것이다.

아래의 코드에서는 데코레이터를 감싸고 있는 함수로 `decorator_maker` 함수를 정의하였고, 이 인자로 `dec_arg를` 받도록 하였다. `dec_arg` 값이 무엇이냐에 따라 출력해주는 시간의 단위를 달리할 수 있다.
```python
def decorator_maker(dec_arg):
    def get_time_consumed_general(func):
        def wrapper(*args):
            start = time.time()
            result = func(*args) 
            end = time.time()
            if dec_arg == 'msec':
                print('%r %2.4 msec' % (func.name, (end - start) * 1000))
            elif dec_arg == 'usec':
                print('%r %2.4 usec' % (func.name, (end - start) * 1000000))
            else:
                print('%r %2.4 sec' % (func.name, (end - start)))
            return result
        return wrapper
    return get_time_consumed_general
```
```python
@decorator_maker('sec)
def plus_func(*args):
    result = sum(args)
    print('the result is {0}'.format(result))

plus_func(3, 4, 5)
```
```
>>> the result is 12
>>> 'plus_func' 0.0001 sec
```
```python
@decorator_maker('msec)
def plus_func(*args):
    result = sum(args)
    print('the result is {0}'.format(result))

plus_func(3, 4, 5)
```
```
>>> the result is 12
>>> 'plus_func' 0.1483 msec
```
```python
@decorator_maker('usec)
def plus_func(*args):
    result = sum(args)
    print('the result is {0}'.format(result))

plus_func(3, 4, 5)
```
```
>>> the result is 12
>>> 'plus_func' 79.1550 usec
```

### 데코레이터 사용 시 함수 디버깅이 어렵다!
#### 왜 어려울까?

살펴보았듯이, 데코레이터를 호출(사용)한다는 것의 의미는 `plus_func` 함수를 `wrapper` 함수로 감싼다는 의미이며, 따라서 `plus_func` 함수의 이름, docstring, 그리고 전달받은 인자들은 모두 `wrapper`라는 함수 안에 감춰진다.
즉, `plus_func`함수의 메타데이터들이 `wrapper`함수에 가려져서 보이지 않는다는 것이다.

위에서 정의한 `decorator_maker`를 사용하여 꾸민 `plus_func`의 메타데이터를 확인해보자.
```python
@decorator_maker('sec')
def plus_func(*args):
    '''
    This function returns the sum of the arguments
    '''
    result = sum(args)
    print('the result is {0}'.format(result))

print(plus_func.doc)
print(plus_func.name)
```
```
>>> None
>>> wrapper
```
`plus_func.doc`를 출력하면 'This function returns the sum of all arguments'라는 문구가 나오길 기대했지만 'None'이 출력되었고, `plus_func.name`을 출력하면 'plus_func'가 나오기를 바랐지만 이게 웬걸, 'wrapper'가 대신 출력되었다.
이를 통해 우리는 `plus_func`의 메타데이터가 `wrapper`함수에 의해 가려지게 되었음을 확인할 수 있다.

이는 곧, 만약 `plus_func`함수의 특정 부분을 잘못 코딩하여 에러가 났을 때 python tracebacke이 `plus_func`함수 레벨이 아니라 `wrapper`함수 레벨에서 까지밖에 에러를 추적하지 못한다는 것을 의미한다.
데코레이터를 호출하여 함수를 정의하면 그 함수에 대한 디버깅이 어려운 이유가 여기에 있다.

#### 어떻게 해결할 수 있을까?
이를 해결하기 위해 `functools` 모듈의 `wraps` 라는 데코레이터를 사용할 수 있다. `functools.wraps` 데코레이터는 `plus_func` 함수의 메타데이터를 카피해 `wrapper` 함수의 메타데이터에 붙여넣는 역할을 해준다.
`functools.wraps`의 사용법은 간단하다. `wrapper` 함수를 정의하기 전에 `@functools.wraps` 데코레이터를 추가해주면 끝이다!

```python
def decorator_maker(dec_arg):
    def get_time_consumed_general(func):
        @functools.wraps(func)
        def wrapper(*args):
            start = time.time()
            result = func(*args) 
            end = time.time()
            if dec_arg == 'msec':
                print('%r %2.4 msec' % (func.name, (end - start) * 1000))
            elif dec_arg == 'usec':
                print('%r %2.4 usec' % (func.name, (end - start) * 1000000))
            else:
                print('%r %2.4 sec' % (func.name, (end - start)))
            return result
        return wrapper
    return get_time_consumed_general
```
```python
@decorator_maker('sec')
def plus_func(*args):
    '''
    This function returns the sum of the arguments
    '''
    result = sum(args)
    print('the result is {0}'.format(result))

print(plus_func.doc)
print(plus_func.name)
```
```
>>> This function returns the sum of all arguments
>>> plus_func
```
`plus_func`함수의 메타데이터가 잘 출력되는 것을 확인할 수 있다.

### 데코레이터는 class로도 정의할 수 있다!

이제까지 데코레이터는 항상 function으로 정의했었는데, 사실 데코레이터는 class로도 정의할 수 있다. 인자를 필요로 하지 않는 데코레이터(`get_time_consumed_general`), 인자를 필요로 하는 데코레이터 (`decorator_maker`)모두 class로 정의할 수 있으니 이 챕터에서는 두 가지 경우를 모두 다뤄보도록 하자.

#### 1. `get_time_consumed_general` 데코레이터를 class로 정의해보자
`get_time_consumed_general` 데코레이터를 class로 정의해보자. 

인자를 필요로 하지 않았던 `get_time_consumed_general` 이라는 데코레이터를 class로 바꿔서 정의하면 아래와 같다.

```python
class GetTimeConsumedGeneral:
    def init(self, func):
        self.func = func
    
    def call(self, *args):
        start = time.time()
        result = self.func(*args)
        end = time.time()
        print('%r %2.4f usec' % (self.func.name, (end - start) * 1000000))
        return result
```
`init`메소드에서 꾸미려는 함수를 받고, `call`메소드에서 어떤식으로 꾸밀지 그 꾸미는 컨텐츠를 작성해주면 된다.
이렇게 정의된 클래스를 이용하여 `plus_func`를 꾸밀 수 있는데, 두 가지 case로 나누어서 꾸며보겠다.

```python
#-- case 1 --#
def plus_func(*args):
    result = sum(args)
    print('the result is {0}'.format(result))

decorated_plus_func = GetTimeConsumedGeneral(plus_func)
decorated_plus_func(3, 4, 5)
```
```
>>> the result is 12
>>> 'plus_func' 40.7696 usec
```
위의 case 1 코드와 같이 데코레이터를 '@' 기호를 사용하지 않고 `GetTimeConsumedGeneral`클래스에 속하는 인스턴스를 직접 만들어 `plus_func` 함수를 꾸며줄 수도 있고,
```python
#-- case 2 --#
@GetTimeConsumedGeneral
def plus_func(*args):
    result = sum(args)
    print('the result is {0}'.format(result))
```
```
>>> the result is 12
>>> 'plus_func' 40.7696 usec
```
위의 case 2 코드와 같이 데코레이터를 '@' 기호를 사용하여 `GetTimeConsumedGeneral`클래스로 정의된 데코레이터를 호출하여 `plus_func` 함수를 꾸며줄 수도 있다.

#### 2. `decorator_maker`를 class로 만들어보자
이번에는 'sec', 'usec', 'msec'와 같은 인자를 전달받았던 `decorator_maker`를 class로 정의해보도록 하자.

```python
class DecoratorMaker:
    def init(self, dec_arg):
        self.dec_arg = dec_arg
    
    def call(self, func):
        def wrapper(*args):
            start = time.time()
            result = func(*args) 
            end = time.time()
            if dec_arg == 'msec':
                print('%r %2.4 msec' % (func.name, (end - start) * 1000))
            elif dec_arg == 'usec':
                print('%r %2.4 usec' % (func.name, (end - start) * 1000000))
            else:
                print('%r %2.4 sec' % (func.name, (end - start)))
            return result
        return wrapper
```
`init`메소드에서 데코레이터의 인자(`dec_arg`)를 전달받고, `call`메소드에서 꾸미려는 함수(`func`)를 전달받는다.
그리고 `call`메소드 안에 `wrapper` 함수를 정의하고, 그 안에 어떤 식으로 꾸밀지 컨텐츠를 작성해주면 된다.

```python
#-- case 1 --#
def plus_func(*args):
    result = sum(args)
    print('the result is {0}'.format(result))

decorator_maker = DecoratorMaker('sec')
decorated_plus_func = decorator_maker(plus_func)
decorated_plus_func(3, 4, 5)
```
```
the result is 12
'plus_func_ 0.0001 sec
```
위의 case 1 코드와 같이 데코레이터 호출기호인 '@'를 사용하지 않고 `DecoratorMaker` 클래스에 속하는 인스턴스를 직접 만들어 `plus_func`함수를 꾸며줄 수도 있고,
```python
#-- case 1 --#
@DecoratorMaker('sec')
def plus_func(*args):
    result = sum(args)
    print('the result is {0}'.format(result))

plus_func(3, 4, 5)
```
```
the result is 12
'plus_func_ 0.0001 sec
```


### 데코레이터를 사용한 예제
데코레이터를 사용한 예제는 decorator_example.py 파일에 있으니 참고하도록 한다.