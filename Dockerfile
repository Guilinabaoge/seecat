FROM python:3.9.18-bullseye
WORKDIR /seecat 
COPY requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt 
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE 5000
COPY . . 
CMD ["/usr/bin/python3", "process_manager.py"]