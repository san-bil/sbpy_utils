import numpy as np
import sklearn.metrics as metrics

def generate_unblended_mclass_metrics(predictions_col, labels_col):

    precision_fh = lambda(tmp_confusionMat): np.diag(tmp_confusionMat)/np.sum(tmp_confusionMat,1);

    recall_fh = lambda(tmp_confusionMat): np.diag(tmp_confusionMat)/np.sum(tmp_confusionMat,0);

    f1Scores_fh = lambda(tmp_confusionMat): 2*(precision_fh(tmp_confusionMat)*recall_fh(tmp_confusionMat))/(precision_fh(tmp_confusionMat)+recall_fh(tmp_confusionMat));

    meanF1_fh = lambda(tmp_confusionMat): np.mean(f1Scores_fh(tmp_confusionMat));

    accuracy_fh = lambda(tmp_confusionMat): np.sum(np.diag(tmp_confusionMat))/np.sum(tmp_confusionMat);

    confusion_matrix = metrics.confusion_matrix(labels_col, predictions_col)
    accuracy = accuracy_fh(confusion_matrix)
    precision = precision_fh(confusion_matrix)
    recall = recall_fh(confusion_matrix)
    f1Scores = f1Scores_fh(confusion_matrix)
    meanF1 = meanF1_fh(confusion_matrix)

    label_corr=np.corrcoef(predictions_col,labels_col)


    return {'label_corr':label_corr,
            'accuracy':accuracy, 
            'precision':precision, 
            'recall':recall, 
            'f1Scores':f1Scores, 
            'meanF1':meanF1, 
            'confusion_matrix':confusion_matrix}



