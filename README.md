# server-setup
## What is it and how it works
This is a very basic server setup automation tool writen in python. It uses ssh to connect to a remote server and execute a set of instructions to setup the server. It is a work in progress but it can do some basic setup senarios.
## Depentencies
The only depentency other than python itself is the paramiko (http://www.paramiko.org/) library used for ssh connection handling. It is also good to have Docker install if you do not a spare server to test on.
## Run
You could run it using the command **python setup-server.py -c <path to config> -s <section of the config>**.
You could also run the demo script **build.sh** that creates a docker container, starts the ssh server and then runs the demo script that set-up a basic webserver with a Demo Application that does absolutly nothing.

