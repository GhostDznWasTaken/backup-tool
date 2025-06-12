import os,shutil,json
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# selectare director -> zipfile -> redenumire zip -> mutare zip

#functie care deschide si citeste configu
def read_config():
    with open('config.json', 'r') as file:
        data = json.load(file)
        return data

#functia care face rost de timp(data+ora) + schimba numele
def change_template(nume: str):
    now = datetime.now()
    #variabile de timp separate
    ora = now.strftime("%H")
    minut = now.strftime("%M")
    secunda = now.strftime("%S")
    zi = now.strftime("%d")
    luna = now.strftime("%m")
    an = now.strftime("%Y")
    nume = nume.replace("%hh%",ora).replace("%MM%", minut).replace("%ss%", secunda).replace("%dd%", zi).replace("%mm%", luna).replace("%yyyy%", an)
    return nume

#functia care face arhiva
def zip(nume,inp,out):
    nume = nume
    in_path = inp
    out_path = out
    arhiva = shutil.make_archive(nume, 'zip', in_path)
    cale_noua = os.path.join(out_path, os.path.basename(arhiva))
    shutil.move(arhiva, cale_noua)

def incarcare(nume,folder_id):
    file_path = nume
    file = drive.CreateFile({'title': nume,
                            'parents': [{'id': folder_id}]})
    file.SetContentFile(file_path)
    file.Upload()

def stergere():
    file_list = drive.ListFile({'q': "title contains '.zip' and trashed=false"}).GetList()
    if len(file_list) <= 3:
        return
    else:

        file_list.sort(key=lambda f: datetime.strptime(f['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ"))

        # Cel mai vechi fișier
        oldest_file = file_list[0]

        # Șterge fișierul
        oldest_file.Delete()

if __name__ == '__main__':
    #functia care imi preia datele din config
    config = read_config()
    #functia care schimba template-ul din config
    nume_template = change_template(config["template"])
    nume_arhiva = nume_template + ".zip"
    path_arhiva = config["backup_path"] + "\\" + nume_arhiva
    #functia care face zipul
    zip(nume_template,config["world_path"],config["backup_path"])
    #autentificare la drive
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
    #functia incarcare in drive
    incarcare(path_arhiva,config["drive_target_directory_id"])
    #functia stergere a cea mai veche in drive
    stergere()
