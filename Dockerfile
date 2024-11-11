# Use the official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY environment.yaml .
RUN pip install --upgrade pip setuptools wheel
RUN pip install conda-pack
# Install mamba to handle the environment (optional, can be handled via conda-pack)
# Since we are using Conda environment inside Docker, it's better to use Miniconda
# Install Miniconda
ENV CONDA_DIR /opt/conda
RUN mkdir -p $CONDA_DIR
ENV PATH=$CONDA_DIR/bin:$PATH
RUN curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh && \
    bash miniconda.sh -b -p $CONDA_DIR && \
    rm miniconda.sh && \
    conda clean -ya

# Create the environment
COPY environment.yaml .
RUN conda env create -f environment.yaml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "playlette", "/bin/bash", "-c"]

# Activate the environment
ENV PATH /opt/conda/envs/playlette/bin:$PATH

# Install pip dependencies if any (otter-grader)
COPY environment.yaml .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose ports for Flask and Jupyter
EXPOSE 5000 8888

# Start both Flask and Jupyter using supervisord or another process manager
# For simplicity, we'll use a script to start both

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
