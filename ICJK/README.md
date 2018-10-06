admin password is icjkifb299

## To install Mysql
1. Download MySQL from orcale
https://dev.mysql.com/downloads/mysql/

2. You will need to set a path to mysql binary
- edit the .bashrc (or my case .zshrc) and add
export PATH=$PATH:/usr/local/mysql/bin

3. Install the python MySQL connector
pip install mysqlclient django
- OR if you have python3 from Anaconda instead you do
conda install mysqlclient django
(conda install -c bioconda mysqlclient django) This is the exact command that actually worked for me
- you might then need to reinstall Django because Anaconda messes up the pathing
conda install django

4. You need to manually make the database (Django migrate will make the tables)
mysqladmin -u root -p create icjkdatabase

5. Modify the ICJK/settings.py in the DATABASES section
https://medium.com/@bencleary/django-mysql-for-windows-528272b3169b
- For security, set a environment varible with your password
export MYSQL_PASSWORD=**********

6. Prepair the database migration (You only need to do this if the DB has changed)
python3 manage.py makemigrations

7. Create the DB in MySQL
python3 manage.py migrate 

8. Need to import the data into the database manually
- First start the python shell that has hooks into the database
python3 manage.py shell
- Copy everything in the file import.py  
CTRL-A then CTRL-C
- Paste everything into the python shell
CTRL-V
Press enter 2 times (process may take ~5 seconds)

9. Test the data is there, in the shell type
Store.objects.all().values()
- You should see a bunch of data (will be truncated)
- If you want you can look at the 3 other tables also
- Or you could install MySQL Workbench, but you on your own for that one :)