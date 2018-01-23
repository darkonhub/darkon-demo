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
from cifar10_input import *

import numpy as np
import json

maybe_download_and_extract()
_, train_label = prepare_train_data(padding_size=0)

_cifar10_classes = (
    'airplane',
    'automobile',
    'bird',
    'cat',
    'deer',
    'dog',
    'frog',
    'horse',
    'ship',
    'truck'
)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32) or isinstance(obj, np.float64) or isinstance(obj, np.float):
            return float(obj)
        if isinstance(obj, np.int32) or isinstance(obj, np.int64) or isinstance(obj, np.int):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


demo_indices = np.loadtxt('demo-50.txt').astype(np.int32)
prediction_results = np.loadtxt('pred.txt').astype(np.float32)

demo_database = list()
for i, key in enumerate(demo_indices):
    scores = np.loadtxt('diffs/diff-{}.txt'.format(key))
    sorted_indices = np.argsort(scores)

    d = dict()
    d['key'] = key
    d['class_id'] = int(i / 5)
    d['pred'] = list(prediction_results[i])
    d['helpful'] = list(sorted_indices[-10:][::-1])
    d['harmful'] = list(sorted_indices[:10])

    d['helpful_meta'] = list(train_label[d['helpful']])
    d['helpful_meta'] = map(lambda x: _cifar10_classes[int(x)], d['helpful_meta'])

    d['harmful_meta'] = list(train_label[d['harmful']])
    d['harmful_meta'] = map(lambda x: _cifar10_classes[int(x)], d['harmful_meta'])
    demo_database.append(d)

with open('demo_database.json', 'wt') as f:
    json.dump(demo_database, f, indent=4, cls=NumpyEncoder)
