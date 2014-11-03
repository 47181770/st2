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

import datetime

from st2common.models.db.reactor import (TriggerDB, TriggerTypeDB)
from st2common.models.api.reactor import TriggerAPI
from st2common.models.api.rule import RuleAPI
from st2common.persistence.reactor import (TriggerType, Trigger, Rule)
from st2common.services import triggers as TriggerService
from st2common.services.triggers import get_trigger_db
from st2common.util import reference
import st2reactor.container.utils as container_utils
from st2reactor.rules.matcher import RulesMatcher
from st2tests.base import DbTestCase


class RuleMatcherTest(DbTestCase):

    def test_get_matching_rules(self):
        self._setup_sample_trigger('st2.test.trigger1')
        trigger_instance = container_utils.create_trigger_instance(
            {'name': 'st2.test.trigger1', 'pack': 'dummy_pack_1'},
            {'k1': 't1_p_v', 'k2': 'v2'},
            datetime.datetime.utcnow()
        )
        trigger = get_trigger_db(trigger=trigger_instance.trigger)
        rules = self._get_sample_rules()
        rules_matcher = RulesMatcher(trigger_instance, trigger, rules)
        matching_rules = rules_matcher.get_matching_rules()
        self.assertTrue(matching_rules is not None)
        self.assertEqual(len(matching_rules), 1)

    def _setup_sample_trigger(self, name):
        trigtype = TriggerTypeDB()
        trigtype.name = name
        trigtype.pack = 'dummy_pack_1'
        trigtype.description = ''
        trigtype.payload_schema = {}
        trigtype.parameters_schema = {}
        TriggerType.add_or_update(trigtype)

        created = TriggerDB()
        created.name = name
        created.pack = 'dummy_pack_1'
        created.description = ''
        created.type = trigtype.get_reference().ref
        created.parameters = {}
        Trigger.add_or_update(created)

    def _get_sample_rules(self):
        rules = []

        RULE_1 = {
            'enabled': True,
            'name': 'st2.test.rule1',
            'trigger': {
                'type': 'dummy_pack_1.st2.test.trigger1'
            },
            'criteria': {
                'k1': {                     # Missing prefix 'trigger'. This rule won't match.
                    'pattern': 't1_p_v',
                    'type': 'equals'
                }
            },
            'action': {
                'ref': 'sixpack.st2.test.action',
                'parameters': {
                    'ip2': '{{rule.k1}}',
                    'ip1': '{{trigger.t1_p}}'
                }
            },
            'id': '23',
            'description': ''
        }
        rule_api = RuleAPI(**RULE_1)
        rule_db = RuleAPI.to_model(rule_api)
        trigger_api = TriggerAPI(**rule_api.trigger)
        trigger_db = TriggerService.create_trigger_db(trigger_api)
        trigger_ref = reference.get_str_resource_ref_from_model(trigger_db)
        rule_db.trigger = trigger_ref
        rule_db = Rule.add_or_update(rule_db)
        rules.append(rule_db)

        RULE_2 = {                      # Rule should match.
            'enabled': True,
            'name': 'st2.test.rule2',
            'trigger': {
                'type': 'dummy_pack_1.st2.test.trigger1'
            },
            'criteria': {
                'trigger.k1': {
                    'pattern': 't1_p_v',
                    'type': 'equals'
                }
            },
            'action': {
                'ref': 'sixpack.st2.test.action',
                'parameters': {
                    'ip2': '{{rule.k1}}',
                    'ip1': '{{trigger.t1_p}}'
                }
            },
            'id': '23',
            'description': ''
        }
        rule_api = RuleAPI(**RULE_2)
        rule_db = RuleAPI.to_model(rule_api)
        rule_db.trigger = trigger_ref
        rule_db = Rule.add_or_update(rule_db)
        rules.append(rule_db)

        RULE_3 = {
            'enabled': False,         # Disabled rule shouldn't match.
            'name': 'st2.test.rule3',
            'trigger': {
                'type': 'dummy_pack_1.st2.test.trigger1'
            },
            'criteria': {
                'trigger.k1': {
                    'pattern': 't1_p_v',
                    'type': 'equals'
                }
            },
            'action': {
                'ref': 'sixpack.st2.test.action',
                'parameters': {
                    'ip2': '{{rule.k1}}',
                    'ip1': '{{trigger.t1_p}}'
                }
            },
            'id': '23',
            'description': ''
        }
        rule_api = RuleAPI(**RULE_3)
        rule_db = RuleAPI.to_model(rule_api)
        rule_db.trigger = trigger_ref
        rule_db = Rule.add_or_update(rule_db)
        rules.append(rule_db)

        return rules
