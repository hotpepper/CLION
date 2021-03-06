from tqdm import tqdm
import params
import os
import shutil
import time
import zipfile


FILES = [
    'nyclion_{version}.zip',
    'rpl_{version}.zip',
    'ldf_{version}.zip',
    'nysswi_{version}.zip',
    'nyccwi_{version}.zip',
    'nypp_{version}.zip',
    'nynta_{version}.zip'
    ]


def setup_folders(folder=params.FOLDER):
    for nf in ('DATA', 'RAW_DATA'):
        path = os.path.join(folder, nf)
        if not os.path.isdir(path):
            os.makedirs(path)
        else:
            if nf == 'DATA':
                print '*'*25
                raw_input('\nCLEAN OUT EXISTING FOLDER: %s\n' % path)
                print '*' * 25


def download_files(files=FILES, folder=params.FOLDER, version=params.VERSION, download_path=params.DOWLOAD_PATH):
    url = 'https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/'
    for f in tqdm(files):
        _ = url+f.format(version=version)
        os.startfile(_)
    # Make sure files are downloaded
    time.sleep(10)
    for f in tqdm(files):
        from_path = os.path.join(download_path, f.format(version=version))
        to_path = os.path.join(os.path.join(folder, 'RAW_DATA'), f.format(version=version))
        if os.path.isfile(to_path):
            os.remove(to_path)
        shutil.copyfile(from_path, to_path)
        os.remove(from_path)
        unzip(to_path)


def unzip(zip_path):
    unzip_path = os.path.dirname(zip_path)
    if os.path.isfile(unzip_path):
        os.remove(unzip_path)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(unzip_path)


def extract_files(files, folder, version):
    data_folder = os.path.join(folder, 'RAW_DATA')
    output_data_folder = os.path.join(folder, 'DATA')
    for f in tqdm(files):
        if 'lion' in f:
            # TODO: just add straight to database to avoid shp naming restrictions
            # extract shp from geodatabase
            cmd = r'ogr2ogr -f "ESRI Shapefile" {fldr} {gdb}'.format(
                fldr=output_data_folder,
                gdb=os.path.join(data_folder, 'lion\lion.gdb'))
            os.system(cmd)
        elif os.path.isdir(os.path.join(data_folder, f.format(version=version)[:-4])):
            # copy shapefiles to root folder
            for pth, dir, fls in os.walk(os.path.join(data_folder, f.format(version=version)[:-4])):
                for _ in fls:
                    src = os.path.join(pth, _)
                    shutil.copyfile(src, os.path.join(output_data_folder, _))
    plain_files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f))
                   and f[-4:] != '.zip']
    for _f in plain_files:
        shutil.copyfile(os.path.join(data_folder, _f),
                        os.path.join(output_data_folder, _f))


def run():
    print 'Setting up subfolders...'
    setup_folders(params.FOLDER)
    print 'Downloading data...'
    download_files(FILES, params.FOLDER, params.VERSION, params.DOWLOAD_PATH)
    print 'Moving shapefiles...'
    extract_files(FILES, params.FOLDER, params.VERSION)
