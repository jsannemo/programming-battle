from battle.backend.sandbox import Sandbox
from battle.backend.compile import CppCompiler, PythonCompiler
from battle.api import Language, detect_language
from battle.util.config import config

import os.path
import stat

class JudgeException(Exception):
    pass

class Program:
    def __init__(self, code, name, path, language):
        self.code = code
        self.name = name
        self.path = path
        self.language = language
        os.makedirs(self.path, exist_ok=True)
        os.chmod(path, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)

    def compile(self):
        print("Language %s" % self.language)
        if self.language == Language.cpp:
            compiler = CppCompiler(self.code, self.path, self.name)
        elif self.language == Language.python:
            compiler = PythonCompiler(self.code, self.path, self.name)
        else:
            raise JudgeException("Unsupported language")
        status = compiler.compile()
        self.compiler_output = compiler.get_compiler_output()
        return status

    def run(self, args=[], stdin=''):
        if self.language == Language.cpp:
            runner = CppRunner(self.path, self.name)
        elif self.language == Language.python:
            runner = PythonRunner(self.path, self.name)
        result = runner.run(args, stdin)
        runner.cleanup()
        return result

class Runner:
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.sandbox = Sandbox(path)

    def add_input(self, text):
        self.sandbox.add_stdin(text)

    def get_output(self):
        return self.sandbox.get_stdout()

    def cleanup(self):
        self.sandbox.cleanup()

class CppRunner(Runner):

    def run(self, args, stdin):
        return self.sandbox.run([self.name] + args, None, 10, stdin)

class PythonRunner(Runner):

    def run(self, args, stdin):
        return self.sandbox.run(["/usr/bin/python3", "%s.py" % self.name] + args, None, 10, stdin)

class InputValidator(Program):

    def __init__(self, problem):
        path = os.path.join(config.problem_directory, problem.contest.tag, problem.tag, "input_validator")
        files = os.listdir(path)
        if not len(files):
            raise JudgeException("No output validator for problem %s/%s"%(problem.contest.tag, problem.tag))
        validator = files[0]
        validator_path = os.path.join(path, validator)
        code_file = open(validator_path, "r")
        code = code_file.read()
        code_file.close()

        super(InputValidator, self).__init__(code, "input_validator", "/opt/progbattle/runs/%s/%s"%(problem.contest.tag, problem.tag), detect_language(validator))

    def validate(self, testcase):
        result = self.run([], testcase)
        if result.status_code == 42:
            return True
        self.message = result.stderr
        return False

class OutputValidator(Program):

    def __init__(self, problem):
        path = os.path.join(config.problem_directory, problem.contest.tag, problem.tag, "output_validator")
        files = os.listdir(path)
        if not len(files):
            raise JudgeException("No output validator for problem %s/%s"%(problem.contest.tag, problem.tag))
        validator = files[0]
        validator_path = os.path.join(path, validator)
        code_file = open(validator_path, "r")
        code = code_file.read()
        code_file.close()

        self.run_path = "/opt/progbattle/runs/%s/%s" % (problem.contest.tag, problem.tag)

        super(OutputValidator, self).__init__(code, "output_validator", self.run_path, detect_language(validator))

    def validate(self, testcase, output):
        testcase_file = open(os.path.join(self.run_path, "testcase.txt"), "w")
        testcase_file.write(testcase)
        testcase_file.close()

        output_file = open(os.path.join(self.run_path, "output.txt"), "w")
        output_file.write(output)
        output_file.close()

        result = self.run(["testcase.txt", "output.txt"], None)
        if result.status_code == 42:
            return True
        self.message = result.stderr
        return False

class SolutionProgram(Program):

    def __init__(self, solution):
        # TODO: support multiple files
        super(SolutionProgram, self).__init__(solution.files[0].contents, "solution", "/opt/progbattle/runs/%d"%solution.solution_id, Language[solution.language])

    def test(self, testcase):
        result = self.run([], testcase)
        return result
