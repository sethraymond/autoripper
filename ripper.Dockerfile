FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    build-essential \
    git \
    pkg-config \
    libc6-dev \
    libssl-dev \
    libexpat1-dev \
    libavcodec-dev \
    libgl1-mesa-dev \
    qtbase5-dev \
    zlib1g-dev \
    python3-grpcio \
    python3-grpcio-tools \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://www.makemkv.com/download/makemkv-oss-1.18.4.tar.gz --output makemkv.tar.gz && mkdir -p /opt/makemkv && tar xzf makemkv.tar.gz -C /opt/makemkv
WORKDIR /opt/makemkv/makemkv-oss-1.18.4
RUN ./configure && make && make install
