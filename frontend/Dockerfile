FROM node:18

LABEL authors="ronylitv"

ARG UID=2000
ARG GID=2000

ENV UID=${UID}
ENV GID=${GID}

RUN groupadd -g $GID docker_user \
    && useradd -m -u $UID -g docker_user docker_user

USER docker_user

WORKDIR /home/docker_user/app

COPY package.json package.json
RUN npm install

COPY . .

EXPOSE 9000
EXPOSE 8000

ENTRYPOINT ["npx", "webpack", "serve"]
