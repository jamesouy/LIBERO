from .base_predicates import *
from ...envs.bddl_base_domain import BDDLBaseDomain
from typing import Optional


# And and Or can't be defined in base_predicates because they require eval_goal_state and there will be a cyclical import
class AndPredicateFn(MultiarayAtomic):
    def __call__(self, env: BDDLBaseDomain, *args):
        assert len(args) >= 1
        return all(eval_goal_state(arg, env=env) for arg in args)


class OrPredicateFn(MultiarayAtomic):
    def __call__(self, env: BDDLBaseDomain, *args):
        assert len(args) >= 1
        return any(eval_goal_state(arg, env=env) for arg in args)


VALIDATE_PREDICATE_FN_DICT = {
    "true": TruePredicateFn(),
    "false": FalsePredicateFn(),
    "and": AndPredicateFn(),
    "or": OrPredicateFn(),
    "in": In(),
    # "incontact": InContactPredicateFn(),
    "on": On(),
    "up": Up(),
    # "stack":     Stack(),
    # "temporal":  TemporalPredicate(),
    "printjointstate": PrintJointState(),
    "open": Open(),
    "close": Close(),
    "turnon": TurnOn(),
    "turnoff": TurnOff(),
}


def update_predicate_fn_dict(fn_key, fn_name):
    VALIDATE_PREDICATE_FN_DICT.update({fn_key: eval(fn_name)()})


def eval_goal_state(state, env: Optional[BDDLBaseDomain] = None):
    """
    Evaluates a goal state (list or str), converting any object/site names into the object/site states
    """
    assert env is not None # we need the env to access the object states
    if type(state) is not list: # state can either be a list [name, *args] or a str name of the predicate
        state = [state]
    assert len(state) >= 1
    predicate_fn_name = state[0]
    args = [env.object_states_dict.get(arg, arg) if type(arg) is str else arg for arg in state[1:]]
    return eval_predicate_fn(predicate_fn_name, *args, env=env)


def eval_predicate_fn(predicate_fn_name, *args, env: Optional[BDDLBaseDomain] = None):
    assert predicate_fn_name in VALIDATE_PREDICATE_FN_DICT, f"{predicate_fn_name} is not a valid predicate"
    # if predicate_fn_name not in VALIDATE_PREDICATE_FN_DICT:
    #     return False
    predicate_fn = VALIDATE_PREDICATE_FN_DICT[predicate_fn_name]
    if predicate_fn_name.lower() in ['and', 'or']: # and/or require the environment
        return predicate_fn(env, *args)
    else:
        return VALIDATE_PREDICATE_FN_DICT[predicate_fn_name](*args)


def get_predicate_fn_dict():
    return VALIDATE_PREDICATE_FN_DICT


def get_predicate_fn(predicate_fn_name):
    return VALIDATE_PREDICATE_FN_DICT[predicate_fn_name.lower()]
