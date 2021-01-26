FROM python:3.7-slim
COPY . /app          
WORKDIR /app      
RUN apt-get update && apt-get install -y libmagic-dev libglib2.0-0
RUN apt install -y libgl1-mesa-glx 
RUN pip install -r requirements.txt
EXPOSE 5000   

ENV MODEL_NAME MyModel
ENV API_TYPE REST   
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0     

CMD exec seldon-core-microservice $MODEL_NAME $API_TYPE --service-type $SERVICE_TYPE --persistence $PERSISTENCE
