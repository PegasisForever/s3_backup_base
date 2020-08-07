#! /usr/bin/python3

import os
import yaml

pre_script = os.getenv('PRE_SCRIPT') or '/root/empty-script'
post_script = os.getenv('POST_SCRIPT') or '/root/empty-script'
init_script = os.getenv('INIT_SCRIPT') or '/root/empty-script'
backup_name_list = os.getenv('BACKUP_LIST').split(',')

jobs = {}
job_index = 0
for backup_name in backup_name_list:
    time, keep_count = os.getenv(f'BACKUP_{backup_name}').split("|")
    job_name = f'backup_{backup_name}'
    jobs[job_name] = {
        'cmd': f'{pre_script} && /root/backup.py {keep_count} {job_name} && {post_script}',
        'time': time,
        'onError': 'Continue',
        'notifyOnSuccess': [
            {
                'type': 'stdout',
                'data': ['stdout', 'stderr']
            }
        ],
        'notifyOnError': [
            {
                'type': 'stdout',
                'data': ['stdout', 'stderr']
            }
        ]
    }
    job_index += 1

jobber_file = {
    'version': 1.4,
    'jobs': jobs
}

with open('/root/.jobber', 'w') as file:
    yaml.dump(jobber_file, file)
os.chmod('/root/.jobber', 0o600)

os.system(init_script)