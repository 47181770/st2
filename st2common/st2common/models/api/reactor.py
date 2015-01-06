# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from st2common.util import isotime
from st2common.models.api.base import BaseAPI
from st2common.models.api.tag import TagsHelper
from st2common.models.db.reactor import SensorTypeDB, TriggerTypeDB, TriggerDB, TriggerInstanceDB

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class SensorTypeAPI(BaseAPI):
    model = SensorTypeDB
    schema = {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
                'default': None
            },
            'name': {
                'type': 'string',
                'required': True
            },
            'pack': {
                'type': 'string'
            },
            'description': {
                'type': 'string'
            },
            'artifact_uri': {
                'type': 'string',
            },
            'entry_point': {
                'type': 'string',
            },
            'trigger_types': {
                'type': 'array',
                'default': []
            },
            'poll_interval': {
                'type': 'number'
            }
        },
        'additionalProperties': False
    }


class TriggerTypeAPI(BaseAPI):
    model = TriggerTypeDB
    schema = {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
                'default': None
            },
            'name': {
                'type': 'string',
                'required': True
            },
            'pack': {
                'type': 'string'
            },
            'description': {
                'type': 'string'
            },
            'payload_schema': {
                'type': 'object',
                'default': {}
            },
            'parameters_schema': {
                'type': 'object',
                'default': {}
            },
            "tags": {
                "description": "User associated metadata assigned to this object.",
                "type": "array",
                "items": {"type": "object"}
            }
        },
        'additionalProperties': False
    }

    @classmethod
    def to_model(cls, triggertype):
        model = super(cls, cls).to_model(triggertype)
        model.pack = getattr(triggertype, 'pack', None)
        model.payload_schema = getattr(triggertype, 'payload_schema', {})
        model.parameters_schema = getattr(triggertype, 'parameters_schema', {})
        model.tags = TagsHelper.to_model(getattr(triggertype, 'tags', []))
        return model

    @classmethod
    def from_model(cls, model):
        triggertype = cls._from_model(model)
        triggertype['tags'] = TagsHelper.from_model(model.tags)
        return cls(**triggertype)


class TriggerAPI(BaseAPI):
    model = TriggerDB
    schema = {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
                'default': None
            },
            'name': {
                'type': 'string'
            },
            'pack': {
                'type': 'string'
            },
            'type': {
                'type': 'string',
                'required': True
            },
            'parameters': {
                'type': 'object'
            },
            'description': {
                'type': 'string'
            }
        },
        'additionalProperties': False
    }

    @classmethod
    def from_model(cls, model):
        trigger = cls._from_model(model)
        return cls(**trigger)

    @classmethod
    def to_model(cls, trigger):
        model = super(cls, cls).to_model(trigger)
        if hasattr(trigger, 'name') and trigger.name:
            model.name = trigger.name
        else:
            # assign a name if none is provided.
            model.name = str(uuid.uuid4())
        model.pack = getattr(trigger, 'pack', None)
        model.type = getattr(trigger, 'type', None)
        model.parameters = getattr(trigger, 'parameters', None)
        return model


class TriggerInstanceAPI(BaseAPI):
    model = TriggerInstanceDB
    schema = {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string'
            },
            'occurrence_time': {
                'type': 'string',
                'pattern': isotime.ISO8601_UTC_REGEX
            },
            'payload': {
                'type': 'object'
            },
            'trigger': {
                'type': 'string',
                'default': None,
                'required': True
            }
        },
        'additionalProperties': False
    }

    @classmethod
    def from_model(cls, model):
        instance = cls._from_model(model)
        instance['occurrence_time'] = isotime.format(instance['occurrence_time'], offset=False)
        return cls(**instance)

    @classmethod
    def to_model(cls, instance):
        model = super(cls, cls).to_model(instance)
        model.trigger = instance.trigger
        model.payload = instance.payload
        model.occurrence_time = isotime.parse(instance.occurrence_time)
        return model
