#  Copyright 2020 Board of Trustees of the University of Illinois.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
import hmac
import logging
import uuid as uuidlib
import pdl_api.app.utils.jsonutils as jsonutils
import copy

from flask import request, g

import pdl_api.app.controllers.configs as cfg


def search():
    out_json = jsonutils.create_test_message()

    return out_json
