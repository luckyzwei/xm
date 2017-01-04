#!/bin/sh

killall uwsgi
sleep 1
uwsgi --ini  /data/xm/mysite/mysite/xm.ini
