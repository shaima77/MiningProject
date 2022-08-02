
import numpy
from sklearn import tree
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

from Modell import save, Performancest


class id3tree:
    def __init__(self):
        self.target = None
        self.model = None
        self.encoder = None

    def train(self, data, target):  # create our model and save it

        self.target = target
        x = data.drop(columns=[self.target])
        y = data[self.target]
        self.encoder = make_column_transformer((OneHotEncoder(), x.columns), remainder="passthrough")
        x = self.encoder.fit_transform(x)
        if type(x) != numpy.ndarray:
            x = x.toarray()

        self.model = tree.DecisionTreeClassifier(criterion="entropy", max_depth=2).fit(x, y)
        save(self.model)

    def test(self, data):  # test the model

        x = data.drop(columns=[self.target])
        y = data[self.target]

        x = self.encoder.transform(x).toarray()
        z = self.model.predict(x)

        return Performancest(z, y)
