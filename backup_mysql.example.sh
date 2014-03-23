BACKUP_DIR="/your/backup/folder"
BACKUP_CODE="/backup/code/folder"
#Sql file name with year-month-date-hour-minute
NAME=`date +%Y%m%d-%H%M`
SQLFILE=$NAME'.sql'
ZNAME=$NAME'.tar.gz'

FILE_PATH=$BACKUP_DIR'/'$ZNAME

DBNAME='your_db_name'
DBUSER='mysql_user'
DBPASSWORD='mysql_password'
echo "Dumping DB name=$DBNAME"
#Create backup folder if folder is not existing
mkdir -p $BACKUP_DIR
cd $BACKUP_DIR
#Dump sql file to $SQLFILE
mysqldump -u $DBUSER -p $DBNAME --password=$DBPASSWORD --skip-lock-tables --force >$SQLFILE
#Zip sql file
tar -zcvf $ZNAME $SQLFILE
#Remove sql file
rm -f $SQLFILE
#Cd to backup code folder
cd $BACKUP_CODE
echo "UPloading to google drive"
#UPload backup file to google drive
python backup.py configs/dethoima.com.json $FILE_PATH
#Remove backup file since file is uploaded to google drive
rm -f $FILE_PATH
echo "Done"

