# Use an official Python image as the base
FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt .

# Install Python dependencies
RUN pip3 install \
    --no-cache-dir \
    -r requirements.txt \
    --target "${LAMBDA_TASK_ROOT}"

# Copy the current directory contents into the container
COPY ./app ${LAMBDA_TASK_ROOT}

# Set the default command to run when the container starts
CMD ["lambda.lambda_handler"]