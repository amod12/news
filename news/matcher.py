# -*- coding: utf-8 -*-
#imp
import sqlite3 as sql

import nltk
import re

# from models import Places

nltk.download('omw-1.4')

import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer


class Matcher:

    def match_recommendation(self, indices, similarity, threshold=0.1):
        index = indices.index("news_id")
        sim_p = list(enumerate(similarity[index]))
        p_list = sorted(sim_p, key=lambda x : x[1], reverse=True)
        print('@@@@@')
        print(p_list)

        p_id = [x for x in p_list[1:] if x[1] > 0.01]  # Remove less similar news
        print('@@@@@')
        print(p_id)
        plc_lst = [x[0] for x in p_id]
        plc_ids = [indices[x] for x in plc_lst]
        return plc_ids

    def lemmatize(self, value):
        ret = []
        nltk.download("wordnet")

        lemmatizer = WordNetLemmatizer()
        for word in value:
            ret.append(lemmatizer.lemmatize(word))
        return " ".join(ret)

    def matcher(self, title):

        con = sql.connect("db.sqlite3")

        query = "SELECT * from news_news;"

        df = pd.read_sql(query, con)

        new_df = df[["title", "description", "id"]]
        arr = ["query", title, "news_id"]
        new_df.loc[len(new_df)] = arr




        new_df["content"] = new_df["description"].apply(
            lambda string: re.sub(r"\W+", " ", string).split(" ")
        )



        new_df["content"] = new_df["content"].apply(self.lemmatize)

        tkn = RegexpTokenizer(r"\w+")

        tfidf = TfidfVectorizer(
            stop_words="english", ngram_range=(1, 2), tokenizer=tkn.tokenize
        )

        tfidf_mat = tfidf.fit_transform(new_df["content"])

        tf_df = pd.DataFrame(
            tfidf_mat.toarray(), columns=tfidf.get_feature_names_out(), index=new_df["title"]
        )


        sim = cosine_similarity(tfidf_mat.toarray(), tfidf_mat.toarray())

        sim_df = pd.DataFrame(data=sim, index=new_df["title"], columns=new_df["title"])


        indices = pd.Series(new_df["id"])

        ind = indices.tolist()

        return self.match_recommendation(indices=ind, similarity=sim, threshold=0.5)


