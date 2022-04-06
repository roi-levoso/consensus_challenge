# install python in the container
FROM python:3.8.8-slim 
# copy the local requirements.txt file to the 
COPY ./requirements.txt requirements.txt
# install the packages from the requirements.txt file in the container
RUN pip install -r requirements.txt
# expose the port that uvicorn will run the app
EXPOSE 8000
# copy the local app/ folder to the /app fodler in the container
COPY . .
# set the working directory in the container to be the /app
# execute the command python main.py (in the WORKDIR) to start the app
CMD ["python", "main.py"]