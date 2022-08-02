

from Modell import Performancest


class NB:
    def __init__(self, train_df, test_df, class_col):
        self.class_vals_count = None
        self.DATA = None
        self.class_vals_prob = None
        self.train_df = train_df
        self.test_df = test_df
        self.class_col = str(class_col)

    def train(self, debug=False):
        # 1
        # Counting classification values

        if self.class_col not in self.train_df.columns:  # space fix
            if (self.class_col + ' ') in self.train_df.columns:
                self.class_col = self.class_col + ' '

        self.class_vals_count = dict(self.train_df[self.class_col].value_counts()) #first dict


        col_data = dict()#sec dict

        for col in self.train_df.drop(columns=self.class_col).columns:
            col_data[col] = set(self.train_df[col])
        if debug:
            print('# 1:\n', col_data, '\n')

        # 2
        # Initializing col_data as a base for the DATA dictionary

        for data in col_data:
            col_data[data] = dict(zip(col_data[data], [0] * len(col_data[data])))

        if debug:
            print('# 2:\n', col_data, '\n')

        # 3
        # Initializing DATA and dividing the DataFrame to sub DataFrames (for each classification value)
        import copy

        self.DATA = dict()
        sub_dfs = dict()

        classifiers = [classifier for classifier in set(self.train_df[self.class_col])]

        for i in range(len(classifiers)):
            self.DATA[classifiers[i]] = copy.deepcopy((dict(col_data)))
            sub_dfs[classifiers[i]] = self.train_df.loc[self.train_df[self.class_col] == classifiers[i]]

        if debug:
            print('# 3:\n', self.DATA, '\n')

        # 4
        # Setting relevant values in the data

        for classifier in self.class_vals_count:
            for col_title in self.DATA[classifier]:
                for value in self.DATA[classifier][col_title]:

                    # current df with relevant data:
                    sub_df = sub_dfs[classifier]

                    lap_const = 1
                    try:
                        self.DATA[classifier][col_title][value] = (sub_df[col_title].value_counts()[
                                                                       value] + lap_const) / (
                                                                          sum(self.class_vals_count.values()) + len(
                                                                      self.class_vals_count) * lap_const)
                    except:  # value not in the sub_df
                        self.DATA[classifier][col_title][value] = lap_const / (
                                sum(self.class_vals_count.values()) + len(self.class_vals_count) * lap_const)

        if debug:
            print('# 4:\n', self.DATA, '\n')

        # 5
        # Calculating probability for each value in classification column

        self.class_vals_prob = dict(self.train_df[self.class_col].value_counts())

        for key in self.class_vals_prob.keys():
            self.class_vals_prob[key] = self.class_vals_prob[key] / sum(self.class_vals_count.values())

        if debug: print('# 5:\n', 'classifications (before calculation): ', self.class_vals_prob, '\n')

        return self.test(self.train_df, self.class_col)  # @@@

    def classify(self, *args):
        alpha = 1  # Laplace parameter

        df = self.test_df.drop(columns=self.class_col)

        if len(args) != len(list(df.columns)):
            print("args: \n", args, "\n\nlen(args):\n", len(args))
            print("\n\nlist(df.columns): \n", list(df.columns), "\n\nlen(list(df.columns)): \n", len(list(df.columns)))
            raise Exception('inner func expected ' + str(len(df.columns)) +
                            ' values but got ' + str(len(args)) + ' values.\n'
                            + 'Expected values for following columns: '
                            + str(df.columns.tolist())[1:-1])

        temp = dict(self.class_vals_prob)

        for classifier in temp:
            cur_data = self.DATA[classifier]

            cols_list = df.columns.tolist()
            i = 0

            for arg in args:

                if str(arg) in cur_data[cols_list[i]]:
                    temp[classifier] *= cur_data[cols_list[i]][arg]

                elif str(arg + ' ') in cur_data[cols_list[i]]:
                    temp[classifier] *= cur_data[cols_list[i]][arg + ' ']

                else:
                    print("KeyError, received key '" + arg + " ', expected value for '" +
                          str(cols_list[i]) + "' to be in " + str(list(cur_data[cols_list[i]].keys())))
                    raise KeyError(arg)

                i += 1

        classification = max(temp, key=temp.get)
        return classification

    def test(self, data, class_col, debug=False):
        predictions = []
        for _, row in data.iterrows():
            args = list(row.drop(labels=class_col))
            predictions.append(self.classify(*args))

        real_classifications = data[class_col].tolist()

        if debug:
            print("Predictions: ", predictions, "\n", "Real Classifications: ", real_classifications)

        return Performancest(predictions, real_classifications)
