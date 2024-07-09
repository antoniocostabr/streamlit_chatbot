# Tag for the Docker image
IMAGE_TAG = streamlit_chatbot

# Name of the container
CONTAINER_NAME = streamlit_chatbot_container

# Target to build the Docker image
build_image:
	docker build -t $(IMAGE_TAG) .

# Target to run the image, generating a container
run_image:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker run -p 8501:8501 --env-file .env --name $(CONTAINER_NAME) $(IMAGE_TAG)

# Target to stop the running container
stop_container:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Target to restart the Docker container
restart_container: stop_container
	docker run -p 8501:8501 --env-file .env --name $(CONTAINER_NAME) $(IMAGE_TAG)
