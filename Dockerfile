# Use an official NVIDIA CUDA base image to support vLLM acceleration
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

# Set environment system variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1

# Install system dependencies including Python 3.11
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    python3.11-dev \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as the default python/pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Establish target application directory
WORKDIR /workspace

# Copy dependencies definitions first to optimize Docker layer caching
COPY pyproject.toml .

# Install dependencies using standard pip
RUN pip install --upgrade pip setuptools wheel && \
    pip install .

# Expose Jupyter Lab port (8888) and vLLM server port (8000)
EXPOSE 8888 8000

# Launch JupyterLab by default, accepting connections from any host without tokens for training simplicity
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
