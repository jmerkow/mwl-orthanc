FROM jodogne/orthanc-python 
COPY orthanc.json /etc/orthanc/

RUN apt-get update && apt-get upgrade -y \
&& apt-get install -y apt-utils \
&& apt-get install -y build-essential cmake git pkg-config \
&& apt-get install -y libfreetype6 libfreetype6-dev

RUN apt-get install -y python3-pip python3-dev
RUN python3.7 -m pip install pip

RUN ln -s /usr/bin/python3.7 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip install httplib2


# Re-download some of the missing resources
RUN mkdir /code

# Add some useful files to have in the image
ADD resources /code
