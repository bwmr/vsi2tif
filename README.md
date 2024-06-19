# vsi2tif
Take Olympus vsi stacks. Bleach-correct, write out ome-tiff. Save clicks.

```
mamba create -n vsi2tif python=3.10 bioformats_jar -c conda-forge
mamba activate vsi2tif
pip install "git+https://github.com/bwmr/vsi2tif.git"
```

```
vsi2tif --nobleach session_folder/*vsi
```