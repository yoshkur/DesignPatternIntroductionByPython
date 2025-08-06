from abc import abstractmethod

from pydantic import BaseModel


class ParseException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class Context(BaseModel):
    text: str

    tokens: list[str] = list()
    last_token: str = ''
    index: int = 0

    def model_post_init(self, context):
        self.tokens = self.text.strip().split(' ')
        self.index = 0
        self.next_token()

    def next_token(self) -> str:
        if self.index < len(self.tokens):
            self.last_token = self.tokens[self.index]
            self.index += 1
        else:
            self.last_token = None
        return self.last_token

    def current_token(self) -> str:
        return self.last_token

    def skip_token(self, token: str) -> None:
        if self.current_token() is None:
            raise ParseException(msg=f'Error: "{token}" is expected, but no more token is found.')
        elif token != self.current_token():
            raise ParseException(msg=f'Error: "{token}" is expected, but {self.current_token()} is found.')
        self.next_token()

    def current_number(self) -> int:
        if self.current_token() is None:
            raise ParseException(msg='Error: No more token.')
        number = 0
        try:
            number = int(self.current_token())
        except ValueError as e:
            raise ParseException(msg=f'Error: {str(e)}')
        return number


class Node():
    @abstractmethod
    def parse(self, context: Context) -> None:
        pass


class CommandListNode(Node):
    list_: list[Node] = []

    def parse(self, context):
        while True:
            if context.current_token() is None:
                raise ParseException(msg="Error: Missing 'end'")
            elif context.current_token() == 'end':
                context.skip_token(token='end')
                break
            else:
                command_node = CommandNode()
                command_node.parse(context=context)
                self.list_.append(command_node)

    def __repr__(self):
        return str(self.list_)


class RepeatCommandNode(Node):
    number: int
    command_list_node: Node = None

    def parse(self, context):
        context.skip_token(token='repeat')
        self.number = context.current_number()
        context.next_token()
        self.command_list_node = CommandListNode()
        self.command_list_node.parse(context=context)

    def __repr__(self):
        return f'[repeat {self.number} "{self.command_list_node}]'


class PrimitiveCommandNode(Node):
    name: str

    def parse(self, context):
        self.name = context.current_token()
        if self.name is None:
            raise ParseException(msg='Error: Missing <primitive command>')
        elif self.name not in ['go', 'right', 'left']:
            raise ParseException(msg=f"Error: Unknown <primitive command>: '{self.name}'")
        context.skip_token(self.name)

    def __repr__(self):
        return self.name


class CommandNode(Node):
    node: Node

    def parse(self, context):
        if context.current_token() == 'repeat':
            self.node = RepeatCommandNode()
        else:
            self.node = PrimitiveCommandNode()
        self.node.parse(context=context)

    def __repr__(self):
        return str(self.node)


class ProgramNode(Node):
    command_list_node: Node

    def parse(self, context):
        context.skip_token('program')
        self.command_list_node = CommandListNode()
        self.command_list_node.parse(context=context)

    def __repr__(self):
        return f'[program {self.command_list_node}]'


if __name__ == '__main__':
    try:
        with open(file='23_Interpreter/program.txt', mode='r') as fs:
            for text in fs.readlines():
                trim_text = text.strip()
                print(f'text = "{trim_text}"')
                node = ProgramNode()
                node.parse(context=Context(text=trim_text))
                print(f'node = {node}')
    except Exception as e:
        print(str(e))
