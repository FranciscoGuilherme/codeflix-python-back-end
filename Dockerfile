FROM python:3.10.2-slim

# ==========================
# -----[Container user]-----
# ==========================

RUN useradd -ms /bin/bash python

USER python

# ====================================
# -----[Container specifications]-----
# ====================================

WORKDIR /home/python/app

# ===============================
# -----[Keep application up]-----
# ===============================

CMD [ "tail", "-f", "/dev/null" ]
