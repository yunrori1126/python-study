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