FROM tiangolo/uvicorn-gunicorn:python3.7

COPY . /app
RUN pip3 install --upgrade  --trusted-host pypi.org --trusted-host files.pythonhosted.org setuptools_scm
RUN pip3 install --upgrade  --trusted-host pypi.org --trusted-host files.pythonhosted.org pip setuptools
RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt