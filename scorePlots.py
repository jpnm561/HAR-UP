"""
Created on Thu Sep  5 17:45:41 2019

@author: JosePablo
"""

import itertools
import matplotlib.pyplot as plt
import numpy as np

"""
Confusion matrix code taken from scikit-learn.org
https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
"""
def plot_confusion_matrix(cm,classes,normalize=True,title='Confusion matrix',cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:,np.newaxis]
    plt.imshow(cm,interpolation='nearest',cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks,classes,rotation=45)
    plt.yticks(tick_marks,classes)
    fmt = '.2f'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]),range(cm.shape[1])):plt.text(j,i,format(cm[i,j],fmt),
                                        horizontalalignment='center',
                                        color='white' if cm[i,j] > thresh else 'black')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

#Plots scores in a bar graph
def plotScore(arrays,
              cncpt,
              scores=['Accuracy','Precison','Recall','F1Score'],
              t_window=['1&0.5','2&1','3&1.5'],
              methods=['RF','SVM','KNN','MLP'],
              grid = False):
    labels = []
    for method in methods:
        for score in scores:
            labels.append(method + ' ' + score)
    for k in range(0,2):
        bars = []
        fig, ax = plt.subplots()
        xdata = np.arange(len(labels))
        width = 0.20
        for i in range(0,len(t_window)):
            tbar = []
            for l in range(0,len(arrays)):
                arr = arrays[l]
                for j in range(0,len(methods)):
                    tbar.append(arr[i][j][k])
            col = ax.bar(xdata + (i-1)*width, tbar, width, label=t_window[i])
            bars.append(col)
            # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Scores')
        title = ''
        if k == 0:
            title = 'Mean'
        else:
            title = 'Standard Deviation'
        ax.set_title(title +' '+cncpt)
        ax.set_xticks(xdata)
        ax.set_xticklabels(labels)
        
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        count = 1
        for bar in bars:
            ha = {'center': 'center', 'right': 'left', 'left': 'right'}
            offset = {'center': 0, 'right': 1, 'left': -1}
            if count == 1:
                xpos = 'left'
            elif count == 2:
                xpos = 'center'
            else:
                count = 0
                xpos = 'right'
            count += 1
            for rect in bar:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 3, height),
                            xytext=(offset[xpos]*2, 0.5),
                            textcoords="offset points",
                            ha=ha[xpos], va='bottom')
        
        fig.tight_layout()
        plt.xticks(rotation = 90)
        if grid:
            plt.grid()
        plt.figure()
        fig.savefig(cncpt+'//Score_'+title+'_'+cncpt+'.jpg',dpi=100,bbox_inches='tight')
        plt.close(fig)
