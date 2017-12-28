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

import os
import sys
import json
import numpy as np
from scipy import misc

maybe_download_and_extract()

# test images
test_data, _ = read_validation_data_wo_whitening()
train_data, _ = prepare_train_data(padding_size=0)

with open(sys.argv[1]) as f:
    database = json.load(f)

test_indices = [row['key'] for row in database]
helpful_indices = [row['helpful'] for row in database]
harmful_indices = [row['harmful'] for row in database]

test_path = './test_images'
if not os.path.exists(test_path):
    os.makedirs(test_path)

train_path = './train_images'
if not os.path.exists(train_path):
    os.makedirs(train_path)

for idx in test_indices:
    sample = test_data[idx].astype(np.uint8)
    misc.imsave(os.path.join(test_path, '{}.png'.format(idx)), sample)

for ar in helpful_indices:
    for idx in ar:
        sample = train_data[idx].astype(np.uint8)
        misc.imsave(os.path.join(train_path, '{}.png'.format(idx)), sample)

for ar in harmful_indices:
    for idx in ar:
        sample = train_data[idx].astype(np.uint8)
        misc.imsave(os.path.join(train_path, '{}.png'.format(idx)), sample)
