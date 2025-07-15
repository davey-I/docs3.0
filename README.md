# docs3.0
- dependencies are captured in requirements.txt

- After pulling the repo, the same Env. can be created by executing:

 -> python3 -m venv venv
 -> source venv/bin/activate
 -> pip install -r requirements.txt

- After ENV is ready run the server:

 -> python server.py
 
- Desktop entry can be created by using
# DON'T use "~" for home-path, it won't work..
[Desktop Entry]
Type=Application
Terminal=true
Name=Docs 3.0
Icon=${HOMEPATH}/src/docs3.0/desktop-icon.svg
Exec=${HOMEPATH}/src/docs3.0/desktop-entry-script.sh
Comment=Start Docs3.0
Categories=Application;
