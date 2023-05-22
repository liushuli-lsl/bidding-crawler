# 基础镜像
FROM python:3.8

#
COPY . /app

# 设置 app 目录为工作目录
WORKDIR /app

# 设置环境变量
ENV MYSQL_HOST = 'localhost'
ENV MYSQL_PORT = '3306'
ENV MYSQL_USER = 'root'
ENV MYSQL_PASSWORD = 'root'
ENV MYSQL_DB = 'source'
ENV PAGE_WAIT_INTERVAL = '2'

# 安装 python 依赖支持
RUN pip3 install -r requirements.txt

# 不知道干啥用
# VOLUME ["/app/proxypool/crawlers/private"]

# 
# CMD ["supervisord", "-c", "supervisord.conf"]

# 启动程序
CMD ["python3", "-m", "crawler.scheduler"]