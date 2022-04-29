import os.path

from yaml import load, Loader


class ValidationError(Exception):
    pass


class VersionError(ValidationError):
    def __init__(self, current_version, allowed_versions):
        allowed_versions_str = ", ".join(allowed_versions)
        super(VersionError, self).__init__(
            f"Version {current_version} is not allowed. Valid versions are {allowed_versions_str}"
        )


class NodesError(ValidationError):
    pass


class AccountsError(ValidationError):
    pass


class GenesisError(ValidationError):
    pass


def validate_version(data):
    allowed_versions = [0]
    if data['version'] in allowed_versions:
        return data
    raise VersionError(data['version'], allowed_versions)


def validate_nodes(data):
    if len(data['nodes']) != len(data['accounts']):
        raise NodesError("Amount of nodes is not compatible with 'accounts' settings.")
    return data


def validate_accounts(data):
    for accs_amount, alloc in zip(data['accounts'], data['genesis']['alloc']):
        if accs_amount > len(alloc):
            raise AccountsError("Alloc settings are not valid")
    if any((accs_amount < 0 for accs_amount in data['accounts'])):
        raise AccountsError("Wrong accounts amount")
    return data


def validata_genesis(data):
    if not os.path.exists(data['genesis']['template']):
        raise GenesisError(f"File {data['genesis']['template']} doesn't exist")
    if len(data['accounts']) < len(data['genesis']['signers']) or any(
            accs > len(sig_list) for accs, sig_list in zip(data['accounts'], data['genesis']['signers'])):
        raise GenesisError(f"Wrong amount of signers")
    for accs, sig_list in zip(data['accounts'], data['genesis']['signers']):
        if any(accs < sig_number - 1 for sig_number in sig_list):
            raise GenesisError("Inappropriate signer's number")
    return data


_config_middleware = [
    validate_version,
    validate_nodes,
    validate_accounts,
    validata_genesis,
]

with open("./config.yml", "r") as conf:
    data = load(conf, Loader)

for middleware in _config_middleware:
    try:
        data = middleware(data)
    except ValidationError as e:
        raise  # TODO: gracefully fall here and log the error
    except Exception as e:
        raise  # TODO: gracefully fall here and log the error

print(data)
