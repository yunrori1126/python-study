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
