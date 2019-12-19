import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def load_data(database_filepath):
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql("SELECT * from data", engine)
    X = df['message']
    Y = df[list(df.columns)[5:]]
    category_names = list(df.columns)[5:]
    return X, Y, category_names


def tokenize(text):
    from nltk.tokenize import word_tokenize
    text = word_tokenize(text)
    return text

def build_model():
    from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
    from sklearn.pipeline import Pipeline
    from sklearn.multioutput import MultiOutputClassifier
    from sklearn.ensemble import RandomForestClassifier

    pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', MultiOutputClassifier(RandomForestClassifier()))
            ])
    return pipeline

def evaluate_model(model, X_test, Y_test, category_names):
    from sklearn.metrics import f1_score
    y_pred = model.predict(X_test)
    f1scores = []
    for column in range(Y_test.shape[1]):
        y_test_array = np.array(Y_test.iloc[:,column])
        y_pred_array = np.array(pd.DataFrame(y_pred).iloc[:,column])
        score = f1_score(y_test_array, y_pred_array, average='weighted')
        f1scores.append(score)
        print(category_names[column], score)
    print('Average f1 score is ', np.mean(f1scores))


def save_model(model, model_filepath):
    import pickle
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
