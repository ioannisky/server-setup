#! /bin/bash

keys=$(ls  /etc/ssh/*.pub)
for i in $keys; do
	ssh-keygen -l -f $i
done
