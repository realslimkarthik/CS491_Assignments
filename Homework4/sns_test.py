import pandas
import seaborn as sns


def main():
    sns.set_style('whitegrid')
    data = [['NB', 88.19, 'Training'], ['LOG', 97.46, 'Training'], ['NB', 64.54, '10 Fold CV'], ['LOG', 67.84, '10 Fold CV'], \
        ['NB', 71.03, 'Test'], ['LOG', 73.82, 'Test']]
    data_df = pandas.DataFrame(data, columns=['Classifier', 'Accuracy', 'Dataset'])
    ax = sns.barplot(x='Classifier', y='Accuracy', hue='Dataset', data=data_df)
    sns.plt.show()


if __name__ == '__main__':
    main()