import os
import glob

files = glob.glob(r"c:\Users\Rishuraj Kumar\NLP-Routing-System\frontend\*.html")
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace uppercase folder paths with lowercase for Linux/Vercel compatibility
    content = content.replace('href="CSS/', 'href="css/')
    content = content.replace('src="JS/', 'src="js/')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print(f"Updated {len(files)} files.")
