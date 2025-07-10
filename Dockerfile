FROM debian:trixie

ARG vacask_version=0.3.0
ARG vacask_sha256sum=2f0c1369453e83fb1de1250ca2572601b6882ede40f63834f8664878494b4c58
ARG openvaf_version=0.3-31-gf47d557
ARG openvaf_sha256sum=9bc343d52e00529ddba452b90358cdd14da14ec7437d75dec2dbd621eda54bc8
ENV PATH=$PATH:/opt/openvaf
ENV PATH=/opt/venv/bin:$PATH

RUN apt-get update 
RUN apt-get install -y ngspice libngspice0-dev clang python3 python3-pip python3-venv

ADD --checksum=sha256:${vacask_sha256sum} https://codeberg.org/arpadbuermen/VACASK/releases/download/_${vacask_version}/vacask_${vacask_version}_amd64.deb .
RUN apt-get install -y ./vacask_${vacask_version}_amd64.deb 
RUN rm ./vacask_${vacask_version}_amd64.deb

ADD --checksum=sha256:${openvaf_sha256sum} https://fides.fe.uni-lj.si/openvaf/download/openvaf-reloaded-osdi_${openvaf_version}-linux_x64.tar.gz .
RUN mkdir /opt/openvaf 
RUN tar --directory=/opt/openvaf -xvf openvaf-reloaded-osdi_${openvaf_version}-linux_x64.tar.gz
RUN rm openvaf-reloaded-osdi_${openvaf_version}-linux_x64.tar.gz

COPY ./pyproject.toml /heracles-testbenches/pyproject.toml
RUN python3 -m venv /opt/venv
RUN pip3 install /heracles-testbenches

WORKDIR /heracles-testbenches