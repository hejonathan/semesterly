# Render image: same build as the root Dockerfile, plus production serving.
FROM node:22.18.0-bookworm

WORKDIR /code
RUN apt-get update && apt-get install -y python3-pip python3-venv && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt whitenoise==6.9.0

RUN corepack enable && corepack prepare yarn@1.22.22 --activate
COPY package.json yarn.lock /code/
RUN yarn config set registry https://registry.npmjs.org/ \
 && yarn config set network-timeout 600000 -g \
 && (yarn install --non-interactive || (sleep 5 && yarn install --non-interactive)) \
 && yarn add sass --force

COPY . /code/
COPY deploy/render/local_settings.py /code/semesterly/local_settings.py
COPY deploy/render/selfhost_middleware.py /code/selfhost_middleware.py

RUN yarn build && python3 manage.py collectstatic --noinput

ENV PYTHONUNBUFFERED=1
CMD sh -c "python3 manage.py migrate --noinput && gunicorn semesterly.wsgi -b 0.0.0.0:${PORT:-10000} -w 2 --timeout 120"
