import json

import init_data_dirs as idr

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
    with open(f"{_path}/genesis.json", "w") as f:
        json.dump(gen, f)


if __name__ == "__main__":
    for data_dir in idr.DATA_DIRS:
        idr.Geth.exec("account", "new", datadir=data_dir, password=idr.ACC_PASSWORD).stdout  # TODO: add logger

    res = idr.Geth.get_accounts()
    generate_file(
        "/Users/ssi/geth_infra/",  # TODO: parametrise
        [
            res[idr.DATA_DIRS[0]][0]['address'],
            # res[idr.DATA_DIRS[1]][0]['address'],
            # res[idr.DATA_DIRS[2]][0]['address'],
        ],
        {
            "alloc": {
                res[idr.DATA_DIRS[0]][0]['address']: {"balance": "3000000000000000000"},  # TODO: parametrise
                res[idr.DATA_DIRS[1]][0]['address']: {"balance": "3000000000000000000"},  # TODO: parametrise
            }
        }
    )

    for data_dir in idr.DATA_DIRS:
        idr.Geth.exec("init genesis.json", datadir=data_dir)
