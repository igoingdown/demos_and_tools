#!/usr/bin/python3

"""
===============================================================================
author: 赵明星
desc:   lda包demo。
===============================================================================
"""

import numpy as np
import lda
import lda.datasets


def lda_test():
    X = lda.datasets.load_reuters()
    vocab = lda.datasets.load_reuters_vocab()

    print("X.shape = {}".format(X.shape))
    print("X.sum = {}".format(X.sum()))

    model = lda.LDA(n_topics=20, n_iter=1000, random_state=1)
    model.fit(X)

    topic_word = model.topic_word_
    n_top_word = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_word+1):-1]
        print("topic {0}:{1}".format(i, ''.join(topic_words)))


if __name__ == "__main__":
    lda_test()
