FROM python:3.9

RUN apt update -y
RUN apt install -y iproute2 iputils-ping net-tools dnsutils
CMD tc qdisc add dev eth0 root netem delay 100ms && tail -f /dev/null