# dl_attachments
Download and print email attachments. 

## Setup 🔧
clone the repo and change to directory:
~~~
git clone https://github.com/dch42/dl_attachments.git && cd dl_attachments
~~~

Running `make` will install dependencies and add executable permissions to relevant scripts.

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
    - print downloaded attachments (if called without `d`, will print all in dl dir)
- `-s, --seenflag`
    - set `seen` flag on processed emails (imap conn read only if not invoked)
- `-u, --unseen`
    - search for messages marked `unseen`
- `-a, --address [ADDRESS...]`
    - search for messages from address(es)
- `-i, --inbox [INBOX...]`
    - search inbox(es)
    
## To-Do/WIP
- convert pesky .docs to pdf 
- add secondary printer cfg and args
- add subject query arg