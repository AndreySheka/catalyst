from typing import Any, Callable, Dict, List, Optional, Union
import collections
import copy

import numpy as np


def get_key_str(dictionary: dict, key: Optional[Union[str, List[str]]],) -> Any:
    """
    Returns value from dict by key.

    Args:
        dictionary: dict
        key: key

    Returns:
        value
    """
    return dictionary[key]


def get_key_list(
    dictionary: dict, key: Optional[Union[str, List[str]]],
) -> Dict:
    """
    Returns sub-dict from dict by list of keys.

    Args:
        dictionary: dict
        key: list of keys

    Returns:
        sub-dict
    """
    result = {key_: dictionary[key_] for key_ in key}
    return result


def get_key_dict(
    dictionary: dict, key: Optional[Union[str, List[str]]],
) -> Dict:
    """
    Returns sub-dict from dict by dict-mapping of keys.

    Args:
        dictionary: dict
        key: dict-mapping of keys

    Returns:
        sub-dict
    """
    result = {key_out: dictionary[key_in] for key_in, key_out in key.items()}
    return result


def get_key_none(
    dictionary: dict, key: Optional[Union[str, List[str]]],
) -> Dict:
    """
    Returns empty dict.
    Args:
        dictionary: dict
        key: none

    Returns:
        dict
    """
    return {}


def get_key_all(
    dictionary: dict, key: Optional[Union[str, List[str]]],
) -> Dict:
    """
    Returns whole dict.
    Args:
        dictionary: dict
        key: none

    Returns:
        dict
    """
    return dictionary


def get_dictkey_auto_fn(key: Optional[Union[str, List[str]]]) -> Callable:
    """
    Function generator for sub-dict preparation from dict
    based on predefined keys.

    Args:
        key: keys

    Returns:
        function
    """
    if isinstance(key, str):
        if key == "__all__":
            return get_key_all
        else:
            return get_key_str
    elif isinstance(key, (list, tuple)):
        return get_key_list
    elif isinstance(key, dict):
        return get_key_dict
    elif key is None:
        return get_key_none
    else:
        raise NotImplementedError()


def merge_dicts(*dicts: dict) -> dict:
    """
    Recursive dict merge.
    Instead of updating only top-level keys,
    ``merge_dicts`` recurses down into dicts nested
    to an arbitrary depth, updating keys.

    Args:
        *dicts: several dictionaries to merge

    Returns:
        dict: deep-merged dictionary
    """
    assert len(dicts) > 1

    dict_ = copy.deepcopy(dicts[0])

    for merge_dict in dicts[1:]:
        merge_dict = merge_dict or {}
        for k in merge_dict:
            if (
                k in dict_
                and isinstance(dict_[k], dict)
                and isinstance(merge_dict[k], collections.Mapping)
            ):
                dict_[k] = merge_dicts(dict_[k], merge_dict[k])
            else:
                dict_[k] = merge_dict[k]

    return dict_


def append_dict(dict1, dict2):
    """
    Appends dict2 with the same keys as dict1 to dict1
    """
    for key in dict1.keys():
        dict1[key] = np.concatenate((dict1[key], dict2[key]))
    return dict1


def flatten_dict(
    dictionary: Dict[str, Any], parent_key: str = "", separator: str = "/"
) -> "collections.OrderedDict":
    """
    Make the given dictionary flatten

    Args:
        dictionary (dict): giving dictionary
        parent_key (str, optional): prefix nested keys with
            string ``parent_key``
        separator (str, optional): delimiter between
            ``parent_key`` and ``key`` to use

    Returns:
        collections.OrderedDict: ordered dictionary with flatten keys
    """
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(
                flatten_dict(value, new_key, separator=separator).items()
            )
        else:
            items.append((new_key, value))
    return collections.OrderedDict(items)


def split_dict_to_subdicts(dct: Dict, prefixes: List, extra_key: str):
    subdicts = {}
    extra_subdict = {
        k: v
        for k, v in dct.items()
        if all(not k.startswith(prefix) for prefix in prefixes)
    }
    if len(extra_subdict) > 0:
        subdicts[extra_key] = extra_subdict
    for prefix in prefixes:
        subdicts[prefix] = {
            k.replace(f"{prefix}_", ""): v
            for k, v in dct.items()
            if k.startswith(prefix)
        }
    return subdicts
