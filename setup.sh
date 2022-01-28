#!/bin/sh

declare personal_bin="/Users/$USER/bin"
declare cfg=".bash_profile"

eval pip3 install -r requirements.txt

[ -n $ZSH_VERSION ] && 
cfg=".zprofile"

[[ -d $personal_bin ]] || mkdir $personal_bin &&
echo export PATH="$personal_bin:\$PATH" >> /Users/$USER/$cfg

chmod +x ./dl_attachments.py &&
cp ./dl_attachments.py $personal_bin/dla