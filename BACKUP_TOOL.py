import os,shutil,json
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# the function that reads the config
def read_config():
    with open('config.json', 'r') as file:
        data = json.load(file)
        return data

# the function which assign the name with the date and time using the config
def change_template(name: str):
    now = datetime.now()
    # separete time variabels
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    second = now.strftime("%S")
    day = now.strftime("%d")
    mounth = now.strftime("%m")
    year = now.strftime("%Y")
    name = name.replace("%hh%",hour).replace("%MM%", minute).replace("%ss%", second).replace("%dd%", day).replace("%mm%", mounth).replace("%yyyy%", year)
    return name

# the function which is doing the archive
def zip(name,inp,out):
    name = name
    in_path = inp
    out_path = out
    archive = shutil.make_archive(name, 'zip', in_path)
    new_path = os.path.join(out_path, os.path.basename(archive))
    shutil.move(archive, new_path)

# upload function
def upload(name,folder_id):
    file_path = name
    file = drive.CreateFile({'title': name,
                            'parents': [{'id': folder_id}]})
    file.SetContentFile(file_path)
    file.Upload()

# erase function
def erase(path_archive,keep_archives):
    file_list = drive.ListFile({'q': "title contains '.zip' and trashed=false"}).GetList()
    if len(file_list) <= 3:
        return
    else:
        file_list.sort(key=lambda f: datetime.strptime(f['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ"))
        oldest_file = file_list[0]
        oldest_file.Delete()
    if not keep_archives:
        os.remove(path_archive)

if __name__ == '__main__':
    # date config
    config = read_config()
    template_name = change_template(config["template"])
    archive_name = template_name + ".zip"
    path_archive = config["backup_path"] + "\\" + archive_name
    keep_archives = config["keep_local_archives"]

    # functia care face zipul
    zip(template_name,config["target_path"],config["backup_path"])

    # autentificare la drive
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)

    # functia incarcare in drive
    upload(path_archive,config["drive_target_directory_id"])

    # functia stergere a cea mai veche in drive
    erase(path_archive,keep_archives)
