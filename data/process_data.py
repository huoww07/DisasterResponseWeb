import sys
import pandas as pd
import numpy as np
from langdetect import detect
import pycountry

def load_data(messages_filepath, categories_filepath):
    '''
    1. Extract data:
    Load training data, detect the language of each message and return it as a datafram.
    '''
    messages = pd.read_csv(messages_filepath)
    # detect language input
    names = []
    for row in list(messages.index):
        try:
            name = detect(messages.iloc[row, 2])
            lan = pycountry.languages.get(alpha_2=name).name
            names.append(lan)
        except:
            try:
                name = detect(messages.iloc[row, 1])
                lan = pycountry.languages.get(alpha_2=name).name
                names.append(lan)
            except:
                names.append('Undetermined')
    messages['language'] = names
    # read in categories and merge data
    categories = pd.read_csv(categories_filepath)
    df = messages.merge(categories, on=['id'])
    return df


def clean_data(df):
    '''
    2. Transform data:
    clean the training data so that the categories are separated and stored as categorical numeric format.
    duplicated input messages are dropped
    return the clean data as dataframe
    '''
    categories = df['categories'].str.split(";", expand=True)
    category_colnames = categories.iloc[1,:].apply(lambda x: x.split("-")[0])
    categories.columns = category_colnames
    for column in categories:
    # set each value to be the last character of the string
        categories[column] = categories[column].str.split("-").str.get(1)
    categories_numeric = categories.astype('int')
    df = pd.concat([df.drop('categories', axis=1), categories_numeric], axis=1)
    # remove duplicated entry
    df.drop_duplicates(inplace=True)
    return df

def save_data(df, database_filename):
    '''
    3. Load data:
    save the data as SQL database
    '''
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///'+database_filename)
    df.to_sql("data", engine, index=False, if_exists='replace')
    return None

def main():
    '''
    Run the ETL pipeline to clean data and save it in SQL database
    '''
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
