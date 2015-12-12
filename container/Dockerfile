FROM ubuntu:14.04
WORKDIR /cloud
ADD . /cloud
RUN sudo apt-get -y install wget python git
RUN wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
RUN sudo python get-pip.py
RUN sudo python -m pip install markovify
RUN sudo python -m pip install requests
RUN sudo python -m pip install flask
RUN git clone https://github.com/jpanda109/twc.git
