FROM ubuntu:latest

WORKDIR /usr/src/app

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN apt update
RUN apt install -y python3 python3-pip python3-dev libopencv-dev libfreetype6-dev

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-m", "denmoni" ]
