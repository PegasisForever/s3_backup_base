from boto3 import session
from botocore.client import Config
from datetime import datetime

time_format = '%m-%d-%Y_%H:%M:%S'
access_id = 'GHZKYSC42PLPUPTUKHIM'
access_key = 'HvIgK/DMRLa/J4bmxPFSdP4NAaqnMqh7tEewd6fi1xk'
bucket = 'backup.pegasis'
backup_local_file_path = '/home/pegasis/Projects/Docker/s3-backup-base/backup.py'
backup_local_file_name = backup_local_file_path.split('/')[-1]
backup_s3_directory = 'ta2-backup/daily/'
keep_count = 3

session = session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id=access_id,
                        aws_secret_access_key=access_key)


def get_backup_list():
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=backup_s3_directory,
        Delimiter='/'
    )
    return sorted(list(map(lambda item: datetime.strptime(item['Prefix'].split('/')[-2], time_format), response['CommonPrefixes'])))


def backup():
    client.upload_file(
        backup_local_file_path,
        bucket,
        f'{backup_s3_directory}{datetime.now().strftime(time_format)}/{backup_local_file_name}'
    )


def delete_backup(time):
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=f'{backup_s3_directory}{time.strftime(time_format)}/'
    )
    files_to_delete = list(
        map(lambda item: {'Key': item['Key']}, response['Contents']))
    client.delete_objects(
        Bucket=bucket,
        Delete={
            'Objects': files_to_delete
        }
    )


print('Add backup: ', datetime.now())
backup()

backup_list = get_backup_list()
for i in range(len(backup_list)-keep_count):
    print('Delete backup: ', backup_list[i])
    delete_backup(backup_list[i])
