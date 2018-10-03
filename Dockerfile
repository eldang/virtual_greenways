FROM jupyter/pyspark-notebook:latest

COPY ./requirements.txt ./
COPY virtual_greenways ./
RUN conda remove libgdal; \
    conda install -c conda-forge gdal libgdal; \
    pip install --update pip; \
    pip install -r requirements.txt; \
    jupyter nbextension enable --py widgetsnbextension
