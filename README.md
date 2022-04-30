# dl_attachments
CLI script to conditionally download and print attachment files from email inboxes, invoked as `dla`. Printing is handled using `lpr`.
Currently only prints `.pdf` files.

Handy for dealing with large amounts of daily orders, labels, or other printable documents sent via email.

Can be easily run as a cronjob.

## Setup 🔧
Clone the repo and change to directory:
~~~
git clone https://github.com/dch42/dl_attachments.git && cd dl_attachments
~~~

Add exec permissions and run `setup.sh`:
~~~
chmod +x ./setup.sh && ./setup.sh
~~~
This will install dependencies and install the script as `dla` in /Users/$USER/bin, as well as add to bash or zsh $PATH.

### Config

Fill out the configuration file: `config.yml`.

Printer information can be found via CUPS web admin interface, or with `lpstat -p -d`.

~~~
# Download Directory
#   Place path to download attachments to:
DOWNLOAD_DIRECTORY: "/data/downloads/"
EXTENSIONS_TO_DOWNLOAD: [".pdf"]


# Email Account Info 
#   Place your imap server info here:  
IMAP_INFO:
  IMAP_HOST: "imap.host.com"
  PORT: 993
  ROOT_INBOX: "Inbox"

MAIN_PRINTER: "PrinterCo_5500_3"
MEDIA: "Letter"
~~~


## Usage

Invoke like so:

~~~
dla -dusp -a someaddress@mail.com another@mail.com -i Orders -t urgent
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
