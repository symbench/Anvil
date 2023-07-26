FROM ubuntu:hirsute

USER root
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago
RUN apt-get update
RUN apt-get install -y apt-utils 2>/dev/null
RUN apt-get install -y tzdata
RUN apt-get dist-upgrade -y
RUN apt-get install -y freecad gmsh git nano python3-pip jupyter-notebook

EXPOSE 8888

RUN useradd --create-home ubuntu
USER ubuntu
WORKDIR /home/ubuntu
COPY --chown=ubuntu:ubuntu . /home/ubuntu
RUN pip3 install -e .
ENV PATH "$PATH:/home/ubuntu/.local/bin"

CMD ["jupyter-notebook", "--no-browser", "--ip=0.0.0.0"]
