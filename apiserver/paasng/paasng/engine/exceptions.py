# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making
蓝鲸智云 - PaaS 平台 (BlueKing - PaaS System) available.
Copyright (C) 2017-2022THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.

We undertake not to change the open source license (MIT license) applicable

to the current version of the project delivered to anyone in the future.
"""


class ProcfileInvalidException(Exception):
    pass


class StopProcessFailedException(Exception):
    pass


class OfflineOperationExistError(Exception):
    """Offline Operation already exist"""


class ProcessOperationTooOften(Exception):
    """进程操作过于频繁"""


class NoUnlinkedDeployPhaseError(Exception):
    """没有未绑定的部署阶段"""


class StepNotInPresetListError(Exception):
    """不是预设步骤"""

    def __init__(self, step_name: str, *args, **kwargs):
        self.message = f"Cannot find step: {step_name} in preset list"
        super().__init__(self.message, args, kwargs)


class DuplicateNameInSamePhaseError(Exception):
    """预设步骤名重复"""

    def __init__(self, step_name: str, *args, **kwargs):
        self.message = f"Step: {step_name} is duplicated in same phase, please reassign them"
        super().__init__(self.message, args, kwargs)


class InternalEventFormatError(Exception):
    """部署阶段 内部事件格式错误"""


class DeployInterruptionFailed(Exception):
    """Unable to interrupt a deployment"""
