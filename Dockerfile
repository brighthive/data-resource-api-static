FROM python:3.7.2-slim
WORKDIR /data-resource-api
ADD schema schema
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN pip install pipenv && pipenv install --system
ADD data_resource_api data_resource_api
ADD cmd.sh cmd.sh
RUN chmod a+x cmd.sh
EXPOSE 8000
CMD [ "/data-resource-api/cmd.sh" ]
