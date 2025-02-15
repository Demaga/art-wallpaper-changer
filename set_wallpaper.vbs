' Create WScript Shell object
Set oShell = CreateObject("WScript.Shell")

' Python code as a string (escape any double quotes with "")
strPythonCode = "import os" & vbNewLine & _
                "import ctypes" & vbNewLine & _
                "user_dir = os.environ['USERPROFILE']" & vbNewLine & _
                "img_dir = user_dir + '/art_wallpapers'" & vbNewLine & _
                "imgs = os.listdir(img_dir)" & vbNewLine & _
                "imgs = list(filter(lambda x: '_orig' not in x, imgs))" & vbNewLine & _
                "latest_img = imgs[-1]" & vbNewLine & _
                "abs_path = os.path.abspath(img_dir + '/' + latest_img)" & vbNewLine & _
                "ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)"

' Create a temporary .py file
Set fso = CreateObject("Scripting.FileSystemObject")
tempFile = fso.GetSpecialFolder(2) & "\temp_wallpaper_script.py"
Set ts = fso.CreateTextFile(tempFile, True)
ts.Write strPythonCode
ts.Close

' Build the command to execute Python with arguments
' Modify the Python path as needed
pythonCmd = "python """ & tempFile & """ arg1 arg2"

' Execute the Python code
oShell.Run "cmd /c " & pythonCmd, 0, True

' Clean up the temporary file
fso.DeleteFile tempFile