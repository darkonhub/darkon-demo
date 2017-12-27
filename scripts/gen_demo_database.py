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
import numpy as np
import json


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
    demo_database.append(d)

with open('demo_database.json', 'wt') as f:
    json.dump(demo_database, f, indent=4, cls=NumpyEncoder)
