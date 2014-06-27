import os.path
from enum import Enum

class NamedEnum(Enum):
    def __init__(self, name):
        self.display_name = name

    @classmethod
    def get_names(cls):
        return [name for name, _ in cls.__members__.items()]

class Role(NamedEnum):

    solver = ('Solver')
    tester = ('Tester')

class Status(NamedEnum):

    queued = ('Queued')
    testing = ('Testing')
    failed = ('Failed')
    inactive = ('Inactive')
    rejected = ('Rejected')
    defeated = ('Defeated')
    active = ('Active')

class Verdict(NamedEnum):

    solved = ('Solved')
    wrong_answer = ('Wrong Answer')
    time_limit_exceeded = ('Time Limit Exceeded')
    run_time_error = ('Run-Time Error')
    security_violation = ('Security Violation')
    judge_error = ('Judge Error')

class ExtensionEnum(NamedEnum):
    def __init__(self, name, extension):
        self.extension = extension
        super(ExtensionEnum, self).__init__(name)

class Language(ExtensionEnum):

    cpp = ('C++', 'cpp')
    python = ('Python', 'py')

def detect_language(filename):
    extension = os.path.splitext(filename)[-1]
    if extension == '.cpp' or extension == '.cc':
        return Language.cpp
    if extension == '.py':
        return Language.python
    return None
