import os
import subprocess
from subprocess import PIPE

DATA_DIRS = [
    "~/geth_data/data1",
    "~/geth_data/data2",
    "~/geth_data/data3",
    "~/geth_data/data4",
]

GETH_PATH = "~/go-ethereum/build/bin/geth"

ACC_PASSWORD = "/Users/ssi/geth_infra/password"


class Account:
    @classmethod
    def new(cls, *args, **kwargs):
        pass


class Geth:
    ACCOUNT = Account()

    @classmethod
    def account(cls):
        return cls.ACCOUNT

    @classmethod
    def get_accounts(cls):
        res = {}
        for data_dir in DATA_DIRS:
            exec_result = cls.exec("account", "list", datadir=data_dir)
            split_result = exec_result.stdout.split(b'\n')
            # print(exec_result.stdout.split(b'\n'))
            res[data_dir] = []
            for sr in split_result:
                if sr == b'':
                    continue
                address = sr.split(b'{')[1][:40]
                keystore = sr.split(b'keystore://')[1]
                res[data_dir].append({
                    "address": address.decode('UTF-8'),
                    "keystore": keystore.decode('UTF-8')
                })

        return res

    @classmethod
    def exec(cls, *args, **kwargs):
        subcommand = " ".join(args)
        params = " ".join(f"--{key} {val}" for key, val in kwargs.items())
        command = f"{GETH_PATH} {subcommand} {params}"
        return subprocess.run(command, stdout=PIPE, stderr=PIPE, universal_newlines=False, shell=True)


if __name__ == "__main__":
    for data_dir in DATA_DIRS:
        print(Geth.exec("account", "new", datadir=data_dir, password=ACC_PASSWORD).stdout)
