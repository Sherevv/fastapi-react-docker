FROM python:3.10-slim as backend

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app


# install dependencies
RUN pip install --upgrade pip
#RUN pip install --upgrade pip poetry
COPY requirements.txt .
#COPY poetry.lock pyproject.toml .
RUN pip install --upgrade -r requirements.txt
#RUN poetry install
#RUN pip install uvicorn

FROM node:16.14-alpine3.15 as frontend_dev

WORKDIR /app
COPY ./frontend/package.json ./
COPY ./frontend/yarn.lock ./

RUN yarn install

COPY ./frontend ./

RUN yarn build


FROM nginx:1.21-alpine as frontend_prod

RUN rm -rf /usr/share/nginx/html/*
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
COPY --from=frontend_dev /app/dist /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]




