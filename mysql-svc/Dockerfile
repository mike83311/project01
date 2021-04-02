FROM library/mysql:5.7

# ARG uid=<uid>
# ARG gid=<gid>
# RUN groupadd -g $gid <user_name> && useradd -lm -u $uid -g $gid <user_name>
# USER <user_name>

# ADD custom/mycustom.cnf /etc/mysql/conf.d/
ADD init.sql /docker-entrypoint-initdb.d/