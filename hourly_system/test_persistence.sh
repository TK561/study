#\!/bin/bash
# Simple test to verify daemon persistence
sleep 10
ps -p $(cat /mnt/c/Desktop/Research/session_logs/persistent_daemon.pid) -o pid,ppid,cmd || echo 'Daemon stopped'

