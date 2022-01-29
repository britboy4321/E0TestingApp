# Docker Container :  To do list
Python code interacts with MongoDB to give a unique front end used for coordinating containerised running of tests.  Also allows test execution, stores results, and
further functionality

Hosted on Azure (or locally).

Terraform IAC implemented.

OAUTH Security implemented.

Logging on Dynatrace.  Alerting on Dynatrace (and normal Github alerts)

This application currently does not allow anonymous login.  A valid github ID and password are required for 'read only'.  

In this version, write permissions are restricted to a list of hardcoded people (within app.py).

Advanced kubernetes to be implemented 


Getting Started

Docker image 1 (tag:  dave2): 
Gunicorn production environment, built using:
docker build --target production -f Dockerfile --tag dave2 .

Docker image 2 (tag:  davedev):
Flask development environment, built using:
docker build --target development -f Dockerfile --tag davedev .

Docker image 3 (tag:  test):
Flask test environment, built using:
docker build --target test --tag my-test-image .

## Prerequisities

Update .env (see .env.template for guidance)

To run locally, 

(poetry add oauthlib flask-login is recorded in pyproject.toml)

export FLASK_APP=todo_app/app.py

1)  For a security reason add this to .env file:

OAUTHLIB_INSECURE_TRANSPORT=1

then run:

In order to run this container you'll need 
1) Docker installed
2) A file, recommended called .env, that has at least below elements :

Minimum variable file:
# Flask server configuration.
FLASK_APP=app
FLASK_ENV=development

# Change the following values for local development.
SECRET_KEY=secret-key
key=   Enter value here                 NO LONGER REQUIRED (FROM OLDER VERSION)
mongopass = Enter mongo password here
Values from .env.template

#END OF FILE

Container Parameters
--env-file                   Recommended value:       .env 
-p                           Recommended value:       5000:5000
Image name                   Recommended value:       davedev or dave2

Docker image runs:  Examples:
RUN DEVELOPMENT ENVIRONMENT IMAGE:
docker run --env-file .env -p 5000:5000 davedev
RUN DEVELOPMENT ENVIRONMENT WITH BIND MOUNT FOR HOT RELOADING:
docker run --env-file .env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app davedev
RUN PRODUCTION ENVIRONMENT IMAGE:
docker run --env-file .env -p 5000:5000 dave2
RUN TESTS FOR APP:
docker run --env-file .env -p 5000:5000 my-test-image


RUNNING APP ON KUBERNETES - ensure secrets on pod:

kubectl create secret generic secret-key --from-literal=SECRET_KEY='xxxxxxxxxxx'
kubectl create secret generic client-id --from-literal=client_id='xxxxxxxxxxxxxxxxxxxxxxxxx'
kubectl create secret generic client-secret --from-literal=client_secret='xxxxxxxxxxxxxxxxxxxx'
kubectl create secret generic mongodb-connection-string --from-literal=MONGODB_CONNECTION_STRING='mongodb://xxxxxxxxxxxxxxxxxxxxxxxxxxx'

Authors.

Dave Rawlinson


ADDITIONAL:

To stop constantly being asked to provide client_id and client_secret on a manual terraform apply .. add secret file vv.tfvars:  syntax:


client_id = "xxxxxxxxxxxxxxxxxxx"
client_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
LOGGLY_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  

and run 

terraform apply -var-file="vv.tfvars"

(Suggestion .. add this to .gitignore  ... contains secrets)

EXTRA INFO:

poetry run flask run      <<< works to run local version (not dockerised)
docker build --target production -f Dockerfile --tag dave2 .        <<< works to BUILD docker image
docker run --env-file .env -p 5000:5000 dave2       <<< works to run docker image on local


docker container ls        SHOWS the container after it's been run
docker stop container_name   (eg vigilant_leakey )    STOP THE CONTAINER
app is e0testingapp   on cloud  at  http://e0testingapp3.azurewebsites.net/

e0testingapp.azurewebsites.net

To run tests:

docker run my-test-image .       << from base directory>>

To force MondoDB to run on cloud: uncomment these lines to app.py     Or to run Mondo in non-cloud, ensure these lines are commented

mongodb_connection_string = os.environ["MONGODB_CONNECTION_STRING"]    # FOR CLOUD - insert this line later, after LOCAL is running ok.
client = pymongo.MongoClient(mongodb_connection_string)
