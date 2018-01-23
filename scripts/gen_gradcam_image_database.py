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
from tensorflow.contrib.slim.nets import resnet_v1, vgg
import tensorflow.contrib.slim as slim
import cv2
import sys
import json
import os


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32) or isinstance(obj, np.float64) or isinstance(obj, np.float):
            return float(obj)
        if isinstance(obj, np.int32) or isinstance(obj, np.int64) or isinstance(obj, np.int):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


with open('imagenet_class.json', 'r') as f:
    class_id_to_label = json.load(f)

# load model
nbclasses = 1000
inputs = tf.placeholder(tf.float32, [1, 224, 224, 3])

model_name = sys.argv[1]
if model_name == 'resnet':
    check_point = 'test/data/resnet_v1_50.ckpt'
    with slim.arg_scope(resnet_v1.resnet_arg_scope()):
        net, end_points = resnet_v1.resnet_v1_50(inputs, nbclasses, is_training=False)
    pred_ts = end_points['predictions']
    feature_idx = -1
elif model_name == 'vgg':
    check_point = 'test/data/vgg_16.ckpt'
    with slim.arg_scope(vgg.vgg_arg_scope()):
        net, end_points = vgg.vgg_16(inputs, nbclasses, is_training=False)
        net = slim.softmax(net)
    pred_ts = net
    feature_idx = -2
else:
    raise Exception('unknown model name')

saver = tf.train.Saver(tf.global_variables())
sess = tf.InteractiveSession()
saver.restore(sess, check_point)

# darkon
target_op_name = darkon.Gradcam.candidate_featuremap_op_names(sess)[feature_idx]
prob_op_name = darkon.Gradcam.candidate_predict_op_names(sess, nbclasses)[-1]
insp = darkon.Gradcam(inputs, nbclasses, target_op_name, prob_op_name)

database = []
# database generation
for data_path in sys.argv[2:]:
    base_name = os.path.splitext(os.path.basename(data_path))[0]
    image = cv2.imread(data_path, cv2.IMREAD_COLOR)
    resized_image = cv2.resize(image, (224, 224))
    resized_image = resized_image.astype(np.float)

    scores = sess.run(pred_ts, feed_dict={inputs: [resized_image]})
    scores = scores.reshape(-1)
    rsorted_ret = np.argsort(scores)[::-1]

    d = dict()
    d['src'] = 'static/gradcam/' + os.path.basename(data_path)
    d['ret_gradcam'] = []
    d['ret_guided_gradcam'] = []
    for idx in rsorted_ret[:5]:
        ret = insp.gradcam(sess, resized_image, idx)
        path = 'static/gradcam/{}/{}/{}_'.format(model_name, base_name, idx)
        path_gradcam = path + 'gradcam.png'
        path_guided_gradcam = path + "guided_gradcam.png"

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        cv2.imwrite(path_gradcam, ret['gradcam_img'])
        cv2.imwrite(path_guided_gradcam, ret['guided_gradcam_img'])

        d['ret_gradcam'].append([path_gradcam, class_id_to_label[str(idx)], scores[idx]])
        d['ret_guided_gradcam'].append([path_guided_gradcam, class_id_to_label[str(idx)], scores[idx]])

    database.append(d)

with open('gradcam_{}_database.json'.format(model_name), 'w') as f:
    json.dump(database, f, indent=4, cls=NumpyEncoder)
