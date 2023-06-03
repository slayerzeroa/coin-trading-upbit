import importlib

algo = importlib.import_module('reverse_timeseries_z_score')

print(algo.run())