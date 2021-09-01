# Word Counter Application
This project is a FastAPI application to count how many words are in a text file.
To use it, submit a text file to receive the word count.
The submissions are stored in the database and can be retrieved filtering by filename and/or date range.

### Setup Instructions for Local Development
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

An interative auto-generated documentation provided by FastAPI will be availabe at **http://127.0.0.1:8000/docs**.


### Testing Instructions
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

### API Documentation
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