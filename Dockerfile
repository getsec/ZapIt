FROM python:3.7-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

ENTRYPOINT ["python"]

CMD ["app.py"]

