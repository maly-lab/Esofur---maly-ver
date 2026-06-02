This is a upload of the EsoFur-Interpreter by TaseTheFox (link:https://github.com/TaserTheFox/EsoFur-Interpreter) but with clanker (AI) modifications.
I wanted to use the langauge but it was missing some features and I didn't want to mess with the code myself tbh so I just got a clanker to do it.

Changes made:

enabled konsole/command prompt usage:
	Linux:
		1. download/clone repo
		2. run in konsole:
		cd EsoFur-Interpreter
		chmod +x install.sh
		./install.sh
	Windows:
		1. download/clone repo
		2. open command prompt and run one of the options:
			1. install.bat
			2. python esofur_engine.py test.EsoFur
	To run .EsoFur files use:
	1. esofur {file path}
	2. esofur run {file path}
	
	There is a test file in the repo call test.EsoFur
	Make sure to use the full or relative file path
	and that the file is a EsoFur file
	
	To write and edit in cmd prompt or Konsole use run: esofur
	Pasting code here breaks how the console looks 
	but if you press enter it should still run
	(This code cant be saved though does work if you want to just mess around)
	
Enabled VS code use by pressing ctrl+shift+b/f5 (whatever u prefer):
	To do this open up a folder with the file you want to run
	
	create a new folder called .vscode in the folder:
	
		create a file called tasks.json and copy the code from vs_tasks.txt (in the repo docs folder)
			- this enables you to run the code using ctrl+shift+b
			
		create a file called launch.json and copy the code from vs_launch.txt (in the repo docs folder)
			- will not work without tasks.json set-up
			- enables you to press f5 to run code

Commands can be found in "EsoFur Modules.txt"
