#! /bin/bash
KEYPATH="./keys/local_test_rsa"

if [ ! -f "$KEYPATH" ] ; then
	echo "Generating key pair"
	ssh-keygen -b 4096 -t rsa -N '' -C 'demokey' -f $KEYPATH
fi
echo "Building docker container"
cp ./keys/local_test_rsa.pub ./docker-ssh/local_test_rsa.pub
cd docker-ssh
docker build -t "local:ubuntu-14.04-ssh" ./
cd ../
rm ./docker-ssh/local_test_rsa.pub

KEYS=$(docker run --rm local:ubuntu-14.04-ssh /opt/list_keys.sh)
IFS=$'\r\n'
XKEYS=($KEYS)
declare -a NR
for i in ${KEYS[@]}; do
	LINE=$(echo $i | awk -F ' ' '{print substr($4,2,length($4)-2)"::"$2}')
	NR+=($LINE)
done
L=$(IFS=$","; echo "${NR[*]}")

docker run -d --name ssh-test local:ubuntu-14.04-ssh

INIP=`docker inspect ssh-test | sed  -n "s/ *\"IPAddress\": \"\([0-9\.]*\)\",/\1/p"`
sed -e "s/public-keys=.*/public-keys=$L/" -e "s/host=.*/host=$INIP/" config/config.cfg > config/config-new.cfg
rm config/config.cfg
mv config/config-new.cfg config/config.cfg
echo "Setting up server. This may take a while."
python setup-server.py -c config/config.cfg -s local-test

echo "The app should be available from your browser at http://$INIP/demoapp/"
