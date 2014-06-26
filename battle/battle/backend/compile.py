import os
import os.path
import tempfile

from battle.backend.sandbox import Sandbox
from battle.api import Language

class CppCompiler:

    def __init__(self, code, path, executable):
        self.code = code
        self.path = path
        self.executable = executable

    def compile(self):
        code_path = os.path.join(self.path, "%s.cpp" % self.executable)
        f = open(code_path, "w")
        f.write(self.code)
        f.close()
        sandbox = Sandbox(self.path)
        run_result = sandbox.run(["/usr/bin/g++", "-O2", "-static", "-o", self.executable, "%s.cpp" % self.executable], None, 10)
        sandbox.cleanup()
        self.output = run_result.stderr
        if run_result.unsuccessful:
            return False
        return True

    def get_compiler_output(self):
        return self.output

class PythonCompiler:
    def __init__(self, code, path, executable):
        self.code = code
        self.path = path
        self.executable = executable

    def compile(self):
        code_path = os.path.join(self.path, "%s.py" % self.executable)
        f = open(code_path, "w")
        f.write(self.code)
        f.close()
        return True

    def get_compiler_output(self):
        return None
