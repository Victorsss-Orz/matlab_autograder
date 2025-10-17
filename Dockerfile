FROM ubuntu:22.04
# FROM karthiksharma98/jupyter-octave:latest

# Needed to properly handle UTF-8
ENV PYTHONIOENCODING=UTF-8
ENV LANG=en_US.UTF-8

COPY install.sh /
COPY --chmod=777 grader /grader
RUN /bin/bash /install.sh