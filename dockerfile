FROM python:3.7

ADD . /usr/ownlittleworld

WORKDIR /usr/ownlittleworld

COPY . .

RUN pip install pipenv && pipenv install --system --deploy

EXPOSE 8888:8888

CMD ["/bin/bash", "deploy/run.sh"]
