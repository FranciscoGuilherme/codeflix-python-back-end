FROM python:3.10.2-slim

ARG USER=python
ARG USER_HOME=/home/$USER

RUN apt update && apt install -y --no-install-recommends \
    git \
    zsh \
    curl \
    wget \
    fonts-powerline

# =============================================
# -----[Make entrypoint script executable]-----
# =============================================

COPY ./docker/entrypoint.sh $USER_HOME/entrypoint.sh

RUN chmod +x $USER_HOME/entrypoint.sh

# ===============================================
# -----[Python packages manager instalation]-----
# ===============================================

RUN pip install pdm

# ==========================
# -----[Container user]-----
# ==========================

RUN useradd -ms /bin/bash python
RUN chown $USER:$USER -R $USER_HOME

USER python

COPY ./docker/zsh/powerlevel10k/.p10k.zsh $USER_HOME/.p10k.zsh

# ====================================
# -----[Container specifications]-----
# ====================================

WORKDIR $USER_HOME/app

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PYTHONPATH=${PYTHONPATH}$USER_HOME/app/src
ENV MY_PYTHON_PACKAGES=$USER_HOME/app/__pypackages__/3.10

# =================================
# -----[oh-my-zsh instalation]-----
# =================================

RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" \
    -a 'export TERM=xterm-256color'

# ====================================
# -----[Plugins download for zsh]-----
# ====================================

RUN git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-${USER_HOME:-~/.oh-my-zsh}/custom}/plugins/zsh-completions && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-${USER_HOME:-~/.oh-my-zsh}/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git ${ZSH_CUSTOM:-${USER_HOME:-~/.oh-my-zsh}/custom}/plugins/fast-syntax-highlighting

# ======================================
# -----[Plugins activation for zsh]-----
# ======================================

RUN echo "source $USER_HOME/custom/plugins/zsh-completions/zsh-completions.plugin.zsh" >> $USER_HOME/.zshrc && \
    echo "source $USER_HOME/custom/plugins/zsh-autosuggestions/zsh-autosuggestions.plugin.zsh" >> $USER_HOME/.zshrc && \
    echo "source $USER_HOME/custom/plugins/fast-syntax-highlighting/fast-syntax-highlighting.plugin.zsh" >> $USER_HOME/.zshrc && \
    echo "[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh" >> $USER_HOME/.zshrc \

# ==============================
# -----[Other informations]-----
# ==============================

RUN echo "HISTFILE=/home/node/zsh/.zsh_history" >> $USER_HOME/.zshrc && \
    echo 'eval "$(pdm --pep582)"' >> $USER_HOME/.bashrc && \
    echo 'eval "$(pdm --pep582)"' >> $USER_HOME/.zshrc

# ===============================
# -----[Keep application up]-----
# ===============================

CMD [ "bash", "../entrypoint.sh" ]
