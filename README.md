# dl_attachments
Download and print email attachments. Printing is handled using `lpr`.
Currently only prints `.pdf` files.

## Setup 🔧
clone the repo and change to directory:
~~~
git clone https://github.com/dch42/dl_attachments.git && cd dl_attachments
~~~

Running `make` will install dependencies and add executable permissions to the script.

~~~
make
~~~

### Config

Fill out the configuration file `config.yml`.

Printer information can be found via CUPS web admin interface, or with `lpstat -p -d`.

## Usage

~~~
./dl-attachments.py -dusp -a someaddress@mail.com another@mail.com -i Orders
~~~

### Options
- `-h, --help`
    - show this help message and exit
- `-d, --download`
    - download email attachments
- `-p, --print`
    - print downloaded attachments 
        - *if called without 'd', will print all printable files in dl dir*
- `-s, --seenflag`
    - set 'seen' flag on processed emails after downloading attachments
- `-u, --unseen`
    - search for messages marked 'unseen'
- `-a, --address [ADDRESS...]`
    - search for messages from specific address(es)
- `-i, --inbox [INBOX...]`
    - search specific inbox(es)
- `-t, --terms [TERMS...]`
    - search subjects for specific term(s)
