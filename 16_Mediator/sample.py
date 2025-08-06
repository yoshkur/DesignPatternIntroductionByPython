"""
GUI部分で
https://yamakatsusan.web.fc2.com/pythonpattern22.html
を参考にさせていただき、実装。
"""

from abc import ABC, abstractmethod

import tkinter as tk


class Mediator(ABC):
    @abstractmethod
    def create_colleagues(self) -> None:
        pass

    @abstractmethod
    def colleague_changed(self) -> None:
        pass


class Colleague(ABC):
    @abstractmethod
    def set_mediator(self, mediator: Mediator) -> None:
        pass

    @abstractmethod
    def set_colleague_enabled(self, obj: object, enabled: bool) -> None:
        pass


class ColleagueButton(Colleague):
    mediator: Mediator

    def set_mediator(self, mediator):
        self.mediator = mediator

    def set_colleague_enabled(self, obj, enabled):
        if enabled:
            obj.configure(state=tk.NORMAL)
        else:
            obj.configure(state=tk.DISABLED)


class ColleagueTextField(Colleague):
    def set_mediator(self, mediator):
        self.mediator = mediator

    def set_colleague_enabled(self, obj, enabled):
        if enabled:
            obj.configure(state=tk.NORMAL)
        else:
            obj.configure(state=tk.DISABLED)

    def text_value_changed(self) -> None:
        self.mediator.colleague_changed()


class ColleagueCheckbox(Colleague):
    def set_mediator(self, mediator):
        self.mediator = mediator

    def set_colleague_enabled(self, obj, enabled):
        pass

    def item_state_changed(self) -> None:
        self.mediator.colleague_changed()


class LoginFrame(tk.Frame, Mediator):
    def __init__(self, master=None):
        super().__init__(master, bg='light gray')
        self.master.title('Mediator Sample')

        self.instance_colleagues()

        self.root = tk.Frame(self, bg='light gray')
        self.root.pack()

        self.radio_button_value = tk.IntVar()
        self.radio_button_value.set(1)

        self.check_guest_ = tk.Radiobutton(
            self.root,
            text='Guest',
            variable=self.radio_button_value,
            value=0,
            bg='light gray',
            font=("Times", 12),
            command=self.check_guest.item_state_changed,
        )
        self.check_guest_.grid(row=0, column=0, padx=5, pady=5)

        self.check_login_ = tk.Radiobutton(
            self.root,
            text='Login',
            variable=self.radio_button_value,
            value=1,
            bg='light gray',
            font=("Times", 12),
            command=self.checkLogin.item_state_changed,
        )
        self.check_login_.grid(row=0, column=1, padx=5, pady=5)

        self.user_name_ = tk.Label(
            self.root,
            text='Username',
            bg='light gray',
            relief=tk.RIDGE,
            bd=0,
            font=("Times", 12),
        )
        self.user_name_.grid(row=1, column=0, padx=5, pady=5)

        self.password_ = tk.Label(
            self.root,
            text='Password',
            bg='light gray',
            relief=tk.RIDGE,
            bd=0,
            font=("Times", 12),
        )
        self.password_.grid(row=2, column=0, padx=5, pady=5)

        self.text_user_buffer = tk.StringVar()
        self.text_user_buffer.trace_add(
            "write",
            lambda name, index, mode: self.text_user.text_value_changed(),
        )

        self.text_user_ = tk.Entry(
            self.root,
            width=15,
            textvariable=self.text_user_buffer,
            font=("Times", 12),
        )
        self.text_user_.grid(row=1, column=1, padx=5, pady=5)

        self.text_passbuffer = tk.StringVar()
        self.text_passbuffer.trace_add(
            "write",
            lambda name, index, mode: self.text_pass.text_value_changed(),
        )

        self.text_pass_ = tk.Entry(
            self.root,
            width=15,
            textvariable=self.text_passbuffer,
            font=("Times", 12),
        )
        self.text_pass_.grid(row=2, column=1, padx=5, pady=5)

        self.button_ok_ = tk.Button(
            self.root,
            text='OK',
            bg='light gray',
            width=12,
            font=("Times", 12),
            command=self.button_ok_pushed,
        )
        self.button_ok_.grid(row=3, column=0, padx=5, pady=5)

        self.button_cancel_ = tk.Button(
            self.root,
            text='Cacel',
            bg='light gray',
            width=12,
            font=("Times", 12),
            command=self.button_cancel_pushed,
        )
        self.button_cancel_.grid(row=3, column=1, padx=5, pady=5)

        self.create_colleagues()
        self.colleague_changed()

    def instance_colleagues(self):
        self.check_guest = ColleagueCheckbox()
        self.checkLogin = ColleagueCheckbox()
        self.text_user = ColleagueTextField()
        self.text_pass = ColleagueTextField()
        self.button_ok = ColleagueButton()
        self.buttonCancel = ColleagueButton()

    def create_colleagues(self):
        self.check_guest.set_mediator(self)
        self.checkLogin.set_mediator(self)
        self.text_user.set_mediator(self)
        self.text_pass.set_mediator(self)
        self.button_ok.set_mediator(self)
        self.buttonCancel.set_mediator(self)

    def colleague_changed(self):
        if self.radio_button_value.get() == 0:   # Guest mode
            self.text_user.set_colleague_enabled(self.text_user_, False)
            self.text_pass.set_colleague_enabled(self.text_pass_, False)
            self.button_ok.set_colleague_enabled(self.button_ok_, True)
        else:                   # Login mode
            self.text_user.set_colleague_enabled(self.text_user_, True)
            self.userpass_changed()

    def userpass_changed(self):
        # print(self.textUserBuffer.get()) #debug
        if (len(self.text_user_buffer.get()) > 0):
            self.text_pass.set_colleague_enabled(self.text_pass_, True)
            if (len(self.text_passbuffer.get()) > 0):
                self.button_ok.set_colleague_enabled(self.button_ok_, True)
            else:
                self.button_ok.set_colleague_enabled(self.button_ok_, False)
        else:
            self.text_pass.set_colleague_enabled(self.text_pass_, False)
            self.button_ok.set_colleague_enabled(self.button_ok_, False)

    def button_ok_pushed(self):
        print("buttonOkPushed")

    def button_cancel_pushed(self):
        print("buttonCancelPushed")


if __name__ == '__main__':
    login_frame = LoginFrame()
    login_frame.pack()
    login_frame.mainloop()
