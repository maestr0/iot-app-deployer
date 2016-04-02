#!/usr/bin/env python
from config import *
from utils.remoteshell import *

edison = RemoteShellCommandExecutor(edison_user, edison_pass, edison_ip, edison_ssh_port)

template_path = './git-hooks-templates/' + git_hook_template
# with open(template_path, 'r') as template_file:
#     git_hook_template = template_file.read()
#
# print git_hook_template

app_repo_dir = git_repos + '/' + app_name + '.git'

post_receive_hook_path = app_repo_dir + '/hooks/post-receive'

commands = ['mkdir -p ' + app_work_directory + '/' + app_name,
            'mkdir -p ' + app_repo_dir,
            'git init --bare ' + app_repo_dir,
            'touch ' + post_receive_hook_path,
            'chmod +x ' + app_repo_dir + '/hooks/post-receive'
            ]

for command in commands:
    status = edison.executeRemoteCommand(command)
    if status != 0:
        raise CommandExecutionError('command failed: ' + command)

edison.scpFile(template_path, post_receive_hook_path)

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
