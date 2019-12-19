import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
from sklearn.externals import joblib
from sqlalchemy import create_engine


app = Flask(__name__)

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///Users/Wenwen/Software/github-repository/DisasterResponseWeb/data/Clean_entry_data.db')
df = pd.read_sql_table('data', engine)

# load model
model = joblib.load("../models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():

    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    # Second set of data
    # extract language data
    language_counts = df['language'].value_counts().sort_values(ascending=False)
    language_names = list(language_counts.index)

    # Third set of data
    # calculate total number of positive cases in training data
    pos_case = {}
    data = []
    for column in list(df.columns)[5:]:
        total = sum(df[df.loc[:,column]==1].loc[:,column])
        pos_case[column] = total
        data.append(total)
    pos_case_df = pd.DataFrame.from_dict(pos_case, orient='index', columns=['count']).sort_values(by='count', ascending=False)

    # create visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre",
                }
            }
        },
        # second set of data
        {
            'data': [
                Bar(
                    x=language_names,
                    y=language_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Languages',
                'yaxis': {
                    'title': "Count (log)",
                    'type': 'log'
                },
                'xaxis': {
                    'title': "Language",
                    'tickangle': 30
                }
            }
        },
      # third set of data
        {
            'data': [
                Bar(
                    x=list(pos_case_df.index),
                    y=list(pos_case_df['count'])
                )
            ],

            'layout': {
                'title': 'Total No. of Positive Cases in Training Dataset',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Case type",
                    'tickangle': 30
                }
            }
        }
    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '')

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[5:], classification_labels))

    # This will render the go.html Please see that file.
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
