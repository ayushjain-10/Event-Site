# Events App

To run this code, start by cloning this repository to your computer. Then in a terminal, navigate to the project folder.

To install dependencies, run:

```
pip3 install -r requirements.txt
```

Then rename the `.env.example` file as `.env`:

```
cp .env.example .env
```

Then you can run the server:

```
python3 app.py
```

## Dockerfile

1. Build the Image - 
`docker build -t flask-image .`

2. Run the Container -
`docker run -p 5000:5000 --rm --name flask-container flask-image`

3. Go to localhost:5000