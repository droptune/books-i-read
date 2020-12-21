# Books I Read

Simple [Flask](https://flask.palletsprojects.com/) app to track and review books that I am currently reading.

## Initializing application

```bash
cd /path/to/app
python -m venv .venv
source .venv/bin/activate
# install dependencies
pip install -r requirements.txt
export FLASK_APP=bir
flask init-db
# Add user account
flask add-user username password
```

![screenshot](https://user-images.githubusercontent.com/2103126/91102376-b7f1ee00-e671-11ea-84cc-fec0257dd5ba.png)
