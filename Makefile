#---------------------------------------------------------------------
# Install deps & add exec permissions
#---------------------------------------------------------------------

init:
	pip3 install -r requirements.txt
	chmod +x ./dl_attachments.py
	nano config.yml
