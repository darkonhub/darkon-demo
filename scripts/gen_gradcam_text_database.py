# Copyright 2017 Neosapience, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
import darkon
import tensorflow as tf
import numpy as np
from tensorflow.contrib import learn
import sys
import json


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32) or isinstance(obj, np.float64) or isinstance(obj, np.float):
            return float(obj)
        if isinstance(obj, np.int32) or isinstance(obj, np.int64) or isinstance(obj, np.int):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


# load model
nbclasses = 2
model_name = sys.argv[1]

if model_name == 'text':
    vocab_path = "test/data/sequence/vocab"
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)

    checkpoint_file = "test/data/sequence/model-30000"
    saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))

    saver = tf.train.Saver(tf.global_variables())
    sess = tf.InteractiveSession()
    saver.restore(sess, checkpoint_file)

    graph = tf.get_default_graph()
    input_x = graph.get_operation_by_name("input_x").outputs[0]
    input_y = graph.get_operation_by_name("input_y").outputs[0]
    dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
    pred = graph.get_operation_by_name("output/predictions").outputs[0]
else:
    raise Exception('unknown model name')


dataset = [
    "it leaves little doubt that kidman has become one of our best actors .",
    "exposing the ways we fool ourselves is one hour photo's real strength .",
    "the lively appeal of the last kiss lies in the ease with which it integrates thoughtfulness and pasta-fagioli comedy .",
    "the movie is too amateurishly square to make the most of its own ironic implications .",
    "unfortunately , neither sendak nor the directors are particularly engaging or articulate .",
    "a zombie movie in every sense of the word--mindless , lifeless , meandering , loud , painful , obnoxious ."
]
x_test_batch = np.array(list(vocab_processor.transform(dataset)))
y_test_batch = [[1.0, 0.0]]


# darkon
target_op_name = darkon.Gradcam.candidate_featuremap_op_names(sess, feed_options={
    input_x: x_test_batch[:1], input_y: y_test_batch[:1], dropout_keep_prob: 1.0}, graph=graph)[-4]

prob_op_name = darkon.Gradcam.candidate_predict_op_names(sess, 2, feed_options={
    input_x: x_test_batch[:1], input_y: y_test_batch[:1], dropout_keep_prob: 1.0}, graph=graph)[-1]

insp = darkon.Gradcam(input_x, nbclasses, target_op_name, prob_op_name)

database = []
# database generation
for src, test_data in zip(dataset, x_test_batch):
    ret_pos = insp.gradcam(sess, test_data, feed_options={dropout_keep_prob: 1}, target_index=1)
    ret_neg = insp.gradcam(sess, test_data, feed_options={dropout_keep_prob: 1}, target_index=0)

    words = src.split()

    pred_val = sess.run(pred, feed_dict={input_x: [test_data], dropout_keep_prob: 1})[0]
    pred_val = 'neg' if pred_val == 0 else 'pos'

    d = dict()
    d['src'] = src
    d['pred'] = pred_val
    d['ret_gradcam'] = []
    for word, pos, neg in zip(words, ret_pos['heatmap'][0], ret_neg['heatmap'][0]):
        d['ret_gradcam'].append([word, pos, neg])

    database.append(d)

with open('gradcam_{}_database.json'.format(model_name), 'w') as f:
    json.dump(database, f, indent=4, cls=NumpyEncoder)
