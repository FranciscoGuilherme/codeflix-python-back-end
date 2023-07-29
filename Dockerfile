FROM python:3.10.2-slim

RUN apt update && apt install -y --no-install-recommends default-jre

# ==========================
# -----[Container user]-----
# ==========================

RUN useradd -ms /bin/bash python

USER python

# ====================================
# -----[Container specifications]-----
# ====================================

WORKDIR /home/python/app

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PYTHONPATH=${PYTHONPATH}/home/python/app/src

# ===============================
# -----[Keep application up]-----
# ===============================

CMD [ "tail", "-f", "/dev/null" ]
