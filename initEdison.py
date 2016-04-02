#!/usr/bin/env python
from config import *
from utils.remoteshell import RemoteShellCommandExecutor

edison = RemoteShellCommandExecutor(edison_user, edison_pass, edison_ip, edison_ssh_port)
edison.executeRemoteCommand('ls')

edison.close()
