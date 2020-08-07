# S3 Backup Base

```
docker pull pegasis0/s3_backup_base:latest
```

## Enviroument variables

- PRE_SCRIPT="/root/empty-script"
- POST_SCRIPT="/root/empty-script"
- INIT_SCRIPT="/root/empty-script" (Do not name your init script init.py as it is used by this image)
- BACKUP_LIST="daily,weekly"
- BACKUP_daily="* * *|10"
- BACKUP_weekly="* * *|4"
- TIME_FORMAT="%m-%d-%Y_%H:%M:%S"
- ACCESS_ID=""
- ACCESS_KEY=""
- BUCKET=""
- BACKUP_FILE="/path/to/file"
- BACKUP_S3_DIR="/path/on/s3/"
- REGION_NAME="nyc3"
- ENDPOINT_URL="https://nyc3.digitaloceanspaces.com"
