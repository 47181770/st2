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

import webtest


SUPER_SECRET_PARAMETER = 'SUPER_SECRET_PARAMETER_THAT_SHOULD_NEVER_APPEAR_IN_RESPONSES_OR_LOGS'
ANOTHER_SUPER_SECRET_PARAMETER = 'ANOTHER_SUPER_SECRET_PARAMETER_TO_TEST_OVERRIDING'


class ResponseValidationError(ValueError):
    pass


class ResponseLeakError(ValueError):
    pass


class TestApp(webtest.TestApp):
    def do_request(self, *args, **kwargs):
        res = super(TestApp, self).do_request(*args, **kwargs)

        if res.headers.get('Warning', None):
            raise ResponseValidationError('Endpoint produced invalid response. Make sure the '
                                          'response matches OpenAPI scheme for the endpoint.')

        if not kwargs.get('expect_errors', None):
            if SUPER_SECRET_PARAMETER in res.body or ANOTHER_SUPER_SECRET_PARAMETER in res.body:
                raise ResponseLeakError('Endpoint response contains secret parameter. '
                                        'Find the leak.')

        return res
