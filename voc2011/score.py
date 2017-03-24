import numpy as np
import keras.backend as K


def get_confusion(a, b, n):
    """Compute the confusion matrix given two vectors and number of classes
    """
    k = (a >= 0) & (a < n)
    return np.bincount(n * a[k].astype(int) + b[k],
                       minlength=n**2).reshape(n, n)


def compute_error_matrix(y_true, y_pred):
    """ Compute Confusion matrix (a.k.a. error matrix)
    a       predicted
    c       0   1   2
    t  0 [[ 5,  3,  0],
    u  1  [ 2,  3,  1],
    a  2  [ 0,  2, 11]]
    l

    Note true positves are in diagonal
    """
    # Find channel axis given backend
    if K.image_data_format() == 'channels_last':
        ax_chn = 3
    else:
        ax_chn = 1
    classes = y_true.shape[ax_chn]
    confusion = np.zeros((classes, classes))
    confusion += get_confusion(y_true.argmax(ax_chn).flatten(),
                               y_pred.argmax(ax_chn).flatten(),
                               classes)
    return confusion


def accuracy(y_true, y_pred):
    confusion = compute_error_matrix(y_true, y_pred)
    # per-class accuracy
    acc = np.diag(confusion).sum() / float(confusion.sum())
    return acc


def mean_accuracy(y_true, y_pred):
    confusion = compute_error_matrix(y_true, y_pred)
    # per-class accuracy
    acc = np.diag(confusion) / confusion.sum(1)
    return np.nanmean(acc)


def mean_IU(y_true, y_pred):
    confusion = compute_error_matrix(y_true, y_pred)
    # per-class IU
    iu = np.diag(confusion) / (confusion.sum(1) + confusion.sum(0)
                               - np.diag(confusion))
    return np.nanmean(iu)


def freq_weighted_IU(y_true, y_pred):
    confusion = compute_error_matrix(y_true, y_pred)
    freq = confusion.sum(1) / float(confusion.sum())
    # per-class IU
    iu = np.diag(confusion) / (confusion.sum(1) + confusion.sum(0)
                               - np.diag(confusion))
    return (freq[freq > 0] * iu[freq > 0]).sum()