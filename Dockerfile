FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
WORKDIR $(pwd)

RUN pip install -r requirements.txt


RUN echo Working Dir: $(pwd)
RUN ls -lh
ENTRYPOINT [ "python" ]

CMD [ "app.py" ]