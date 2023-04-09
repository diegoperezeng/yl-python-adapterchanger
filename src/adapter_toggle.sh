#!/bin/bash
/usr/sbin/capsh --caps="cap_net_admin+ep cap_setuid,cap_setgid+ep" --keep=1 --user=$USER -- -c "exec python3 $(dirname "$0")/adapter_toggle.py"

