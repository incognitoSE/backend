FROM python:3.7
COPY . .
RUN pip install -r requirements.txt --cache-dir=.pip_cache
EXPOSE 8000
EXPOSE 587
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]