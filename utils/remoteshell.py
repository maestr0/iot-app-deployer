import paramiko


class RemoteShellCommandExecutor:
    'Runs shell commands on remote Edison module'

    def __init__(self, user, password, ip, port):

        self.client = paramiko.Transport((ip, port))
        self.client.connect(username=user, password=password)
        self.session = self.client.open_channel(kind='session')

    def executeRemoteCommand(self, command):

        nbytes = 4096
        stdout_data = []
        stderr_data = []

        self.session.exec_command(command)
        while True:
            if self.session.recv_ready():
                stdout_data.append(self.session.recv(nbytes))
            if self.session.recv_stderr_ready():
                stderr_data.append(self.session.recv_stderr(nbytes))
            if self.session.exit_status_ready():
                break

        print ''.join(stdout_data)
        print ''.join(stderr_data)
        return self.session.recv_exit_status()

    def close(self):
        self.session.close()
        self.client.close()
