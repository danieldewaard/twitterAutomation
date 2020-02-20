FROM python:3.7-alpine

COPY bots/twitterAutomation.py /bots/
COPY photos/ /photos/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "twitterAutomation.py"]