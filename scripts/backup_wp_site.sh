#You need modify below varriable to appropriate with your
BACKUP_TEMP_DIR="/var/www/backup_folder"
BACKUP_CODE="/var/www/Backup-To-Google-Drive"
BACKUP_CONFIG_FILE="config_for_your_domain.json"
#if your site is stored in /var/www/yourdomain.com
# then PARENT_WORDPRESS_SITE="/var/www"
# and SITE_NAME="yourdomain.com"
PARENT_WORDPRESS_SITE="/var/www"
SITE_NAME="yourdomain.com"

DBNAME='yourdb_name'
DBUSER='yourdb_user'
DBPASSWORD='yourdb_password'

#End define, below is my work :)

WORDPRESS_SITE_PATH=$PARENT_WORDPRESS_SITE"/"$SITE_NAME

BACKUP_FILE=$SITE_NAME"_`date +%Y%m%d-%H%M`.tar.gz"
#Sql file name with year-month-date-hour-minute
SQLFILE=$DBNAME'.sql'
SQL_BACKUP_FILE=$DBNAME'.tar.gz'

BACKUP_FILE_PATH=$BACKUP_TEMP_DIR'/'$BACKUP_FILE

echo "Dumping DB name=$DBNAME"
#Create backup folder if folder is not existing

mkdir -p $BACKUP_TEMP_DIR

cd $WORDPRESS_SITE_PATH
#Dump sql file to $SQLFILE
mysqldump -u $DBUSER -p $DBNAME --password=$DBPASSWORD --skip-lock-tables --force >$SQLFILE
#Zip sql file
tar -zcvf $SQL_BACKUP_FILE $SQLFILE
#Remove sql file
rm -f $SQLFILE

#Cd to backup code folder
cd $PARENT_WORDPRESS_SITE
tar -zcvf $BACKUP_FILE_PATH $SITE_NAME

echo "Uploading to google drive"
cd $BACKUP_CODE
#UPload backup file to google drive
python backup.py configs/$BACKUP_CONFIG_FILE $BACKUP_FILE_PATH
#Remove backup file since file is uploaded to google drive
rm -f $BACKUP_FILE_PATH
#echo "Done"

cd $WORDPRESS_SITE_PATH
rm -f $SQL_BACKUP_FILE
