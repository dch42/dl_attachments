#!/bin/sh

declare script_name="dla"
declare personal_bin="/Users/$USER/bin"
declare hidden_dir="/Users/$USER/.$script_name"
declare cfg=".bash_profile"

echo "Installing requirements..."
eval pip3 install -r requirements.txt

[ -n $ZSH_VERSION ] && 
cfg=".zprofile"

echo "Adding $personal_bin to \$PATH..."
[[ -d $personal_bin ]] || mkdir $personal_bin &&
echo export PATH="$personal_bin:\$PATH" >> /Users/$USER/$cfg

echo "Installing $script_name..."
chmod +x ./dl_attachments.py &&
cp ./dl_attachments.py $personal_bin/$script_name &&
echo "[SUCCESS] Installed as '$script_name'." ||
echo "[ERROR] Something went wrong..." exit 1

[[ ! -d $hidden_dir ]] &&
mkdir -pv $hidden_dir

read -p "Config file will now open, please hit 'ENTER' and fill in the required info..."
nano ./config.yml &&
cp ./config.yml  ${hidden_dir}/${script_name}_config.yml &&
cp ./cfg_crypt.py $personal_bin &&
echo "Config file moved to ${hidden_dir}/${script_name}_config.yml..."
echo "[SUCCESS] For help, invoke '$script_name -h'"
exit 0