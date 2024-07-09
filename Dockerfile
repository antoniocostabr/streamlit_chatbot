# base image python 3.10 slim
FROM python:3.10-slim

# setting the working directory
WORKDIR /project

# copy the requirements file into the image
COPY requirements.txt .
# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Define the user number as a variable
ARG USER_ID=10001

# create a user to run the app as non-root, with the specified user number
RUN useradd -rm -d /project -s /bin/bash -g root -G sudo -u ${USER_ID} appuser

# copy the config file and give access to the non-root user
COPY config.yaml .
RUN chown ${USER_ID}:root config.yaml

# copy folder app to the image
COPY ./app /project/app

# make a temp_dir folder and give access to the non-root user
RUN mkdir temp_dir && chown -R ${USER_ID}:root temp_dir

# switch to non-root user
USER appuser

# expose port 8501
EXPOSE 8501

# command to run on container start
CMD ["streamlit", "run", "app/Home.py"]
