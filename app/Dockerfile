FROM python:3.12-slim

WORKDIR /app
COPY server.py index.html highlight.min.js latex.min.js ./
COPY fonts/ ./fonts/

ENV TOOLBOX_HOST=0.0.0.0
ENV TOOLBOX_PORT=8420
ENV TOOLBOX_ROOT=/toolbox

EXPOSE 8420

CMD ["python3", "server.py"]
