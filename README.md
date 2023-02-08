# README for mp4toftp

This python script is intended to be called as an 'extrascript' from ukmon-pitools to upload the allnight timelapse to an FTP site.  The uploaded file is named {stationid}_latest.mp4, where stationid is the 6-letter RMS station code such as UK0001. 

The script can also probably be used directly as an "external script" from RMS. However, i've not tested this and so i can't be certain. 

Uploads can be made with ftp, sftp or ftps (ftp with tls). 


## Installation
### Step 1: Download the Software
open a terminal window and type
<pre>
cd ~/source  
git clone https://github.com/markmac99/mp4toftp.git  
cd mp4toftp  
</pre>

### Step 2: Configure the ftp Connection
Edit the configuration file using a text editor, for example
<pre>
nano ~/source/mp4toftp/mp4toftp.ini  
</pre>
Provide the server name, username, password and target folder for your FTP site. 
Select a protocol (FTP, SFTP or FTPS). 
If uploading to the default location on your server just leave the target folder blank. 
Then save and exit the editor. 


### Step 3a: Add the Hook to UKMON-pitools
If you're not using UKMON-pitools, skip ahead to 3b.

If you're  using the 'extrascript' function in ukmon-pitools (for example to contribute to Istrastream), copy the extrascript file from ukmon-pitools to the mp4toftp folder. 
<pre>
cp ~/source/ukmon-pitools/extrascript ~/source/mp4toftp
</pre>

Then create or update the *ukmon-pitools* 'extrascript' file so that it calls mp4toFTP.py:
<pre>
echo /home/pi/source/mp4toftp/mp4toFTP.py > ~/source/ukmon-pitools/extrascript
</pre>

### Step 3b: Add the Hook Directly to RMS
Open the RMS config file in an editor and find the line starting *external_script_path*

If you're contributing to istrastream, this will probably read  
<pre>
external_script_path: /home/pi/source/RMS/iStream/iStream.py
</pre>

Make a note of the path, then update the line to read
<pre>
external_script_path: /home/pi/source/mp4toftp/mp4toFTP.py
</pre>

Now, create a new text file */home/pi/source/mp4toftp/extrascript* containing just the path that you noted earlier. For example if you are contributing to istrastream, then the extrascript file would contain 
<pre>/home/pi/source/RMS/iStream/iStream.py</pre>

## Testing and Manual Use
The script can also be tested by passing a single argument which is the dated folder name you want to upload from. For example
<pre>
python ~/source/mp4toftp/mp4toFTP.py UK0006_20220511_043312_012356
</pre>
You should see some messages in the terminal window, and a logfile is also created in ~/RMS_data/logs. The logfile name starts with ftpu_. Note that any extrascript you've configured will be called. 

Questions and Requests
----------------------
Contact me via the email address in github, or by raising an Issue on this repository. 
