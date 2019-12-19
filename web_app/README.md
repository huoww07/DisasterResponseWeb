# Disaster Response Pipeline Project

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

### Web deployment:
Build a virtual environment
1. pip install flask pandas plotly gunicorn
2. touch Procfile
  web gunicorn web_name:app
3. pip freeze > requirements
4. deployment using heroku
  curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
  # remove app.run() from worldbank.py
  # type cd web_app into the Terminal so that you are inside the folder with your web app code.
  heroku login
  git init
  git add .
  git commit -m ‘first commit’
  heroku create app_name
  git remote -v
  git push heroku master
