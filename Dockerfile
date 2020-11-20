# Build backend
FROM mildblue/cee-hacks-2020-base AS backend-build
LABEL description="CEE Hacks 2020 backend"
LABEL project="mildblue:cee-hacks-2020-images-backend"

WORKDIR /app

# Install dependencies
COPY conda.yml .
RUN conda env create -f conda.yml
# Register conda in the .bashrc
RUN conda init bash

# Do all your magic from here
# Copy rest of the app
COPY backend ./backend
RUN mkdir -p /logs

# Create version file
ARG release_version=development-docker
ENV RELEASE_FILE_PATH=./release.txt
RUN echo $release_version > $RELEASE_FILE_PATH

# Start the app - one must initialize shell beforehand
CMD . ~/.bashrc && \
    conda activate breviary && \
    gunicorn --bind 0.0.0.0:8080 backend.app:app --preload