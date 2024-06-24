# vsi2tif
Take Olympus vsi stacks. Bleach-correct, write out ome-tiff, possibly by channel. Save clicks.

Tested for 3D XYZ Data, but not for timeseries. 

Bleach-correction by histogram matching, according to [Miura (2020)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7871415/).
Implementation inspired by `napari-bleach-correct`.

```
mamba create -n vsi2tif python=3.10 bioformats_jar -c conda-forge
mamba activate vsi2tif
pip install "git+https://github.com/bwmr/vsi2tif.git"
```

```
vsi2tif --help
vsi2tif session_folder/*vsi
```
