FROM ubuntu:21.10
ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./kook/ /kook
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    imagemagick
RUN python3 -m pip install -r /kook/requirements.txt 
CMD python3 /kook/main.py 
