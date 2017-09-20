# base docker file
FROM index.docker.io/manmanli/base7:latest
MAINTAINER limanman<xmdevops@vip.qq.com>

# copy files
COPY idmap.conf /xm_workspace/xmcloud3.0/upgradeserver_lua/
COPY geoip.mmdb /xm_workspace/xmcloud3.0/upgradeserver_lua/
COPY manage.py /xm_workspace/xmcloud3.0/upgradeserver_lua/
COPY requirements.txt /xm_workspace/xmcloud3.0/upgradeserver_lua/
COPY upgradeserver_lua /xm_workspace/xmcloud3.0/upgradeserver_lua/upgradeserver_lua
COPY nginx.conf /etc/nginx/nginx.conf

# install envirment
RUN yum -y install epel-release
RUN yum -y install python-devel python-pip
RUN pip install -r /xm_workspace/xmcloud3.0/upgradeserver_lua/requirements.txt
RUN pip install https://github.com/darklow/django-suit/tarball/v2

# make log dirs
RUN mkdir -p /xm_workspace/xmcloud3.0/upgradeserver_lua/logs/nginx
RUN mkdir -p /xm_workspace/xmcloud3.0/upgradeserver_lua/logs/upgradeserver_lua

# supervisord
COPY supervisord.conf /etc/supervisord.conf 

# run settings
WORKDIR /xm_workspace/xmcloud3.0/upgradeserver_lua/
EXPOSE 8802
CMD ["supervisord"]
