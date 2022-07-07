README for mp4toftp
===================

This python script is intended to be called as an 'external script' from RMS, the meteor detection
software. 
Note: The software is designed to chain with RMS and any external script it might already be running such as Istrastream or the UKMON tools.

Installation
------------

**Step 1: Download the Software**  
open a terminal window and type
<pre>
cd ~/source  
git clone https://github.com/markmac99/mp4toftp.git  
cd mp4toftp  
nano mp4toftp.ini  
</pre>
Provide the target folder, server name, username and password for your FTP site, save and exit the editor. 

**Step 2: Add the RMS hooks**

If you're contributing to Istrastream type the following in the terminal window:  
<pre>
echo /home/pi/source/RMS/iStream/iStream.py > ~/source/mp4toftp/extrascript
</pre>

if you're using the UKMON toolset, type the following in the terminal window:  
<pre>
echo /home/pi/source/mp4toftp/mp4ToFTP.py > ~/source/ukmon-pitools/extrascript
</pre>

If you're NOT using the UKMON toolset, you'll need to edit the RMS config file.
* open the file in an editor
* find the line containing **external_script_path**
* replace the value with **/home/pi/source/mp4toftp/mp4ToFTP.py**
* a few lines above this, change external_script_run to **true**
* save and exit

Testing and Manual Use
----------------------
The script can also be tested by passing a single argument which is the dated folder name you want to upload eg
<pre>
python ~/source/mp4toftp/mp4ToFTP.py UK0006_20220511_043312_012356
</pre>
You should see some messages in the terminal window, and a logfile is also created in ~/RMS_data/logs. The logfile name starts with ftpu_