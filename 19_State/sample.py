"""
https://yamakatsusan.web.fc2.com/pythonpattern16.html
を参考にさせていただき、実装。
"""

from abc import abstractmethod

import tkinter as tk
import tkinter.scrolledtext


class Context():
    @abstractmethod
    def set_clock(self, hour: int) -> None:
        pass

    @abstractmethod
    def change_state(self, state) -> None:
        pass

    @abstractmethod
    def call_security_center(self, msg: str) -> None:
        pass

    @abstractmethod
    def record_log(self, msg: str) -> None:
        pass


class State():
    @abstractmethod
    def do_clock(self, context: Context, hour: int) -> None:
        pass

    @abstractmethod
    def do_use(self, context: Context) -> None:
        pass

    @abstractmethod
    def do_alarm(self, context: Context) -> None:
        pass

    @abstractmethod
    def do_phone(self, context: Context) -> None:
        pass


class DayState(State):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_singleton'):
            cls._singleton = super(DayState, cls).__new__(cls, *args, **kwargs)
        return cls._singleton

    @classmethod
    def get_instance(cls) -> State:
        return DayState()._singleton

    def do_clock(self, context, hour):
        if hour < 9 or 17 <= hour:
            context.change_state(NightState.get_instance())

    def do_use(self, context):
        context.record_log(msg='金庫使用(昼間)')

    def do_alarm(self, context):
        context.call_security_center(msg='非常ベル(昼間)')

    def do_phone(self, context):
        context.call_security_center(msg='通常の通話(昼間)')

    def __repr__(self):
        return '[昼間]'


class NightState(State):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_singleton'):
            cls._singleton = super(NightState, cls).__new__(cls, *args, **kwargs)
        return cls._singleton

    @classmethod
    def get_instance(cls) -> State:
        return NightState()._singleton

    def do_clock(self, context, hour):
        if 9 <= hour < 17:
            context.change_state(DayState.get_instance())

    def do_use(self, context):
        context.call_security_center(msg='非常：夜間の金庫使用！')

    def do_alarm(self, context):
        context.call_security_center(msg='非常ベル(夜間)')

    def do_phone(self, context):
        context.record_log(msg='夜間の通話録音')

    def __repr__(self):
        return '[夜間]'


class SafeFrame(tk.Frame, Context):
    def __init__(self, master=None):
        # tkinter
        tk.Frame.__init__(self, master, bg='light gray')
        self.master.title('State Sample')
        self.file_name = None
        # 時計
        self.clock = tk.StringVar()
        text_clock = tk.Label(
            self,
            textvariable=self.clock,
            font=('MS ゴシック', 12),
            bg='light gray',
            width=20,
        )
        text_clock.pack()
        # 掲示板
        self.screen = tkinter.scrolledtext.ScrolledText(
            self,
            font=('MS ゴシック', 12),
            width=25,
            height=16,
        )
        self.screen.pack(fill=tk.BOTH, expand=1)
        self.screen.focus_set()
        # 押しボタン
        self.footer_area = tk.Frame(self, bg='light gray')
        self.footer_area.pack()
        self.start_button = tk.Button(
            self.footer_area,
            text='Clock+',
            bg='light gray',
            width=8,
            font=('Times', 10),
            command=self.clock_plus,
        )
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.a_button = tk.Button(
            self.footer_area,
            text='金庫使用',
            bg='light gray',
            width=8,
            font=('Times', 10),
            command=self.button_use,
        )
        self.a_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.b_button = tk.Button(
            self.footer_area,
            text='非常ベル',
            bg='light gray',
            width=8,
            font=('Times', 10),
            command=self.button_alarm,
        )
        self.b_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.c_button = tk.Button(
            self.footer_area,
            text='通常通話',
            bg='light gray',
            width=8,
            font=('Times', 10),
            command=self.button_phone,
        )
        self.c_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.d_button = tk.Button(
            self.footer_area,
            text='終了',
            bg='light gray',
            width=8,
            font=('Times', 10),
            command=self.button_exit,
        )
        self.d_button.pack(side=tk.LEFT, padx=5, pady=5)
        # tkinter終り
        # メインルーチン
        self.state = DayState.get_instance()     # 現在の状態
        self.hour = 22
        self.set_clock(self.hour)                # 最初に，昼→夜
    # コンストラクタ終り

    def clock_plus(self):
        temp_hour = self.hour + 1
        self.hour = temp_hour % 24
        self.set_clock(self.hour)

    # ボタンが押されたらここに来る
    def button_use(self):
        self.state.do_use(self)

    def button_alarm(self):
        self.state.do_alarm(self)

    def button_phone(self):
        self.state.do_phone(self)

    def button_exit(self):
        self.quit()
        self.destroy()

    # 時刻の設定
    def set_clock(self, hour):
        clock_string = f'現在時刻は{str(hour).zfill(2)}:00'
        self.clock.set(clock_string)
        self.state.do_clock(self, hour)

    # 状態変化
    def change_state(self, state):
        self.screen.insert(tk.END, f'{self.state}から{state}へ状態が変化しました。\n')
        self.state = state

    # 警備センター警備員呼び出し
    def call_security_center(self, msg):
        self.screen.insert(tk.END, f'call! {msg}\n')

    # 警備センター記録
    def record_log(self, msg):
        self.screen.insert(tk.END, f'record ... {msg}\n')


if __name__ == '__main__':
    app = SafeFrame()
    app.pack()
    app.mainloop()
