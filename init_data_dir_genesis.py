import init_data_dirs as idr


if __name__ == "__main__":
    for data_dir in idr.DATA_DIRS:
        idr.Geth.exec("init genesis.json", datadir=data_dir)
