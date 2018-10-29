import hug
from models import EpsilonGreedyOptimizer, StochasticGOptimizer#, #FTRL
import database
from hug.middleware import CORSMiddleware

from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

# Whats in a name
#http://www.derekruths.com/static/publication_files/LiuRuths_AM2013.pdf

"""Serves a directory from the filesystem using Hug.
try /static/a/hi.txt  /static/a/hi.html  /static/a/hello.html
"""
import hug

#Make List
vowels = list("aeiouy")
consonants = list("bcdfghjklmnpqrstvexz")
syllables = lambda w:len(''.join(" x"[c in"aeiouy"]for c in w.rstrip('e')).split())

model = SGDClassifier(loss="log")
dict2vec = Pipeline(
    steps=[
        ('vectorizer', DictVectorizer(sparse=False)),
        ('oh', OneHotEncoder(n_values=1e5, sparse=False))
        ]
)


#encoder = OneHotEncoder(sparse=False)
optimizer = StochasticGOptimizer()

def get_features(name):
    lookup = database.DB.execute_raw(
        """
            SELECT year, rank
            FROM names
            WHERE name=%s
            AND gender = "M"
        """, [name]
    )[0]

    features = {
        "name_length": len(name) # length
        , "consonants_count": sum(name.count(c) for c in consonants) # number of consonants
        , "vowels_count": sum(name.count(c) for c in vowels) #" number_of_vowels":
        , "syllables_count": syllables(name) # number of syllables
        , "year_popular": lookup["year"] # popular in year
        , "year_rank": lookup["rank"] # rank in ^ year
        , "letter_first": name[1] #  "first_letter":
        , "letter_last": name[-1] # "last_letter":
    }

    #for l in name:
    #    features["letter_"+l] = 1.

    #print(features)

    return features


#test_X = [
#    get_features("Alfred"),
#    get_features("Alfred")
#]
#
#test_Y = [1, 0]
#model.partial_fit(dict2vec.fit_transform(test_X), test_Y, classes=[0, 1])


def cors_support(response, *args, **kwargs):
    response.set_header('Access-Control-Allow-Origin', '*')

@hug.get('/', requires=cors_support)
def main(name, Y):
    Y = int(Y)
    X = get_features(name)

    p = model.partial_fit(dict2vec.fit_transform([X]), [Y], classes=[0, 1])
    database.DB.execute_raw(
        """
            UPDATE names
            SET label = %s
            WHERE name=%s
            AND gender = "M"
        """, [Y, name]
    )

    all_names = list(map(lambda x: get_features(x['name']), database.DB.execute_raw(
        """
            SELECT name
            FROM names
            WHERE label IS NULL
            AND gender = "M"
        """, []
    )))

    #print(all_names)
    #print(dict2vec.fit_transform(all_names))
    #x = [dict2vec.fit_transform(all_names)[0]]
    print(x)

    scores = model.predict_proba(x)



    next_choice, next_score = optimizer.pull(scores)

    return {
        "last": p,
        "next": next_choice,
        "score": round(next_score,3)
    }

@hug.get('/files/open', requires=cors_support)
def files_open(name):
    with open(name) as fh:
        file = {
            "content": fh.read()
        }
    return file