# DisasterResponseWeb

## Table of Contents
  1. Installation and instructions to run
  2. Project description
  3. File description
  4. Summary of results
  5. Licensing, Acknowledgements

## Installation and instructions
The code does not require installation. It runs using python3. Required libraries to run the code (installation via: pip install library_name) include: pandas, numpy, langdetect, pycountry, sklearn, json, plotly, nltk, flask, sqlalchemy.

## Project description
The project aims to build a web tool to predict if a message contains information related to natural disaster, including the report of a natural disaster and/or seeking help and/or offering help. The ETL pipeline takes in training data and build prediction model using random forest. The ML pipeline utilizes the previously built model to classify new messages. Both pipelines are wrapped into a web app and can be run locally.

## File description
1. 'data' directory contains training data and ETL pipeline written in python.
- To run ETL pipeline that cleans data and stores in database, go to 'data' folder and run below:
    `python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db`
2. 'models' directory contains ML pipeline written in python.
- To run ML pipeline that trains classifier and saves, go to 'models' folder and run below:
    `python train_classifier.py ../data/DisasterResponse.db classifier.pkl`
3. 'app' directory contains scripts to run a web app locally written in python.
- Run the following command in the 'app' folder to start up the web locally:
    `python run.py`
- Go to the website by entering the following in a web browser:
    http://0.0.0.0:3001/

## Summary of results
1. The home page of the web app provides the overview of the training data, in the aspects of message sources, message languages, and various types of natural disasters.
2. In the prediction panel, the user defined message will be classified to predict its relatedness to a natural disaster. The overall prediction accuracy is 93%.

## Licensing, Acknowledgements
Licensing: Feel free to use the code here as you would like! Comments and suggestions are welcome!
Acknowledgement: Thanks to Udacity Data Scientist Nanodegree program and instructors.  
