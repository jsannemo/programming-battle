import os
import os.path
import stat
import subprocess

from battle.util.config import config

class SandboxError(Exception):
    pass

class RunResult:
    def __init__(self):
        self.status_code = 0
        self.time = 0
        self.memory = 0
        self.time_limit_exceeded = False
        self.run_time_error = False
        self.killed = False
        self.unsuccessful = False
        self.stderr = None
        self.stdout = None

class Sandbox:
    def __init__(self, path):
        self.path = path
        os.chdir(self.path)
        self.box_id = 1
        self.stdin = None
        self.isolate_path = "/opt/progbattle/bin/isolate"
        command = self.get_sandbox_options()
        command += ["--init"]
        exit = subprocess.call([self.isolate_path, "--cg", "--box-id=%d" % self.box_id, "--init"])
        if exit != 0:
            raise SandboxError("Could not initialize sandbox: status code %d (%s)" % (exit, ' '.join(command)))

    # TODO make this better
    def get_sandbox_options(self):
        command = [self.isolate_path]
        command += ["--box-id=%d" % self.box_id]
        command += ["--cg"]
        command += ["-e"]

        paths = [
            "/usr",
            "/usr/lib",
            "/usr/bin",
            "/usr/local/lib",
            "/usr/include",
            "/usr/local/lib/python3.4/dist-packages/",
        ]

        for path in paths:
            if os.path.exists(path):
                command += ["--dir=" + path]

        command += ["--cg-timing"]
        command += ["--processes=128"]
        command += ["--chdir=%s" % self.path]
        command += ["--dir=/box/=%s:rw" % self.path]
        command += ["--dir=%s:rw" % self.path]
        command += ["--meta=sandbox.log"]
        return command


    def cleanup(self):
        exit = subprocess.call([self.isolate_path, "--box-id=%d" % self.box_id, "--cleanup"])
        if exit != 0:
            raise SandboxError("Could not clean up sandbox: status code %d" % exit)


    def _get_stdout(self):
        outfile = open(os.path.join(self.path, "out.txt"))
        stdout = outfile.read()
        outfile.close()
        return stdout

    def _get_stderr(self):
        outfile = open(os.path.join(self.path, "err.txt"))
        stderr = outfile.read()
        outfile.close()
        return stderr

    def run(self, program, memlim, timelim, stdin=''):
        infile_path = os.path.join(self.path, "in.txt")
        infile = open(infile_path, "w")
        if stdin:
            infile.write(stdin)
        infile.close()
        os.chmod(infile_path, stat.S_IRWXU^stat.S_IXUSR|stat.S_IRWXG^stat.S_IXGRP|stat.S_IROTH)

        command = self.get_sandbox_options()
        command += ["--stdin=in.txt"]
        command += ["--stdout=out.txt"]
        command += ["--stderr=err.txt"]
        if memlim:
            command += ["--mem=%f" % memlim]
        if timelim:
            command += ["--time=%f" % timelim]
            command += ["--wall-time=%f" % (2 * timelim)]
        else:
            command += ["--wall-time=%f" % config.sandbox.timelim]

        command += ["--run"]
        command += ["--"]
        command += program
        exit = subprocess.call(command)
        if exit != 0 and exit != 1:
            raise SandboxError("Sandbox crashed")

        meta_file = open(os.path.join(self.path, "sandbox.log"))
        result = RunResult()
        if exit == 1:
            result.unsuccessful = True

        for line in meta_file.readlines():
            key, value = line.split(":")
            if key == "exitcode" or key == "exitsig":
                result.status_code = int(value)
            if key == "status":
                if value == "SG":
                    result.run_time_error = True
                if value == "RE":
                    result.run_time_error = True
                if value == "TO":
                    result.time_limit_exceeded = True
            if key == "message":
                result.message = value
            if key == "time":
                result.time = float(value)
            if key == "cg-mem":
                result.memory = float(value)
        meta_file.close()

        result.stderr = self._get_stderr()
        result.stdout = self._get_stdout()
        return result
