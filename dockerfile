FROM python:2.7.13
MAINTAINER Your Name "pavana@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["git_app.py"]

