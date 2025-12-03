from pygeist.cli import main
from multiprocessing import set_start_method


if __name__ == '__main__':
    set_start_method("spawn", force=True)


    main()
