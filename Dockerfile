FROM python:3.10
# WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt

# FROM continuumio/miniconda3
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

# RUN conda create -c conda-forge -n pdf-chatbot python --file requirements.txt
# RUN echo "source activate env" > ~/.bashrc
# ENV PATH /opt/conda/envs/env/bin:$PATH
# RUN conda install --file /code/requirements.txt

RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

CMD ["panel", "serve", "/code/LangChain_QA_Panel_App.ipynb", "--address", "0.0.0.0", "--port", "7777"]

RUN mkdir .cache
RUN chmod 777 .cache
RUN mkdir .chroma
RUN chmod 777 .chroma