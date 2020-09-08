from confload import Config
cfg = Config({"test": 43})
cfg.load_yaml("../../test.yml")
cfg.load("../../test.ini")
dict(cfg)