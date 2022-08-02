

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
import pandas as pd
from Modell import save, DisplayKmeans


class Kmeans:
    def __init__(self):
        self.model = None

    def train(self, n_clusters):  # create our model and save it
        self.model = KMeans(n_clusters)
        save(self.model)

    def test(self, data, i, title):  # test the model
        encoder = make_column_transformer((OneHotEncoder(), data.columns), remainder="passthrough")
        data = encoder.fit_transform(data).toarray()
        pca = PCA(2)
        df = pca.fit_transform(data)
        label = self.model.fit_predict(df)

        return DisplayKmeans(label, df, i, title)
