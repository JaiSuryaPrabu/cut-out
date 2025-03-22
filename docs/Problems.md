# Deployment Problems
## Docker
* I created the `dockerfile` for the python:3.12 base image with installing the dependencies using pip which leads to error of building the `sam2` package because it has `pyproject.yaml` based configurations
* Then updated the `dockerfile` to copy my virtual environment to the docker, the build is success but the runtime fails because the image is `debian` based, my OS is windows