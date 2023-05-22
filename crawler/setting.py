# -*- coding: utf-8 -*-
from os.path import dirname, abspath, join
from environs import Env

env = Env()
env.read_env()


# MYSQL host
MYSQL_HOST = env.str('MYSQL_HOST', '127.0.0.1')
# MYSQL port
MYSQL_PORT = env.int('MYSQL_PORT', 3306)
# MYSQL user, if no user, set it to None
MYSQL_USER = env.str('MYSQL_USER', 'root')
# MYSQL password, if no password, set it to None
MYSQL_PASSWORD = env.str('MYSQL_PASSWORD', 'root')
# MYSQL db, if no choice, set it to 0
MYSQL_DB = env.str('MYSQL_DB', 'source')

# crawler every page wait interval, default 2 secs
PAGE_WAIT_INTERVAL = env.int('PAGE_WAIT_INTERVAL', 2)




