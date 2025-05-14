# 使用官方 Python 镜像作为基础镜像
FROM python:3.13

# 设置工作目录
WORKDIR /app

# 设置环境变量，防止 Python 生成 .pyc 文件，并使输出立即刷新
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 升级 pip
RUN pip install --upgrade pip

# 复制依赖文件并安装
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . /app/

# 暴露端口
EXPOSE 8000

# 启动 Django 开发服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]