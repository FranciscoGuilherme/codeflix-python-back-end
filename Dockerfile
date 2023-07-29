FROM python:3.10.2-slim

RUN apt update && apt install -y --no-install-recommends \
    git \
    zsh \
    curl \
    wget \
    default-jre \
    fonts-powerline

# ==========================
# -----[Container user]-----
# ==========================

RUN useradd -ms /bin/bash python

USER python

COPY ./docker/zsh/powerlevel10k/.p10k.zsh /home/python/.p10k.zsh

# ====================================
# -----[Container specifications]-----
# ====================================

WORKDIR /home/python/app

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PYTHONPATH=${PYTHONPATH}/home/python/app/src

# =============================
# -----[Instalacao do zsh]-----
# =============================

RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" \
    -p git \
    -p git-flow \
    -p https://github.com/zdharma-continuum/fast-syntax-highlighting \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -a 'export TERM=xterm-256color'

RUN echo '[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh' >> ~/.zshrc
RUN echo 'HISTFILE=/home/python/zsh/.zsh_history' >> ~/.zshrc

# ===============================
# -----[Keep application up]-----
# ===============================

CMD [ "tail", "-f", "/dev/null" ]
