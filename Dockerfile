FROM debian
MAINTAINER benasse <account@cicogna.fr>

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends python-requests python-flask python-concurrent.futures supervisor python-tz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD canal-flask.py /bin/
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000

CMD supervisord -e debug -c /etc/supervisor/conf.d/supervisord.conf
