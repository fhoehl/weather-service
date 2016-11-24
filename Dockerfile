FROM ubuntu:xenial

RUN apt-get update --fix-missing

RUN apt-get install -y \
    python \
    python-pip

RUN apt-get -y autoremove

EXPOSE 5000

COPY requirements.txt .

RUN pip2 install -r requirements.txt

ADD . weather

WORKDIR weather

RUN export TEST
RUN python2 setup.py test
RUN unset TEST

RUN python2 setup.py install

ENTRYPOINT ["python", "weather/run.py"]
