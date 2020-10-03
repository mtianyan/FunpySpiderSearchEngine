FROM python:3.7
ENV PYTHONUNBUFFERED 1

MAINTAINER mtianyan <mtianyan@qq.com>

ADD ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt update && apt -y install curl dirmngr ca-certificates\
	&& curl -sL https://deb.nodesource.com/setup_12.x | bash -\
	&& apt update\
	&& apt -y install gcc g++ make\
	&& apt -y install nodejs\
	&& curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -\
	&& echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list\
	&& apt update && apt install yarn

WORKDIR /PROJECT_ROOT