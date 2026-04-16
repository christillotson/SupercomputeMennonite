# Sentinel-2 Index Pipeline: Commands Used + Final Scripts

## Project goal
Download Sentinel-2 L2A imagery, extract the required 60 m `.jp2` band files, and generate 18 spectral index GeoTIFFs locally and on the HPC.

---

# Part 1: Commands Used

## A. Local Windows setup and testing

### 1. Check existing folders
```bash
pwd
ls
ls /c/Users/israt/sentinel_pipeline
ls /c/Users/israt/sentinel_pipeline/scripts
ls /c/Users/israt/sentinel_pipeline/data

mkdir /c/Users/israt/sentinel_pipeline/scripts

ls /c/Users/israt/sentinel_pipeline
ls /c/Users/israt/sentinel_pipeline/scripts
find /c/Users/israt/sentinel_pipeline -maxdepth 3 -type f
cat /c/Users/israt/sentinel_pipeline/environment.yml

source /c/Users/israt/miniconda3/etc/profile.d/conda.sh
conda activate sentinel-hpc
python --version
python -c "import numpy, rasterio, requests; print('packages loaded successfully')"

export COPERNICUS_USER="YOUR_USERNAME"
export COPERNICUS_PASS="YOUR_PASSWORD"
export S2_DOWNLOAD_DIR="/c/Users/israt/sentinel_pipeline/data/raw"
echo $S2_DOWNLOAD_DIR

mkdir -p /c/s2test
mkdir -p /c/s2test/raw
mkdir -p /c/s2test/processed
export S2_DOWNLOAD_DIR="/c/s2test/raw"

cd /c/Users/israt/sentinel_pipeline
python scripts/download_images.py -78 38 -76 39.0 2024-06-01 2024-08-30
ls /c/s2test/raw
ls /c/s2test/raw/*

cd /c/Users/israt/sentinel_pipeline
python scripts/download_images.py -78 38 -76 39.0 2024-06-01 2024-08-30
ls /c/s2test/raw
ls /c/s2test/raw/*

python /c/Users/israt/sentinel_pipeline/scripts/generate_index_tiffs.py \
"/c/s2test/raw/S2A_MSIL2A_20240628T154941_N0510_R054_T18STH_20240628T222158" \
"/c/s2test/processed/S2A_MSIL2A_20240628T154941_N0510_R054_T18STH_20240628T222158_indices"

ls /c/s2test/processed/S2A_MSIL2A_20240628T154941_N0510_R054_T18STH_20240628T222158_indices

conda install -c conda-forge libgdal-jp2openjpeg
python -c "import rasterio; print(rasterio.__version__)"

LOGIN TO HPC

ssh ifarah@bora.sciclone.wm.edu

mkdir -p ~/sentinel_pipeline/scripts
mkdir -p ~/sentinel_pipeline/data/raw
mkdir -p ~/sentinel_pipeline/data/processed
ls ~/sentinel_pipeline
ls ~/sentinel_pipeline/data

scp /c/Users/israt/sentinel_pipeline/environment.yml ifarah@bora.sciclone.wm.edu:~/sentinel_pipeline/
scp /c/Users/israt/sentinel_pipeline/scripts/*.py ifarah@bora.sciclone.wm.edu:~/sentinel_pipeline/scripts/

ls ~/sentinel_pipeline
ls ~/sentinel_pipeline/scripts
cat ~/sentinel_pipeline/environment.yml

ls /sciclone/apps | grep -i miniforge

source /sciclone/apps/miniforge3-24.9.2-0/etc/profile.d/conda.sh
conda env list

conda env create -f ~/sentinel_pipeline/environment.yml
conda activate sentinel-hpc
python --version
python -c "import numpy, rasterio, requests; print('packages loaded successfully')"

export COPERNICUS_USER="YOUR_USERNAME"
export COPERNICUS_PASS="YOUR_PASSWORD"
export S2_DOWNLOAD_DIR="$HOME/sentinel_pipeline/data/raw"
echo $S2_DOWNLOAD_DIR

cd ~/sentinel_pipeline
python scripts/download_images.py -78 38 -76 39.0 2024-06-01 2024-08-30
ls ~/sentinel_pipeline/data/raw

python ~/sentinel_pipeline/scripts/generate_index_tiffs.py \
~/sentinel_pipeline/data/raw/S2B_MSIL2A_20240623T154819_N0510_R054_T18STH_20240623T195821 \
~/sentinel_pipeline/data/processed/S2B_MSIL2A_20240623T154819_N0510_R054_T18STH_20240623T195821_indices

