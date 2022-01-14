#!/usr/bin/env bash

if ps aux | grep "[/]usr/bin/supervisord"; then
    echo "supervisor is running"
else
    echo "starting supervisor"
    sudo /usr/bin/supervisord -c /etc/supervisord.conf
fi