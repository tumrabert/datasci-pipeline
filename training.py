import pandas as pd
import os
from sentence_transformers import SentenceTransformer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import logging
def get_paper_string(x):

    x_na = x.isna()
    EMPTY_ABSTRACT = x_na["abstracts"]
    EMPTY_DESCRIPTION = x_na["description"]

    if (EMPTY_ABSTRACT) and (EMPTY_DESCRIPTION):
        return "Researchers wrote a paper with an empty abstract and an empty description."
    elif (EMPTY_ABSTRACT):
        return "Researchers wrote a paper with an empty abstract With the following description: "+x["description"]
    elif (EMPTY_DESCRIPTION):
        return "Researchers wrote a paper with the following abstract: "+ x["abstracts"]+"\n with no additional description"

    else:
        return ("Researchers wrote a paper with the following abstract: "+ x["abstracts"]+"\n with the following description: "+x ["description"]

    )
def training(cursor):
    df = pd.DataFrame(list(cursor))
    table=df.copy()
    dataset = table.apply(get_paper_string,axis=1)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    vectors = model.encode(dataset)
    tsne = TSNE(random_state=42, n_iter=1000)

    embeddings = tsne.fit_transform(vectors)
    kmeans = KMeans(n_clusters=20, random_state=42, n_init="auto")

    cluster = kmeans.fit_predict(vectors)

    table["cluster"] = cluster
    table["x"] = embeddings[:,0]
    table["y"] = embeddings[:,1]
    new_df= table[[ '_id','cluster','x','y']]
    return new_df.to_dict(orient='records')
def get_paper_string(x):

    x_na = x.isna()
    EMPTY_ABSTRACT = x_na["abstracts"]
    EMPTY_DESCRIPTION = x_na["description"]

    if (EMPTY_ABSTRACT) and (EMPTY_DESCRIPTION):
        return "Researchers wrote a paper with an empty abstract and an empty description."
    elif (EMPTY_ABSTRACT):
        return "Researchers wrote a paper with an empty abstract With the following description: "+x["description"]
    elif (EMPTY_DESCRIPTION):
        return "Researchers wrote a paper with the following abstract: "+ x["abstracts"]+"\n with no additional description"

    else:
        return ("Researchers wrote a paper with the following abstract: "+ x["abstracts"]+"\n with the following description: "+x ["description"]

    )
def training(cursor):
    try:
        df = pd.DataFrame(list(cursor))
        table = df.copy()
        dataset = table.apply(get_paper_string, axis=1)

        model = SentenceTransformer("all-MiniLM-L6-v2")

        vectors = model.encode(dataset)
        tsne = TSNE(random_state=42, n_iter=1000)

        embeddings = tsne.fit_transform(vectors)
        kmeans = KMeans(n_clusters=20, random_state=42, n_init="auto")

        cluster = kmeans.fit_predict(vectors)

        table["cluster"] = cluster
        table["x"] = embeddings[:,0]
        table["y"] = embeddings[:,1]
        new_df = table[['_id', 'cluster', 'x', 'y']]
        return new_df.to_dict(orient='records')
    except Exception as e:
        logging.error(f'Unexpected error in training: {str(e)}')
        return []
    
    