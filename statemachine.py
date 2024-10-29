#event 는 (종류 문자열, 실제값)로 정의
from dataclasses import asdict
from multiprocessing.connection import answer_challenge
from xml.dom.minicompat import defproperty

from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP

def start_event(e):
    return e[0] == 'start'


def space_down(e):
    return (e[0] == 'input'     #e의 첫번째 요소는 'input'
            and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE)

def time_out(e):
    return e[0] == 'timeout'



#상태 머신을 처리관리 해주는 클래스
# = 전체 상태 관리자.
class StateMachine():
    def __init__(self, o):      #누구를 위한 어떤 object를 위한것인지 전달
        self.o = o  # boy.self가 전달됨.이
        # ^ self.o는 상태머신과 연결된 캐릭터 객체를 의미

        self.event_que = []     #발생하는 이벤트를 담는 곳(큐)
        pass

    def update(self):
        self.cur_state.do(self.o) # Idle.do()를 호출하는 거지/self.o 객체를 이용해서.

        #윗줄do가 끝난 후에,
        # 혹시 이벤트가 발생했는지 확인하고, 거기에 따라 상태변환을 수행
        if self.event_que:      #list에 요소가 ㅣㅆ으면 list값은 True
            e = self.event_que.pop(0) #list의 첫번째(0) 요소를 꺼냄pop

            #이제 현상태와 현재발생한 이벤트를 토대로 다음 상태를 결정해야함
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):  # e가 check_event라면? space_down(e)이라는 것으로 해섣ㄱ뙴
                    self.cur_state.exit(self.o, e)
                    print(f'exit from {self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                    print(f'enter into {self.cur_state}')
                    return

                #trans는 딕셔너리에, 키는 self.cur인 상태를 키로 줌,





    def start(self, start_state):   #현상태를 받아서 시작상태를 정의
        self.cur_state = start_state    # <- 현재 상태를 시작상태로 만듦.
        #그리고 이게 Idle

        self.cur_state.enter(self.o, ('start', 0))      #더미 이벤트 추가
        #^새로운 상태로 시작됐기 때문에 enter를 실행해야함
        print(f'Enter into {self.cur_state}')
        pass

    def draw(self):
        self.cur_state.draw(self.o)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

    def add_event(self, e):
        self.event_que.append(e)    # <- 상태머신용 이벤트 추가
        #초기화떄에 event_que추가해준다음에 그 큐에대가 append로 추가
        print(f'       debug: new event {e} is added')
        pass






#Run상태를 위한 함수들
def right_down(e):
    return e[0] == 'input' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'input' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'input' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'input' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT