from pico2d import load_image, get_time, delay
from statemachine import StateMachine, space_down, time_out, right_down, left_down, right_up, left_up, start_event
from statemachine import a_down


class Idle:
    @staticmethod       # @ : 데코레이터라고함, 함수의 기능을 마사지해줌...??
    # ^ 일반적 클래스내부의 멤버함수로 취급되는ㄷ게아니라 스태틱 메소드로 취급됨
    #"클래스 객체"랑 상관이 없는 함수.
    def enter(boy, e):
        boy.start_time = get_time()     #현재 시작시간을

        if left_up(e) or right_down(e) or boy.dir == -1:
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or boy.dir == 1 or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        #위에 얘들은 전부 입력이 있는 후에벌어지는 idle들임

        boy.frame =0
        boy.dir = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8       #소년객체의 프레임을 어찌저찌 진행해야하는거지
        #참고로 전달해준 boy는 파라미터일뿐이기에 boy라고하든 t라고하든 내맘대로바꾸든 상관없음!!!!

        if get_time() - boy.start_time > 5:
            #이벤트 발생
            boy.state_machine.add_event(('timeout', 0))
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass
    #*****이 클래스는 생성자초기화__init__가 없음!!!!
    #이 뜻은 이 클래스는 특정함수를 모아서 그루핑하는 역하르을 한다는 뜻.
    #객체찍어내는 객체 생성의 역할을 하는 것이 아님.!
    # 이 4개의 함수를 그룹시켰다고 보면 됨.

    #그리고 이렇게 만든 클래스는 저아래에서 클래스 이름을 사용할 수 있음!!!








class Sleep:
    @staticmethod
    def enter(boy, e):
            pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) %8
        pass
    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:   #오른쪽 방향
            boy.image.clip_composite_draw(boy.frame*100,300, 100,100,
            3.141592/2,#회전각도
            '',#좌우상하반전은 하지않겠다
            boy.x -25,boy.y -25, 100,100 )

        elif boy.face_dir == -1:  # 왼쪽방향보는중
            boy.image.clip_composite_draw(boy.frame*100,200, 100,100,
            3.141592/2*3,#회전각도
            '',#좌우상하반전은 하지않겠다
            boy.x -25,boy.y -25, 100,100 )
            # ^ 잘라내서 회전해라







class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.action = 1
            boy.dir = 1
        elif left_down(e) or right_up(e):
            boy.action = 0
            boy.dir = -1

        boy.frame = 0
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame+1) %8
        boy.x +=boy.dir * 3
        delay(0.01)
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame*100, boy.action*100, 100,100, boy.x,boy.y)
        pass






class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        
        self.state_machine = StateMachine(self)
        #self.state_machine.start(Sleep)

        self.state_machine.start(Idle)

        self.state_machine.set_transitions(
            {
                Idle: {right_down:Run, left_down:Run, left_up:Run, right_up:Run, time_out:Sleep,
                       start_event: Idle,
                       a_down:AutoRun},
                AutoRun : {time_out:Idle,
                           right_down:Run, left_down:Run, left_up:Run, right_up:Run},
                Run : {right_down: Idle, left_down: Idle, right_up: Idle, left_up:Idle},
                Sleep : {right_down:Run, left_down:Run, right_up:Run, left_up:Run}
            }
        )



    def update(self):
        self.state_machine.update()
          #얘는 idle에서 진행하게 해야함
        #그러므로 이동

    def handle_event(self, event):
        #현재여기의 이벤트는 input이벤트// event : input event
        #얘를 state machine용의 event로 바꿔줘야함 state machine event : (이벤트 종류, 값)
        self.state_machine.add_event(   #add_이 이벤트 저장해놔
            ('input', event)        #근데그냥 event를 주면 안되니까(플머가 정의한event정의에 위배) 튜플로 가공해서 넘겨줌
        )
        pass

    def draw(self):
        self.state_machine.draw()





class AutoRun:
    @staticmethod
    def enter(boy, e):
        if a_down(e) and boy.face_dir == 1:
            boy.action = 1
            boy.dir = 1
        elif a_down(e) and boy.face_dir == -1:
            boy.action = 0
            boy.dir = -1

        boy.frame = 0

        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame+1) %8

        if 70 <= boy.x <= 770:
            boy.x += boy.dir * 10
        elif boy.x < 70:
            boy.x = 70
            boy.dir -= boy.dir*2
        elif boy.x > 770:
            boy.x = 770
            boy.dir -= boy.dir * 2

        if boy.dir == 1:
            boy.action = 1
        elif boy.dir == -1:
            boy.action = 0


        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('timeout', 0))
            pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame*100, boy.action*100, 100, 100, boy.x, boy.y + 20, 200, 200)