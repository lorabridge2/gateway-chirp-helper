FROM python:3.11-slim AS build

WORKDIR /home/chirp

# RUN apk add --no-cache gcc libc-dev g++
RUN pip install --no-cache-dir pipenv
COPY Pipfile* ./
RUN pipenv install --system --clear

# FROM python:3.11-alpine
# COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# WORKDIR /home/chirp

COPY . .

RUN mkdir /token && chown -R 1337:1337 /token
RUN mkdir /device && chown -R 1337:1337 /device

VOLUME /token /device

USER 1337:1337
ENTRYPOINT [ "python3", "chirp_helper.py"]
