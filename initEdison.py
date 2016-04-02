#!/usr/bin/env python
from config import *
from utils.remoteshell import *

iot = RemoteShellCommandExecutor(edison_user, edison_pass, edison_ip, edison_ssh_port)

template_path = './git-hooks-templates/' + git_hook_template

with open(template_path, 'r') as template_file:
    git_hook_template = template_file.read()

app_repo_dir = apps_git_repos + '/' + app_name + '.git'

post_receive_hook_path = app_repo_dir + '/hooks/post-receive'

app_work_path = apps_work_directory + '/' + app_name

hook_tmp = './work/hook.tmp'
text_file = open(hook_tmp, "w")
text_file.write(git_hook_template.replace('__APP_DEPLOY_DIR___', app_work_path))
text_file.close()

commands = ['mkdir -p ' + app_work_path
    ,
            'mkdir -p ' + app_repo_dir,
            'git init --bare ' + app_repo_dir,
            'touch ' + post_receive_hook_path,
            'chmod +x ' + app_repo_dir + '/hooks/post-receive'
            ]

for command in commands:
    status = iot.executeRemoteCommand(command)
    if status != 0:
        raise CommandExecutionError('command failed: ' + command)

iot.scpFile(hook_tmp, post_receive_hook_path)

print '''

****************** DONE ********************

Run this command in your project repository:
'''
print '     git add remote device ' + edison_user + '@' + edison_ip + ':' + app_repo_dir
print '''
To deploy your app use:

    git push device

'''

iot.close()
