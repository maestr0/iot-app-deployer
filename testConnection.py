#!/usr/bin/env python
from config import *
from utils.remoteshell import RemoteShellCommandExecutor

edison = RemoteShellCommandExecutor(edison_user, edison_pass, edison_ip, edison_ssh_port)
status = edison.executeRemoteCommand('uname -ar')

if status == 0:
    print "Test remote connection works!"
else:
    print "Connection error"

edison.close()
