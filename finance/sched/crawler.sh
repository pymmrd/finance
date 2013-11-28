#!/bin/sh
export PATH=$PATH:/usr/bin

#screen_shot_task
#pgrep [c]rawler.sh || python /var/www/wwwroot/finance/finance/bin/crawler.py >> /data/log/crawler.log 2>&1 &
ps aux | grep [crawler].py || python /var/www/wwwroot/finance/finance/bin/crawler.py >> /data/log/crawler.log 2>&1 &

