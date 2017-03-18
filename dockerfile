FROM python:2.7.13
MAINTAINER Your Name "pavana@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python","git_app.py"]
CMD ["http://github.com/pavanaachar/config-repo"]


