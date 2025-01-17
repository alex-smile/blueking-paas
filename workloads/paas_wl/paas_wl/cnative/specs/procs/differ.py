"""Compare the difference between app model's processes"""
from typing import List

from attrs import define

from paas_wl.cnative.specs.resource import get_mres_from_cluster
from paas_wl.cnative.specs.v1alpha1.bk_app import BkAppResource
from paas_wl.platform.applications.struct_models import ModuleEnv
from paas_wl.workloads.processes.constants import AppEnvName

from .replicas import ReplicasReader


@define
class ProcReplicasChange:
    """Describe changes on process's "replicas" field"""

    proc_type: str
    old: int
    new: int


def get_online_replicas_diff(env: ModuleEnv, new_res: BkAppResource) -> List[ProcReplicasChange]:
    """Get the replicas differences between online version and incoming resource

    :param env: The online environment to be checked
    :param new_res: New resource object
    """
    from_res = get_mres_from_cluster(env)
    if not from_res:
        return []
    return diff_replicas(from_res, new_res, AppEnvName(env.environment))


def diff_replicas(old: BkAppResource, new: BkAppResource, env_name: AppEnvName) -> List[ProcReplicasChange]:
    """Get replicas changes between two resource objects

    :param env_name: The environment name to be compared
    """
    old_vals = ReplicasReader(old).read_all(env_name)
    new_vals = ReplicasReader(new).read_all(env_name)
    changes = []
    for proc_type, (val_o, _) in old_vals.items():
        if proc_type in new_vals:
            if (val_n := new_vals[proc_type][0]) != val_o:
                changes.append(ProcReplicasChange(proc_type, val_o, val_n))
    return changes
