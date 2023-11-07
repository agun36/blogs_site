# base image
FROM python:3.11.6-alpine

# working directory inside container
WORKDIR /app

# copy requirement.txt file to working directory
COPY ./requirements.txt /app/requirements.txt

# The --no-cache-dir option tells pip to not save the downloaded packages locally, as that is only if pip was going to be run again to install the same packages, but that's not the case when working with containers
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the ./app directory inside the working directory.
COPY ./app /app

# run the uvicorn server in working directory
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
