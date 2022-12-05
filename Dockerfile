FROM python:3.11.0
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy
COPY . .
RUN chmod +x entrypoint.sh
CMD ./entrypoint.sh
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

