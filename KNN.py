
import numpy
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

from Modell import save, Performancest


class KNN:
    def __init__(self):
        self.model = None
        self.target = None
        self.encoder = None

    def train(self, data, target, k): # create our model and save it
        self.target = target
        x = data.drop(columns=[self.target])
        y = data[self.target]
        self.encoder = make_column_transformer((OneHotEncoder(), x.columns), remainder="passthrough")
        x = self.encoder.fit_transform(x)
        if type(x) != numpy.ndarray:
            x = x.toarray()
        self.model = KNeighborsClassifier(n_neighbors=k)
        self.model.fit(x, y)
        save(self.model)

    def test(self, data): # test the model
        x = data.drop(columns=[self.target])
        y = data[self.target]

        x = self.encoder.transform(x)
        z = self.model.predict(x)

        return Performancest(z, y)
