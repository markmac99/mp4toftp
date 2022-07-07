README for mp4toftp
===================

This python script is intended to be called as an 'external script' from RMS, the meteor detection
software. 

Installation
------------
open a terminal window and type
<pre>
cd ~/source  
git clone https://github.com/markmac99/mp4toftp.git  
cd mp4toftp  
nano mp4toftp.ini  
</pre>
Enter the target folder, server name, username and password for your FTP site, then save and exit the editor. 


Other Usage
-----------
The script can also be called directly by passing a single argument which is the dated folder name you want to upload eg
<pre>
python ~/source/mp4toftp/mp4ToFTP.py UK0006_20220511_043312_012356
</pre>