# 2. Logging

프로그램에서 장애가 발생했을 때 종종 '로그 파일 주실 수 있나요?'라는 말을 들을 수 있다. 이 때, 로그 파일이 어떤 내용을 담고 있길래 사람들이 이를 필요로 하는 것일까? 

이 챕터에서는 로그 파일이 무엇이며 로그 파일의 가장 기본적인 작성법에 대해서 다룰 것이다.

### 로깅, 로그파일 ?
프로그램의 코드를 잘 때에는 에러가 언제, 어디에서, 왜 발생했는지를 잘 기록해두는 것이 중요하다. 
기록한 것을 토대로 에러를 발생시킨 부분을 쉽게 역추적할 수 있고, 이에 따라 프로그램의 유지보수가 훨씬 쉬워지기 때문이다.

이렇게 코드 수행의 시간, 코드 수행 결과 등을 기록하는 행위 자체를 로깅이라고 하고 로깅의 결과로 만들어진 파일을 로그 파일이라고 한다.
파이썬에서는 로깅을 빠르고 간편하게 수행해주는 자체적인 모듈이 존재하는데, logging이라는 모듈이 그것이다.
그러면 바로 logging 모듈을 사용하는 방법에 대해서 알아보도록 하겠다.

### logging 모듈 사용법
logging 모듈 사용법은 크게 네 가지 스텝으로 이루어져 있다.

#### 1. logging instance 만들기

```python
import logging

logger = logging.getLogger('my_log) # my_log라는 이름의 logging instance인 logger를 생성
```
위의 코드는 `my_log`라는 이름을 갖는 logging instance인 `logger`를 만들어준다.

#### 2. logging instance에 level 부여하기

```python
logger.setLevel(logging.DEBUG) # 생성한 logger라는 logging instance는 DEBUG 이상의 level를 갖는 메시지를 출력
```
위에서 생성한 `logger`가 어떤 수준의 로그 메시지를 기록할지 정하기 위해 `setLevel`이라는 메소드를 사용한다. 만약 `setLevel`에 아무런 파라미터도 전달하지 않는다면 해당 메소드는 default로 `WARNING` level을 사용하게 된다. logging instance의 level에 대해서는 아래에 간단히 정리하였으니 참고하면 좋다.

logging instance의 5가지 level
level | Description 
----- | ----------- 
DEBUG | 간단히 문제를 진단하고 싶을 때 필요한 정보를 기록
INFO  | 계획대로 작동하고 있음을 알리는 확인 메시지 기록
WARNING | 소프트웨어가 작동은 하고 있지만, 예상치 못한 일이 발생했거나 발생할 것으로 예측되는 것을 알림
ERROR | 중대한 문제로 인해 소픝웨어가 몇몇 기능들을 수행하지 못함을 알림
CRITICAL | 작동이 불가능한 수준의 심각한 에러가 발생함을 알림

#### 3. logging instance에 적용할 handler instance 만들기
handler instance는 log 메시지의 level에 따라 적절한 log 메시지를 지정된 위치에 전달(dispatch) 해주는 역할을 수행한다.
handler instance는 기능과 목적에 따라 여러개를 동시에 사용할 수 있다.
가령, console 창에 log 메시지를 띄우고 싶은 경우, StreamHandler라는 메소드를 사용할 수 있고, 아예 로그파일(.log)을 따로 만들고 싶은 경우엔 FileHandler라는 메소드를 사용할 수 있다.

handler isntance를 생성한 뒤에는 기본적인 사항들을 세팅해줘야 하는데 그 방법은 아래와 같다.

##### (1) handler instance 생성
```python
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename='information.log') # information.log라는 이름의 파일에 log 메시지를 전달
```
위의 코드에서는 console에 log 메시지를 띄우고 동시에 'information.log' 파일에 log 메시지를 기록하기 위해 `StreamHandler` 메소드와 `FileHandler` 메소드를 둘다 사용하여 두 개의 handler instance를 생성하였다.

##### (2) handler instance의 level 설정
```python
stream_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)
```
logging instance의 level을 세팅해줬던 것처럼 handler instnace의 level도 `setLevel` 메소드를 통해 세팅해줄 수 있다.
만약 handler instance의 level을 설정하지 않는다면 생성한 handler instance들은 그대로 logging instacne의 level을 따르게 된다.

위의 코드에서는 console 창에서는 INFO 이상의 로그 메시지를, 로그 파일에서는 DEBUG 이상의 로그 메시지를 출력하게끔 설정해주었다.

##### (3) handler instance에 적용할 formatter instance 생성
```python
formatter = logging.Formatter('\n[%(levelnames)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
```
formatter instance는 `Formatter` 메소드로 생성할 수 있다. 이 formatter instance를 통해 어떤 식으로 로그 메시지를 출력할 것인지 그 출력 형태를 지정해줄 수 있다.

formatter instance를 생성할 때 사용하게 되는 format은 아래와 같다.:point_down:

formatter instance를 생성할 때 사용하게 되는 format들
속성 | 이름 | 설명
--- | --- | ---
asctime | %(asctime)s | 인간이 읽을 수 있는 시간 표시
created | %(created)f | log record가 만들어진 시간
filename | %(filename)s | pathname의 file 이름 부분
funcName | %(funcName)s | logging call을 포함하는 function의 이름
levelname | %(levelname)s | 메시지의 text logging level
lineno | %(lineno)d | logging call이 발생한 코드의 line 숫자
module | %(module)s | filename의 모듈 이름 부분
message | %(message)s | 메시지
name | %(name)s | logger의 이름
pathname | %(pathname)s | full pathname
thread | %(thread)d | thread ID
threadName | %(threadName)s | thread의 이름
(참고: https://greeksharifa.github.io/%ED%8C%8C%EC%9D%B4%EC%8D%AC/2019/12/13/logging/)

##### (4) 생성한 handler instance를 logging instance에 적용

```python
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
```
위에서 생성한 formatter instance를 handler에 적용하기 위해서 `setFormatter`라는 메소드를 사용한다.
위의 코드에서는 `stream_handler`와 `file_handler`에 모두 동일한 형식의 formatter를 적용하였다.

#### 4. 생성한 handler instance를 logging instance에 적용

```python
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
```
`setLevel`, `setFormatter` 메소드로 세팅까지 완료된 handler들을 `addHandler` 메소드를 사용하여 logging instance에 적용해준다.

일반적으로 logging module을 사용할 때에는 위에서 작성한 일련의 코드를 함수화하여 사용한다.

```python
def make_logger(logger_name=None):
    #--1. logging instance 생성
    logger = logging.getLogger(logger_name)

    #--2. logging instance에 level 부여
    logger.setLevel(logging.DEBUG)

    #--3. logging instance에 적용할 handler 객체 만들기
    # (1) handler 객체 생성
    file_handler = logging.FileHandler(filename=logger_name + '.log')
    stream_handler = logging.StreamHandler()
    # (2) handler 객체의 level 설정
    file_handler.setLevel(logging.INFO)
    stream_handler.setLevel(logging.DEBUG)
    # (3) handler 객체에 사용할 formatter 객체 생성
    formatter = logging.Formatter('[%(levelname)s|%(name)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    # (4) handler 객체에 formatter 적용하여 format 설정
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    #--4. logging instance에 생성한 hnadler 적용하기
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
```

### 중복해서 찍히는 로그 메시지

바로 위에서 정의한 `make_logger`함수를 이용해서 로그 메시지를 찍게 되면 로그 메시지에서 이상한 점을 발견할 수 있을 것이다.

```python
logger1 = make_logger() # name 인자를 주지 않았기 때문에 instance 이름은 default인 'root'가 된다.
logger1.info('first log message')
logger2 = make_logger()
logger2.info('second log meassage')
logger3 = make_logger()
logger3.info('third log message')        
```
```
[INFO|root|logging_example.py:27] 2020-12-27 22:40:17,306 > first log message
[INFO|root|logging_example.py:29] 2020-12-27 22:40:17,307 > second log meassage
[INFO|root|logging_example.py:29] 2020-12-27 22:40:17,307 > second log meassage
[INFO|root|logging_example.py:31] 2020-12-27 22:40:17,307 > third log message
[INFO|root|logging_example.py:31] 2020-12-27 22:40:17,307 > third log message
[INFO|root|logging_example.py:31] 2020-12-27 22:40:17,307 > third log message
```
위의 출력 stream에서 보이듯, 로그1, 로그2, 로그2, 로그3, 로그3, 로그3, ... 이런식으로 로그를 찍을 때마다 동일한 로그가 계속 하나씩 더 직히는 현상이 발생한다.

#### 왜 이런 일이 발생하는 걸까? 
근본적인 이유는 `logging.getLogger()`함수는 싱글턴 패턴(singleton pattern)을 사용하기 때문이다.

싱글턴 패턴(singleton pattern) 이란?
> 소프트웨어 디자인 패턴에서 싱글턴 패턴을 따르는 클래스는 생성자가 여러 차례 호출되더라도 실제로 생성되는 객체는 하나이고, 최초 생성 이후에 호출된 생성자는 최초의 생성자가 생성한 객체를 리턴한다.
> 이와 같은 디자인 유형을 싱글턴 패턴이라고 한다.
(참고 : https://ko.wikipedia.org/wiki/%EC%8B%B1%EA%B8%80%ED%84%B4_%ED%8C%A8%ED%84%B4)

즉, logging 모듈에서 `getLogger` 함수로 새로운 logger를 받아올 때, 만약 'name'인자가 같을 경우 새로 logger를 만들지 않고 이미 기존에 만들어진 logger를 그대로 반환한다는 뜻이다. 

그럼 이제 다시 로그 메시지 중복현상이 왜 나타나는지 자세히 짚고 넘어가보자.

code | logger의 이름 | logger의 memory 주소 | Stream handler | File handler
---- | ----------- | ------------------- | -------------- | ------------
logger1 = make_logger() | root | 140015491961968 | |

logger의 memory 주소에서 알 수 있듯이, 아무리 logger1, logger2, logger3 이라고 객체의 이름을 달리하여 저장한다 한들, `make_logger` 함수의 name인자를 달리하지 않으면 모두 동일한 객체로 인식되고 있는 상황이다. 

따라서 `make_logger` 함수를 쓸 때마다 handler가 한개씩 추가되서 `info` 메소드로 로그 메시지를 전달해주면, 다수의 handler가 로그 메시지를 전달받아 console창에 로그 메시지가 중복돼서 나타나는 것이다.

#### 어떻게 해결할 수 있을까?

##### (1) logger의 name 인자를 달리하기
```python
logger1 = make_logger('child_1')
logger1.info('first log message')
logger2 = make_logger('child_2')
logger2.info('second log message')
logger3 = make_logger('child_3')
logger3.info('third log message')
```
```
[INFO|child_1|logging_example.py:34] 2020-12-27 23:00:01,198 > first log message
[INFO|child_2|logging_example.py:36] 2020-12-27 23:00:01,198 > second log message
[INFO|child_3|logging_example.py:38] 2020-12-27 23:00:01,198 > third log message
```
logger의 name 인자를 달리하면 `logger1`, `logger2`, `logger3` 이 각각 다른 메모리에 할당되고 따라서 로그 메시지 중복 현상도 일어나지 않는다.

하지만 만약 같은 이름의 logger를 사용하고 싶다면 이 해결책은 근본적인 해결책이 아닐 것이다. 이 경우에는 아래의 해결책을 사용해보자.

##### (2) handler 더 이상 추가하지 않기

결국 로그 메시지 중복 문제는 이미 존재하는 logger에 handler가 계속해서 추가되기 때문에 생기는 것이므로, 처음에 logger 를 생성할 때를 제외하고 handler를 추가하지 않으면 문제가 해결된다. 따라서 `make_logger`함수에 아래와 같은 logic을 추가하는 것이 하나의 방법이 될 수 있다.
```python
def make_logger(logger_name=None):
    logger = logging.getLogger(logger_name)

    # 이미 logger가 존재하면 handler 추가하지 않고 기존의 logger를 반환하는 logic 추가
    if len(logger.handlers) > 0:
        return logger

    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename=logger_name + '.log')
    stream_handler = logging.StreamHandler()
    
    file_handler.setLevel(logging.INFO)
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('\n[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

logger1 = make_logger() 
logger1.info('first log message')
logger2 = make_logger()
logger2.info('second log meassage')
logger3 = make_logger()
logger3.info('third log message') 
```
```
[INFO|root|logging_example.py:29] 2020-12-27 23:04:20,136 > first log message
[INFO|root|logging_example.py:31] 2020-12-27 23:04:20,137 > second log meassage
[INFO|root|logging_example.py:33] 2020-12-27 23:04:20,137 > third log message
```
logger의 name인자를 달리하지 않고도 충분히 중복 메시지 문제를 해결할 수 있음을 알 수 있다.

만약 `make_logger` 함수에 저런 logic을 추가하고 싶지 않다면, 아래의 코드로도 동일한 효과를 볼 수 있다.
```python
logger1 = make_logger() 
logger1.info('first log message')
logger2 = logging.getLogger()
logger2.info('second log meassage')
logger3 = logging.getLogger()
logger3.info('third log message') 
```
```
[INFO|root|logging_example.py:29] 2020-12-27 23:04:20,136 > first log message
[INFO|root|logging_example.py:31] 2020-12-27 23:04:20,137 > second log meassage
[INFO|root|logging_example.py:33] 2020-12-27 23:04:20,137 > third log message
```