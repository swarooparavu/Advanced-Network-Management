#!/bin/sh
cp trapDaemon.py /home/
cp trapDaemon.sh /home/
cp ../db.conf /home/
chmod a+rwx /home/trapDaemon.py
chmod a+rwx /home/trapDaemon.sh
/usr/bin/python backend.py
