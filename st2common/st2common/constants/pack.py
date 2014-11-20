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

__all__ = [
    'PACKS_PACK_NAME',
    'SYSTEM_PACK_NAME',
    'PACKS_PACK_NAME',
    'SYSTEM_PACK_NAMES',
    'USER_PACK_NAME_BLACKLIST'
]

# A list of allowed characters for the pack name
PACK_NAME_WHITELIST = r'^[A-Za-z0-9_-]+'

# Name used for system pack
SYSTEM_PACK_NAME = 'core'

# Name used for pack management pack
PACKS_PACK_NAME = 'packs'

# Name of the default pack
DEFAULT_PACK_NAME = 'default'

# A list of system pack names
SYSTEM_PACK_NAMES = [
    SYSTEM_PACK_NAME,
    PACKS_PACK_NAME,
]

# A list of pack names which can't be used by user-supplied packs
USER_PACK_NAME_BLACKLIST = [
    SYSTEM_PACK_NAME,
    PACKS_PACK_NAME
]
