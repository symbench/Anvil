# Docker file for a slim Ubuntu-based Python3 image

FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev numpy-stl\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install numpy\
  && pip3 install --upgrade pip  \
  && pip3 install numpy kajiki parea


  # Install any extra things we might need
RUN apt-get update \
	&& apt-get install -y \
		sudo \
		wget \
        curl \
        freecad \
        nano \
		software-properties-common ;\
		rm -rf /var/lib/apt/lists/*

# Create a new user called foam
RUN useradd --user-group --create-home --shell /bin/bash anvil_user ;\
	echo "anvil_user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN curl -s https://dl.openfoam.com/add-debian-repo.sh | bash ;\
     apt-get -y install openfoam2112-default; \
     echo "source /usr/lib/openfoam/openfoam2112/etc/bashrc " >> /home/aimed_user/.bashrc; \
     echo "export OMPI_MCA_btl_vader_single_copy_mechanism=none" >> /home/aimed_user/.bashrc ;\
     echo "source /home/aimed_user/.bashrc" >> /home/aimed_user/.profile

# set the default container user to foam
USER aimed_user

WORKDIR /home/aimed_user/dexof_work

ADD ./dexof.tgz /home/aimed_user
ADD ./testcase.tgz /home/aimed_user
ADD ./docs.tgz /home/aimed_user

RUN  sudo chown -R aimed_user.aimed_user  /home/aimed_user/dex_of;\
     sudo chown -R aimed_user.aimed_user  /home/aimed_user/test_casestudy;\
     sudo chmod -R a+r  /home/aimed_user/dex_of /home/aimed_user/test_casestudy ;\
     chmod a+rx /home/aimed_user/dex_of/*.sh

ENTRYPOINT ["/bin/bash"]
