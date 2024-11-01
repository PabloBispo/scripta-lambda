FROM python:3.11-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.4.29 /uv /uvx /bin/

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.cargo/bin/:$PATH"




# Copy function code
ADD . /${LAMBDA_TASK_ROOT}

WORKDIR /${LAMBDA_TASK_ROOT}

RUN uv sync --frozen

ENV PATH="/${LAMBDA_TASK_ROOT}/.venv/bin:$PATH"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_function.handler" ]