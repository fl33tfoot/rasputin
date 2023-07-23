import subprocess
import time
import os
import hashlib
import json
import shutil
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
proc_usr = subprocess.run(["grep", "1000", "/etc/passwd"], capture_output=True)

# Folder directories
MOUNT_POINT = "/home/{}/usb".format(proc_usr.stdout.decode().split(":")[0])
DEST_POINT = "/home/{}/faces".format(proc_usr.stdout.decode().split(":")[0])

SOURCE_POINT = os.path.join(MOUNT_POINT, 'faces')
BACKUP_POINT = os.path.join(MOUNT_POINT, 'backup')

def mount_usb_device(device):
    print("USB storage device detected:")
    print(f"{device}\n")

    
    if not os.path.exists(MOUNT_POINT):
        os.mkdir(MOUNT_POINT)
        
    proc_mount = subprocess.run(["mount", device, MOUNT_POINT], capture_output=True)
        
    if proc_mount.returncode == 0:
        print("\n[OK] : USB storage mounted at {}".format(MOUNT_POINT))
    else:
        if not os.path.ismount(MOUNT_POINT):
            print("[ERR] : USB storage not mounted: ")
            print(proc_mount.stderr.decode())
            return False

    if not os.path.exists(SOURCE_POINT):
        print("\n[ERR] : 'faces' folder not found. Unmounting and exiting.")
        subprocess.run(["umount", device])
        return False

    if not os.path.exists(BACKUP_POINT):
        os.mkdir(BACKUP_POINT)
        print("\n[INFO] : 'faces' folder detected, however 'backup' was not found. Creating...")

    return True

def create_hashes_file():
    gifs = []
    for file in os.listdir(DEST_POINT):
        if file.endswith('.gif'):
            file_path = os.path.join(DEST_POINT, file)
            md5_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            anim_time = 60  # Placeholder, you need to determine the appropriate value
            gifs.append({
                'filename': file,
                'hash': md5_hash,
                'anim_time': anim_time
            })

    hashes_file = os.path.join(DEST_POINT, 'hashes.json')
    with open(hashes_file, 'w') as f:
        json.dump(gifs, f, indent=4)
    print("\n[OK] : Populating 'hashes.json' file...")

def update_hashes_file():
    hashes_file = os.path.join(DEST_POINT, 'hashes.json')
    with open(hashes_file) as f:
        data = json.load(f)

    for file in os.listdir(SOURCE_POINT):
        if file.endswith('.gif'):
            face_path = os.path.join(SOURCE_POINT, file)
            dest_path = os.path.join(DEST_POINT, file)

            matching_file = next((gif for gif in data if gif['filename'] == file), None)

            if not os.path.exists(dest_path):
                # File exists in faces_folder but not in DEST_POINT, copy and add hash to JSON
                shutil.copy2(face_path, DEST_POINT)
                hash_value = hashlib.md5(open(face_path, 'rb').read()).hexdigest()
                if matching_file:
                    matching_file['hash'] = hash_value
                else:
                    data.append({
                        'filename': file,
                        'hash': hash_value,
                        'anim_time': 60
                    })
                print("\n[OK] : File '{}' has been copied successfully and added to the hash list.".format(file))

            elif matching_file:
                # File exists in both faces_folder and DEST_POINT, compare hashes
                faces_folder_hash = hashlib.md5(open(face_path, 'rb').read()).hexdigest()
                if faces_folder_hash != matching_file['hash']:
                    # Hashes are different, overwrite DEST_POINT with faces_folder
                    shutil.copy2(face_path, DEST_POINT)
                    matching_file['hash'] = faces_folder_hash
                    print("\n[OK] : File '{}' has been overwritten successfully and the hash list has been updated".format(file))

    with open(hashes_file, 'w') as f:
        json.dump(data, f, indent=4)



def compress_and_copy():
    shutil.make_archive(os.path.join(BACKUP_POINT, 'faces_{}'.format(timestamp)), 'zip', DEST_POINT)


while True:
    lsblk_output = subprocess.check_output(["lsblk", "-o", "NAME,TRAN"], universal_newlines=True)
    lines = lsblk_output.strip().split("\n")

    if len(lines) > 1:
        device_info = lines[1].split()

        if len(device_info) >= 2:
            device_name = device_info[0]
            transport_type= device_info[1]

            if transport_type == "usb":
                if mount_usb_device("/dev/{}1".format(device_name)):
                    hashes_file = os.path.join(DEST_POINT, 'hashes.json')
                    if not os.path.exists(hashes_file):
                        print("\n[ERR] : There is a 'faces' folder but no 'hashes.json'! Is this a first time run?")
                        print("\n[INFO] : Creating 'hashes.json' file...")
                        create_hashes_file()
                        print("\n[OK] : Created a 'hashes.json' file successfully")
                    print("\n[INFO] : Updating the file hashes")
                    update_hashes_file()
                    print("\n[OK] : Updated all the file hashes successfully")
                    
                    print("\n[INFO] : Backing up before any changes...")
                    compress_and_copy()
                    print("\n[OK] : Backed up successfully")
                    
                    print("\n[INFO] : Transfer completed. USB storage device unmounting...")
                    subprocess.run(["umount", "/dev/{}1".format(device_name)])
                    print("\n[OK] : USB storage device unmounted. Exiting...")
                    exit()

    time.sleep(2)
