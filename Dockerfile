FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    mediainfo \
    jq \
    python3 \
    python3-pip \
    inotify-tools \
    libvpl-dev \
    libmfx-dev \
    intel-media-va-driver-non-free \
    vainfo \
    wget \
    curl \
    libssl-dev \
    autoconf \
    automake \
build-essential cmake git libass-dev libbz2-dev libfontconfig-dev libfreetype-dev libfribidi-dev libharfbuzz-dev libjansson-dev liblzma-dev libmp3lame-dev libnuma-dev libogg-dev libopus-dev libsamplerate0-dev libspeex-dev libtheora-dev libtool libtool-bin libturbojpeg0-dev libvorbis-dev libx264-dev libxml2-dev libvpx-dev m4 make meson nasm ninja-build patch pkg-config tar zlib1g-dev curl libssl-dev clang libva-dev libdrm-dev

    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y build-essential pkg-config libc6-dev libssl-dev libexpat1-dev libavcodec-dev libgl1-mesa-dev qtbase5-dev zlib1g-dev


COPY scripts/ /opt/ripper/

RUN chmod +x /opt/ripper/*.sh

RUN /opt/ripper/install_makemkv.sh

RUN apt update && apt install -y git
RUN git clone https://github.com/HandBrake/HandBrake.git /opt/HandBrake 
RUN apt update && apt install -y WORKDIR /opt/HandBrake
RUN ./configure --enable-qsv --disable-gtk && cd build && make install

CMD ["/opt/ripper/worker.sh"]
