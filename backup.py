#! /usr/bin/python3

from boto3 import session
from botocore.client import Config
from datetime import datetime
import sys
import os


def ensure_trailing_slash(path):
    if path[-1] == '/':
        return path
    else:
        return path+'/'


time_format = os.getenv('TIME_FORMAT') or '%m-%d-%Y_%H:%M:%S'
access_id = os.getenv('ACCESS_ID')
access_key = os.getenv('ACCESS_KEY')
bucket = os.getenv('BUCKET')
backup_local_file_path = os.getenv('BACKUP_FILE')
backup_local_file_name = backup_local_file_path.split('/')[-1]
backup_s3_directory = ensure_trailing_slash(
    os.getenv('BACKUP_S3_DIR'))+sys.argv[2]+'/'
keep_count = int(sys.argv[1])
region_name = os.getenv('REGION_NAME')
endpoint_url = os.getenv('ENDPOINT_URL')

session = session.Session()
client = session.client('s3',
                        region_name=region_name,
                        endpoint_url=endpoint_url,
                        aws_access_key_id=access_id,
                        aws_secret_access_key=access_key)


def get_backup_list():
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=backup_s3_directory,
        Delimiter='/'
    )
    return sorted(list(map(
        lambda item: datetime.strptime(
            item['Prefix'].split('/')[-2],
            time_format
        ),
        response['CommonPrefixes']
    )))


def backup():
    time_str = datetime.now().strftime(time_format)
    print('Add backup: ', time_str)
    client.upload_file(
        backup_local_file_path,
        bucket,
        f'{backup_s3_directory}{time_str}/{backup_local_file_name}'
    )


def delete_one_backup(time_str):
    print('Delete backup: ', time_str)
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=f'{backup_s3_directory}{time_str}/'
    )
    files_to_delete = list(
        map(lambda item: {'Key': item['Key']}, response['Contents']))
    client.delete_objects(
        Bucket=bucket,
        Delete={
            'Objects': files_to_delete
        }
    )


def delete_extra_backups():
    backup_list = get_backup_list()
    for i in range(len(backup_list)-keep_count):
        time_str = backup_list[i].strftime(time_format)
        delete_one_backup(time_str)


backup()
delete_extra_backups()
