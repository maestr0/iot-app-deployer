import paramiko


class RemoteShellCommandExecutor:
    'Runs shell commands on remote Edison module'

    def __init__(self, user, password, ip, port):

        self.client = paramiko.Transport((ip, port))
        self.client.connect(username=user, password=password)

    def executeRemoteCommand(self, command):
        session = self.client.open_channel(kind='session')
        nbytes = 4096
        stdout_data = []
        stderr_data = []
        print 'Executing: ' + command
        session.exec_command(command)
        while True:
            if session.recv_ready():
                stdout_data.append(session.recv(nbytes))
            if session.recv_stderr_ready():
                stderr_data.append(session.recv_stderr(nbytes))
            if session.exit_status_ready():
                break

        output = ''.join(stdout_data)
        if output:
            print output

        errors = ''.join(stderr_data)
        if errors:
            print errors

        return session.recv_exit_status()

    def close(self):
        self.client.close()


class CommandExecutionError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
