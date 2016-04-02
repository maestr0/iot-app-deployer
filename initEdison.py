#!/usr/bin/env python
from config import *
from utils.remoteshell import *

edison = RemoteShellCommandExecutor(edison_user, edison_pass, edison_ip, edison_ssh_port)

gitHook = 'ls -al'

app_repo_dir = git_repos + '/' + app_name + '.git'

commands = ['mkdir -p ' + app_work_directory + '/' + app_name,
            'mkdir -p ' + app_repo_dir,
            'git init --bare ' + app_repo_dir,
            'echo "' + gitHook + '" >  ' + app_repo_dir + '/hooks/post-receive',
            'chmod +x ' + app_repo_dir + '/hooks/post-receive'
            ]

for command in commands:
    status = edison.executeRemoteCommand(command)
    if status != 0:
        raise CommandExecutionError('command failed: ' + command)

print '''

****************** DONE ********************

Run this command in your project repository:
'''
print '     git add remote device ' + edison_user + '@' + edison_ip + ':' + app_repo_dir
print '''
To deploy your app use:

    git push device

'''

edison.close()
