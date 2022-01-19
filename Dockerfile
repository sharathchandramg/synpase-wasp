FROM datamechanics/spark:3.2.0-latest

ENV PYSPARK_MAJOR_PYTHON_VERSION=3
WORKDIR /opt/application/

COPY ./dist/*.whl .

# Work around pip install trying to build from source, and gcc not found.
RUN conda install psutil
RUN pip3 install wasp-0.1.0-py3-none-any.whl

COPY ./wasp/jobs ./jobs/
