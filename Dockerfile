FROM ubuntu:21.10
ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./ /kook
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    tesseract-ocr-nld \
    imagemagick
RUN python3 -m pip install -r /kook/kook/requirements.txt 
CMD python3 /kook/kook/main.py 
