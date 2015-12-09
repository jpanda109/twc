FROM ubuntu
	RUN sudo apt-get -y install python-dev
	RUN sudo python -m pip install markovify
	RUN sudo python -m pip install requests
	RUN sudo python -m pip install flask
	RUN git clone https://github.com/jpanda109/twc.git
	RUN python server.py
