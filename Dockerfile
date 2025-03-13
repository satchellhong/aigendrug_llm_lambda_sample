FROM public.ecr.aws/lambda/python:3.9

# Install system dependencies
RUN pip3 install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy application files
COPY ./src/ ${LAMBDA_TASK_ROOT}/src/
COPY ./public/ ${LAMBDA_TASK_ROOT}/public/
COPY handler.py ${LAMBDA_TASK_ROOT}
COPY ./aws /root/.aws
COPY ./data/ ${LAMBDA_TASK_ROOT}/data/
COPY ./faiss_index/ ${LAMBDA_TASK_ROOT}/faiss_index/

# Set permissions
RUN chmod -R 755 ${LAMBDA_TASK_ROOT}

# Command to run the handler
CMD [ "handler.main" ]
