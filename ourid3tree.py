

import pandas as pd

from mathHelp import find_most_informative_feature
from Modell import save, Performancest, Display


class ourid3tree:
    def __init__(self, data, target):
        self.data = data
        self.testdata = None
        self.target = target
        self.tree = {}
        self.targetOp = None

    def train(self):
        self.targetOp = self.data[self.target].unique()

        def Subtree(col, dataa, class_list, Treedepth):  # create sub tree
            count_dict = dataa[col].value_counts(
                sort=False)  # Number of values in a column
            subtree = {}

            for col_value, count in count_dict.iteritems():  # We will go through each value
                coldata = dataa[
                    dataa[col] == col_value]
                if Treedepth < 2:  # continue to build
                    pass
                else:  # pruning tree by depth
                    subtree[col_value] = dataa[self.target].value_counts().idxmax()
                    dataa = dataa[dataa[col] != col_value]
                    continue

                NodeorNot = False
                for x in class_list:
                    class_count = len(coldata[coldata[self.target] == x])

                    if class_count == count:
                        subtree[col_value] = x
                        dataa = dataa[
                            dataa[col] != col_value]  # remove rows ( pure class)
                        NodeorNot = True
                if not NodeorNot:
                    subtree[col_value] = "?"  # set ? if need continue to build this col

            return subtree, dataa

        def make_tree(root, prev_feature_value, data, label, class_list, Treedepthh):  # create main tree
            if len(data) != 0:
                max_info_feature = find_most_informative_feature(data, label,
                                                                 class_list)
                tree, train_data = Subtree(max_info_feature, data,
                                           class_list, Treedepthh)

                if prev_feature_value is None:  # First round
                    root[max_info_feature] = tree
                    next_root = root[max_info_feature]

                else:
                    root[prev_feature_value] = dict()
                    root[prev_feature_value][max_info_feature] = tree
                    next_root = root[prev_feature_value][max_info_feature]

                for node, branch in list(next_root.items()):
                    if branch == "?": #need to continue
                        feature_value_data = data[
                            data[max_info_feature] == node]
                        Treedepthh = Treedepthh + 1
                        make_tree(next_root, node, feature_value_data, label,
                                  class_list, Treedepthh)

        Treedepth = 0
        make_tree(self.tree, None, self.data, self.target, self.targetOp, Treedepth)
        save(self.tree)
        return self.tree

    def test(self, testdata):
        self.testdata = testdata

        def predict(tree, subtree):
            if isinstance(tree, dict):
                if subtree[next(iter(tree))] in tree[next(iter(tree))]:
                    return predict(tree[next(iter(tree))][subtree[next(iter(tree))]], subtree)
                else:
                    return None
            else:
                return tree

        def evaluate():  # Summarizes the results of the model into an array

            resultList = []
            for w, y in self.testdata.iterrows():
                result = predict(self.tree, self.testdata.iloc[w])
                resultList.append(result)

            return resultList

        return Performancest(evaluate(), self.testdata[self.target])
