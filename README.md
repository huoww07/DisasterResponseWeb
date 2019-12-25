# DisasterResponseWeb

## Table of Contents
  1. Installation and instructions to run
  2. Project description
  3. File description
  4. Summary of results
  5. Licensing, Acknowledgements

## Installation and instructions
The code does not require installation. It runs using python3. Required libraries to run the code (installation via: pip install library_name) include: pandas, numpy, langdetect, pycountry, sklearn, json, plotly, nltk, flask, sqlalchemy. Instructions to run:
    - To run ETL pipeline that cleans data and stores in database, go to 'data' folder and run below:
        `python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves, go to 'models' folder and run below:
        `python train_classifier.py ../data/DisasterResponse.db classifier.pkl`
    - Run the following command in the 'app' folder to start up the web locally:
        `python run.py`

## Project description
The project aims to build a web tool to predict if a message contains  

## File description


## Summary of results



## Licensing, Acknowledgements
Licensing: Feel free to use the code here as you would like! Comments and suggestions are welcome!
Acknowledgement: Thanks to Udacity course instructors.  
