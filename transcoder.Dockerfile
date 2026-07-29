FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    autoconf \
    automake \
    build-essential \
    cmake \
    git \
    libass-dev \
    libbz2-dev \
    libfontconfig-dev \
    libfreetype-dev \
    libfribidi-dev \
    libharfbuzz-dev \
    libjansson-dev \
    liblzma-dev \
    libmp3lame-dev \
    libnuma-dev \
    libogg-dev \
    libopus-dev \
    libsamplerate0-dev \
    libspeex-dev \
    libtheora-dev \
    libtool \
    libtool-bin \
    libturbojpeg0-dev \
    libvorbis-dev \
    libx264-dev \
    libxml2-dev \
    libvpx-dev \
    m4 \
    make \
    meson \
    nasm \
    ninja-build \
    patch \
    pkg-config \
    tar \
    zlib1g-dev \
    curl \
    libssl-dev \
    clang \
    libva-dev \
    libdrm-dev \
    python3-grpcio \
    python3-grpcio-tools \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/HandBrake/HandBrake.git /opt/HandBrake 
WORKDIR /opt/HandBrake
RUN ./configure --enable-qsv --disable-gtk --launch && cd build && make install
