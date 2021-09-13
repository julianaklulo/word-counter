# Word Counter Application
This project is a FastAPI application to count how many words are in a text file.
To use it, submit a text file to receive the word count.
The submissions are stored in the database and can be retrieved filtering by filename and/or date range.

### Setup instructions for local development
1. Clone this repository
```bash
$ git clone https://github.com/julianaklulo/word-counter.git
```
2. Move into the folder
```bash
$ cd word-counter/word_counter
```
3. Create the virtualenv and install the dependencies
```bash
$ poetry install
```
4. Add a database connection string to .env file (use local.env content if you want to use a SQLite database)
```bash
$ cp local.env .env
```
4. Start the application
```bash
$ poetry run uvicorn app.main:app --reload
```

The application will be available at **http://127.0.0.1:8000**.

An interative auto-generated documentation provided by FastAPI will be available at **http://127.0.0.1:8000/docs**.


### Testing instructions
The tests were written using `pytest`. To run, type
```bash
$ poetry run pytest
```


### Running the application using Docker
To run the application on a container, use the provided Dockerfile.

Instructions:
1. Move into the correct folder
```bash
$ cd word-counter
```
2. Build the image
```bash
$ docker build -t word-counter .
```
3. Run the image on a container
```bash
$ docker run -d --name wordcounter -p 80:80 word-counter
```
4. By default it will use SQLite. If you want to use another database, pass the connection string as an env var
```bash
$ docker run -d --name wordcounter --env DATABASE_URL=<connection string to the database here> -p 80:80 word-counter
```

The application will be available at **http://127.0.0.1** and the auto-generated documentation at **http://127.0.0.1/docs**.

### API documentation
Each submission has:
- ID (auto generated)
- Filename
- Timestamp
- Word count

#### Endpoints
Method | Endpoint | Description
-------| ---------| -----------
POST | **/word_counter** | Submit a file to be counted.
GET | **/word_counter** | Retrive all submissions.
GET | **/word_counter/?filename=[** filename to filter **]** | Filter submissions by filename.
GET | **/word_counter/?initial_timestamp=[** initial timestamp to filter **]&final_timestamp=[** final timestamp to filter **]** | Filter submissions by date range, from initial timestamp to final timestamp, both inclusive.
GET | **/word_counter/?filename=[** filename to filter **]&initial_timestamp=[** initial timestamp to filter **]&final_timestamp=[** final timestamp to filter **]** | Filter submissions both by filename and date range.

Payload for POST: *multipart/form-data*
```
{
    "file": <attach file to upload>
}
```

Timestamp format for filtering:
```
YYYY-MM-DD HH:MM:SS
```

#### Requests examples
To create a submission, send a text file (for example, file.txt):
```bash
$ curl --request POST \
  --url http://localhost:8000/word-counter \
  --header 'Content-Type: multipart/form-data' \
  --form file=@file.txt
```

The response should be:
```
{
    "filename": "file.txt",
    "timestamp": "2021-08-29T00:45:00.334998",
    "word_count": 4,
    "id": 1
}
```

To filter submissions using filename, pass the filename as a query param:
```bash
$ curl --request GET \
  --url 'http://localhost:8000/word-counter?filename=file.txt'
```

To filter submissions using date range, pass both initial and final timestamp as query params (URL encoded):
```bash
$ curl --request GET \
  --url 'http://localhost:8000/word-counter?initial_timestamp=2021-08-29%2000%3A00%3A00&final_timestamp=2021-08-29%2000%3A58%3A00&='
```

To filter submissions using both filename and date range:
```bash
$ curl --request GET \
  --url 'http://localhost:8000/word-counter?filename=file.txt&initial_timestamp=2021-08-29%2000%3A00%3A00&final_timestamp=2021-08-29%2000%3A58%3A00'
```


### Infrastructure as code
The infrastructure as a code is provided using Terraform. It creates a Kubernetes cluster in AWS and deploy the application inside the cluster using the Docker image available at Docker Hub (created using the provided Dockerfile).

The infrastructure contains:
* VPC module with subnets and availability zones
* PostgreSQL database using AWS RDS (with own its security group)
* Kubernetes cluster using AWS EKS (with its own security group)
* Deployment of application with load balancer

#### Deploying the application
Before deploying the application, make sure to have AWS CLI configured with your credentials.
You may also need `kubectl` to connect to the cluster and check the running services.

Instructions:
1. Move into the infrastructure folder
```bash
$ cd infrastructure
```
2. Set the database username and password as env vars (with `TF_VAR` as prefix):
```bash
$ export TF_VAR_database_username=<database_username>
$ export TF_VAR_database_password=<database_password>
```
3. Initialize the Terraform workspace
```bash
$ terraform init
```
4. Apply the configuration
```bash
$ terraform apply
```

After the deploy, the application IP will be printed on the terminal.

### Updating the deployed application
To update the application, make the changes to the source code and build the new Docker image. Add a new tag to the image and change the `deployment.tf` file to use the created tag. In the resource `kubernetes_deployment word-counter` update the image parameter. Example:

Before:
```
    image = "julianaklulo/word-counter:v1"
```

After
```
    image = "julianaklulo/word-counter:v2"
```

Then apply the configuration
```bash
$ terraform apply
```

The new code will be available at the application IP which will be printed on the terminal.
