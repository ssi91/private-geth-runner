import json

import init_data_dirs as idr
from config import get_config

_genesis = {
    "config": {
        "chainId": 8765,
        "homesteadBlock": 0,
        "eip150Block": 0,
        "eip155Block": 0,
        "eip158Block": 0,
        "byzantiumBlock": 0,
        "constantinopleBlock": 0,
        "petersburgBlock": 0,
        "clique": {
            "period": 5,
            "epoch": 30000
        }
    },
    "difficulty": "1",
    "gasLimit": "8000000",
    "extradata": "",
    "alloc": {
        "7e056E758a96064D8702bACFcbE2beDA8CAB0251": {"balance": "300000"}
    }
}


def get_genesis(signers, alloc):
    signers = [s[2:] if s[0:2] == "0x" else s for s in signers]
    extradata = "0x0000000000000000000000000000000000000000000000000000000000000000{0}0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    extradata = extradata.format("".join(signers))
    _genesis["extradata"] = extradata
    _genesis["alloc"] = alloc["alloc"]
    return _genesis


def generate_file(_path, signers, alloc):
    gen = get_genesis(signers, alloc)
    with open(_path, "w") as f:
        json.dump(gen, f)


def get_signers_keys(data):
    keys = []
    for node, signers in zip(data['nodes'], data['genesis']['signers']):
        for signer in signers:
            keys.append((node, signer))
    return keys


def get_alloc(data):
    alloc = {}
    for node, alloc_settings in zip(data['nodes'], data['genesis']['alloc']):
        for alloc_setting in alloc_settings:
            alloc[(node, alloc_setting['account'])] = alloc_setting['amount']
    return alloc


if __name__ == "__main__":
    config = get_config("./config.yml")  # TODO: parametrize
    for data_dir, num_accounts in zip(config['nodes'], config['accounts']):
        for _ in range(num_accounts):
            idr.Geth.exec("account", "new", datadir=data_dir, password=idr.ACC_PASSWORD).stdout  # TODO: add logger

    res = idr.Geth.get_accounts()

    keys = get_signers_keys(config)
    alloc = get_alloc(config)

    generate_file(
        config['genesis']['template'],
        [res[data_dir][signer]['address'] for data_dir, signer in keys],
        {
            "alloc": {
                res[data_dir][account]['address']: {"balance": f"{balance}"} for (data_dir, account), balance in
                alloc.items()
            }
        }
    )

    for data_dir in idr.DATA_DIRS:
        idr.Geth.exec("init genesis.json", datadir=data_dir)
