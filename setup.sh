#!/bin/sh

declare script_name="dla"
declare personal_bin="/Users/$USER/bin"
declare hidden_dir="/Users/$USER/.$script_name"
declare cfg=".bash_profile"

declare grn="\e[0;92m"
declare red="\e[0;91m"
declare reset="\e[0m"

function make_dir {
    printf "Creating dir $personal_bin...\n" && 
    mkdir $personal_bin
    }

function add_to_path {
    printf "Adding '$personal_bin' to \$PATH in $cfg...\n" & 
    echo export PATH="$personal_bin:\$PATH" >> /Users/$USER/$cfg
}

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
###############################################################
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

printf "\nAttempting installation of script '$script_name'...\n\n"

echo "Installing requirements..."
eval pip3 install -r requirements.txt

[ -n $ZSH_VERSION ] && 
cfg=".zprofile"

[[ ! -d $personal_bin ]] && 
make_dir ||
printf "'$personal_bin' exists...\n"

grep -q "$personal_bin" /Users/$USER/$cfg && 
printf "'$personal_bin' already in \$PATH...\n" ||
add_to_path

echo "Installing $script_name..."
chmod +x ./${script_name}.py &&
cp ./${script_name}.py $personal_bin/$script_name &&
printf "${grn}[SUCCESS]${reset} Script $script_name installed at '$personal_bin/$script'!\n\n" ||
printf "${red}[ERROR]${reset} Something went wrong...\n" exit 1

[[ ! -d $hidden_dir ]] &&
mkdir -pv $hidden_dir

read -p "Config file will now open, please hit 'ENTER' and fill in the required info..."
nano ./config.yml &&
cp ./config.yml  ${hidden_dir}/${script_name}_config.yml &&
cp ./cfg_crypt.py $personal_bin &&
printf "Config file moved to ${hidden_dir}/${script_name}_config.yml...\n"
printf "${grn}[SUCCESS]${reset} For help, invoke '$script_name -h'\n"
exit 0