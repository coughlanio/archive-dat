import tempfile
import shutil
import uuid
import os
import subprocess
import zipfile
from urllib import request
from datetime import datetime

CONFIGS = [
    {
        "manufacturer": "NEC",
        "system": "PC Engine CD",
        "type": "Redump CHDs",
        "files": [
            "https://archive.org/download/chd_pcecd/chd_pcecd_files.xml",
        ],
    },
    {
        "manufacturer": "Sega",
        "system": "Mega-CD",
        "type": "Redump CHDs",
        "files": [
            "https://archive.org/download/chd_segacd/chd_segacd_files.xml",
        ],
    },
    {
        "manufacturer": "Sega",
        "system": "Saturn",
        "type": "Redump CHDs",
        "files": [
            "https://archive.org/download/chd_saturn/chd_saturn_files.xml",
        ],
    },
    {
        "manufacturer": "Sony",
        "system": "PlayStation",
        "type": "Redump CHDs",
        "files": [
            "https://archive.org/download/chd_psx/chd_psx_files.xml",
            "https://archive.org/download/chd_psx_eur/chd_psx_eur_files.xml",
            "https://archive.org/download/chd_psx_jap/chd_psx_jap_files.xml",
            "https://archive.org/download/chd_psx_jap_p2/chd_psx_jap_p2_files.xml",
            "https://archive.org/download/chd_psx_misc/chd_psx_misc_files.xml",
        ],
    },
]

print("Extracting SabreTools")
st_dir = tempfile.mkdtemp()
print(st_dir)
with zipfile.ZipFile("tools/sabretools.zip", "r") as zf:
    zf.extractall(st_dir)
    zf.close()

for config in CONFIGS:
    tmp_dir = tempfile.mkdtemp()

    manufacturer = config.get("manufacturer", "Default")
    system = config.get("system", "Default")
    type = config.get("type", "Default")
    date = datetime.today().strftime('%Y-%m-%d')

    for f in config.get("files", []):
        output_file = os.path.join(tmp_dir, f"{str(uuid.uuid4())}.xml")
        print(f"Downloading {f}")
        request.urlretrieve(f, output_file)


    dat_name = f"{manufacturer} - {system} {type}"

    executable = os.path.join(st_dir, "SabreTools.dll")
    print(executable)

    print("Running sabretools")
    subprocess.run(
        [
            "dotnetx64",
            executable,
            "-ud",
            "-m",
            "-ot=xml",
            f"-f={dat_name}",
            f"-n={dat_name}",
            f"-de={dat_name}",
            f"-v={date}",
            f"-co=Generated from Achive.org XMLs",
            f"-au=Teddy",
            f"-c=Archive.org {type}",
            "--filter=!machine.name:Default",
            "-out=dats",
            tmp_dir,
        ]
    )

    shutil.rmtree(tmp_dir)
