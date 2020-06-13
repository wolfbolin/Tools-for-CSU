#!/bin/bash
docker image prune -f
docker stop ncov_sign
docker rm ncov_sign
echo -e "\033[5;36mOrz 旧容器(镜像)已清理\033[0m"

time_now=$(date "+%m%d%H")
docker build -f Dockerfile --tag ncov_sign:"${time_now}" .
echo -e "\033[5;36mOrz 镜像重建完成\033[0m"

docker run -itd \
	--restart always \
	--name ncov_sign \
	-v $(pwd):/var/app \
	ncov_sign:"${time_now}"
echo -e "\033[5;36mOrz 镜像启动完成\033[0m"
docker ps -a
docker logs ncov_sign -f