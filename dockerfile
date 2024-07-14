FROM node:14.16.0-alpine3.13 as base

# build python from source: https://stackoverflow.com/questions/62554991/how-do-i-install-python-on-alpine-linux
ARG PYTHON_VERSION=3.7.5

# install build dependencies and needed tools
RUN apk add \
    wget \
    gcc \
    g++ \
    make \
    zlib-dev \
    libffi-dev \
    openssl-dev \
    musl-dev

# download and extract python sources
RUN cd /opt \
    && wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \                                              
    && tar xzf Python-${PYTHON_VERSION}.tgz

# build python and remove left-over sources
RUN cd /opt/Python-${PYTHON_VERSION} \ 
    && ./configure --prefix=/usr --enable-optimizations --with-ensurepip=install \
    && make install \
    && rm /opt/Python-${PYTHON_VERSION}.tgz /opt/Python-${PYTHON_VERSION} -rf \
    && find /usr/lib -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name 'libpython*.a' \) \) \
		\) -exec rm -rf '{}' + \
	;


FROM base as builder

ADD . /code
WORKDIR /code
RUN yarn install
RUN yarn build


FROM base as runner

ADD ./dist /cats/dist
ADD ./app /cats/app
ADD requirements.txt /cats/requirements.txt
COPY --from=builder /code/dist /cats/dist

WORKDIR /cats

RUN pip3 install --no-cache-dir -r requirements.txt

RUN apk del \
    wget \
    gcc \
    g++ \
    make \
    zlib-dev \
    openssl-dev \
    musl-dev

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "--log-file", "-", "app:app"]
