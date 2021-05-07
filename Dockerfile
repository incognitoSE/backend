FROM python:3.7
COPY . .
ADD HouseEstimator/Model/houseestimator.zip HouseEstimator/Model
RUN pip install -r requirements.txt --cache-dir=.pip_cache
RUN unzip -u HouseEstimator/Model/houseestimator.zip -d HouseEstimator/Model 
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]