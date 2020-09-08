from confload import Config
cfg = Config({"test": 43})
cfg.load_yaml("../../test.yml")
cfg.load("../../test.ini")
dict(cfg)

import os
os.environ["dga"] = "54"
cfg.env.int("dga")

os.environ["top"] = "54, 76"
cfg.env.list("top")
