# 実験環境の作成

コンテナベースで実験環境を作成してある。
ドイツと日本はRTTが300ms程度なので、その環境で発生しうることを再現するための環境。

subを増やせばより他の問題も発生することが想定される。

```bash
# docker-composeでコンテナ群を立ち上げる
docker-compose up -d

# dockerコンテナのうちbrokerのコンテナに遅延を300ms発生させる
docker exec l-rabit tc qdisc add dev eth0 root netem delay 300ms

# pub用のコンテナに入って送信処理を始める

docker exec -it publisher bash

> python3 ./src/send.py

# sub用のコンテナに入って受信処理を始める.(自動で受信させたい場合はDockerfielのCMDを参照)

docker exec -it publisher bash

> python3 ./src/receive.py

```



