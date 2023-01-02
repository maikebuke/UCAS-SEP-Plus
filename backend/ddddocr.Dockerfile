FROM python:3.9.16

WORKDIR /workspace

ENV PIP_ROOT_USER_ACTION=ignore

RUN    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ddddocr==1.4.7 flask==2.1.0 flask-cors==3.0.10 \
    && echo "Docker Image ubuntu:16.04-build-env Build Successfully!"

CMD ["python", "main.py"]
