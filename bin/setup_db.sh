#!/bin/bash
SQL=$(cat schema/sql/db_gen.sql schema/sql/db_gen_users.sql)

read -s -p "Enter MySQL password: " MYSQL_PASS
echo ""

mysql -u root --password="$MYSQL_PASS" -e "$SQL"