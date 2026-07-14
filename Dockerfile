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
    && rm -rf /var/lib/apt/lists/*

COPY scripts/ /opt/ripper/

RUN chmod +x /opt/ripper/*.sh

RUN /opt/ripper/install_makemkv.sh
RUN /opt/ripper/install_handbrake.sh

CMD ["/opt/ripper/worker.sh"]
