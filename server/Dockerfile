#Backend Dockerfile

#Python image to be used for container
FROM python:3.9-slim

#Working Directory
WORKDIR /app

#Copy all contents in current dir to work dir (/app)
COPY . /app

#install necessary packages from requirements.txt
#dont cache packages
RUN pip install --no-cache-dir -r requirements.txt

#Expose docker container using port 8080
EXPOSE 8080

#Run application
CMD ["python", "application.py"]