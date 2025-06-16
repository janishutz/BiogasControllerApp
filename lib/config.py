import configparser
from typing import List

# Load the config
config = configparser.ConfigParser()
config.read("./config.ini")

global first_error
first_error = True

global is_verbose
is_verbose = True


def set_verbosity(verbose: bool):
    global is_verbose
    is_verbose = verbose

    print("\n", "-" * 20, "\nValidating configuration...\n")


def str_to_bool(val: str) -> bool | None:
    """Convert a string to boolean, converting "True" and "true" to True, same for False

    Args:
        val: The value to try to convert

    Returns:
        Returns either a boolean if conversion was successful, or None if not a boolean
    """
    return {"True": True, "true": True, "False": False, "false": False}.get(val, None)


def read_config(
    key_0: str,
    key_1: str,
    default: str,
    valid_entries: List[str] = [],
    type_to_validate: str = "",
) -> str:
    """Read the configuration, report potential configuration issues and validate each entry

    Args:
        key_0: The first key (top level)
        key_1: The second key (where the actual key-value pair is)
        default: The default value to return if the check fails
        valid_entries: [Optiona] The entries that are valid ones to check against
        type_to_validate: [Optional] Data type to validate

    Returns:
        [TODO:return]
    """
    # Try loading the keys
    tmp = {}
    try:
        tmp = config[key_0]
    except KeyError:
        print_config_error(key_0, key_1, "", default, "unknown", index=1)
        return default

    value = ""
    try:
        value = tmp[key_1]
    except KeyError:
        print_config_error(key_0, key_1, "", default, "unknown")
        return default

    if len(value) == 0:
        print_config_error(key_0, key_1, value, default, "not_empty")

    # Validate input
    if type_to_validate != "":
        # Need to validate
        if type_to_validate == "int":
            try:
                int(value)
            except ValueError:
                print_config_error(key_0, key_1, value, default, "int")
                return default
        if type_to_validate == "float":
            try:
                float(value)
            except ValueError:
                print_config_error(key_0, key_1, value, default, "float")
                return default

        if type_to_validate == "bool":
            if str_to_bool(value) == None:
                print_config_error(key_0, key_1, value, default, "bool")
                return default

    if len(valid_entries) > 0:
        # Need to validate the names
        try:
            valid_entries.index(value)
        except ValueError:
            print_config_error(
                key_0, key_1, value, default, "oneof", valid_entries=valid_entries
            )
            return default

    return value


def print_config_error(
    key_0: str,
    key_1: str,
    value: str,
    default: str,
    expected: str,
    valid_entries: List[str] = [],
    msg: str = "",
    index: int = 1,
):
    """Print configuration errors to the shell

    Args:
        key_0: The first key (top level)
        key_1: The second key (where the actual value is to be found)
        expected: The data type expected. If unknown key, set to "unknown" and set index; If should be one of, use "oneof" and set valid_entries list
        msg: The message to print
        index: The index in the chain (i.e. if key_0 or key_1)
    """
    if not is_verbose:
        return

    print(f" ==> Using default setting ({default}) for {key_0}.{key_1}")

    if expected == "unknown":
        # The field was unknown
        print(f'    -> Unknown field "{key_0 if index == 0 else key_1}"')
    elif expected == "oneof":
        print(
            f'    -> Invalid name "{value}". Has to be one of', ", ".join(valid_entries)
        )
    elif expected == "not_empty":
        print("    -> Property is unexpectedly None")
    elif expected == "bool":
        print(f'    -> Boolean property expected, but instead found "{value}".')
    else:
        print(f"    -> Expected a config option of type {expected}.")

    if msg != "":
        print(msg)
