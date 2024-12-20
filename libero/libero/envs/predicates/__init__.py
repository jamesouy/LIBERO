from .base_predicates import *


VALIDATE_PREDICATE_FN_DICT = {
    "true": TruePredicateFn(),
    "false": FalsePredicateFn(),
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


def register_predicate_fn(target_class):
    """We design the mapping to be case-INsensitive."""
    VALIDATE_PREDICATE_FN_DICT[target_class.__name__.lower()] = target_class()
    print(VALIDATE_PREDICATE_FN_DICT)


def eval_predicate_fn(predicate_fn_name, *args):
    assert predicate_fn_name in VALIDATE_PREDICATE_FN_DICT, f"{predicate_fn_name} is not a valid predicate"
    return VALIDATE_PREDICATE_FN_DICT[predicate_fn_name](*args)


def get_predicate_fn_dict():
    return VALIDATE_PREDICATE_FN_DICT


def get_predicate_fn(predicate_fn_name):
    return VALIDATE_PREDICATE_FN_DICT[predicate_fn_name.lower()]
