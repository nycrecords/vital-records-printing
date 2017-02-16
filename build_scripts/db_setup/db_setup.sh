#!/usr/bin/env bash

# 1. Install Postgres 9.5
yum -y install rh-postgresql95

# 2. Autostart Postgres
chkconfig rh-postgresql95-postgresql on

# 3. Setup data directory for Postgres (store data from Postgres where it's not normally stored)
mkdir -p /data/postgres
# postgres user owns the created Postgres directory
chown -R postgres:postgres /data/postgres

# 4. Copy script (enable postgres commands in command line) to /etc/profile.d
cp /vagrant/build_scripts/db_setup/postgres.sh /etc/profile.d/postgres.sh
source /etc/profile.d/postgres.sh

postgresql-setup --initdb

# 5. Setup data directory (move data files into created Postgres data directory)
mv /var/opt/rh/rh-postgresql95/lib/pgsql/data/* /data/postgres/
rm -rf /var/opt/rh/rh-postgresql95/lib/pgsql/data
ln -s /data/postgres /var/opt/rh/rh-postgresql95/lib/pgsql/data
chmod 700 /var/opt/rh/rh-postgresql95/lib/pgsql/data

# 6. Setup Postgres Configuration
mv /data/postgres/postgresql.conf /data/postgres/postgresql.conf.orig
mv /data/postgres/pg_hba.conf /data/postgres/pg_hba.conf.orig

# 7. Copy configuration files from home directory (vagrant for vagrant, /export/local/project_name/ for DOITT)
cp /vagrant/build_scripts/db_setup/postgresql.conf /data/postgres/
cp /vagrant/build_scripts/db_setup/pg_hba.conf /data/postgres/
chown -R posgres:postgres /data/postgres

# 8. Create postgres key and certificates
openssl req \
       -newkey rsa:4096 -nodes -keyout /vagrant/build_scripts/db_setup/server.key \
       -x509 -days 365 -out /vagrant/build_scripts/db_setup/server.crt -subj "/C=US/ST=New York/L=New York/O=NYC Department of Records and Information Services/OU=IT/CN=vital_records_printing.nyc"
cp /vagrant/build_scripts/db_setup/server.crt /vagrant/build_scripts/db_setup/root.crt

cp /vagrant/build_scripts/db_setup/root.crt /data/postgres
chmod 400 /data/postgres/root.crt
chown postgres:postgres /data/postgres/root.crt
cp /vagrant/build_scripts/db_setup/server.crt /data/postgres
chmod 600 /data/postgres/server.crt
chown postgres:postgres /data/postgres/server.crt
cp /vagrant/build_scripts/db_setup/server.key /data/postgres
chmod 600 /data/postgres/server.key
chown postgres:postgres /data/postgres/server.key

ln -s /opt/rh/rh-postgresql95/root/usr/lib64/libpq.so.rh-postgresql95-5 /usr/lib64/libpq.so.rh-postgresql95-5
ln -s /opt/rh/rh-postgresql95/root/usr/lib64/libpq.so.rh-postgresql95-5 /usr/lib/libpq.so.rh-postgresql95-5

sudo service rh-postgresql95-postgresql start

# 9. Create postgres users
sudo -u postgres /opt/rh/rh-postgresql95/root/usr/bin/createuser -s -e developer
sudo -u postgres /opt/rh/rh-postgresql95/root/usr/bin/createuser -s -e vital_records_printing_db

# 10. Create database
sudo -u postgres /opt/rh/rh-postgresql95/root/usr/bin/createdb vital_records_printing

# 6. Add the following lines to /etc/sudoers file (allows running postgres commands without sudo access)
#vital_records_printing   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql start
#vital_records_printing   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql stop
#vital_records_printing   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql status
#vital_records_printing   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql restart
#vital_records_printing   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql condrestart
#vital_records_printing   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql try-restart
#vital_records_printing   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql reload
#vital_records_printing   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql force-reload
#vital_records_printing   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql initdb
#vital_records_printing   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql upgrade
