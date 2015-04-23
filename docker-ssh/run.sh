#! /bin/bash

# Print the keys of the ssh server
/opt/list_keys.sh
# Start ssh daemon
/usr/sbin/sshd -D
