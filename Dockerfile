FROM public.ecr.aws/lambda/python:3.10

WORKDIR /app/

# Copy function code
COPY . /app/

ENV PYTHONPATH=/app/

RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_function.handler" ]