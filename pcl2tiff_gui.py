import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from PIL import Image
import os

def pcl_to_png(pcl_file, output_png):
    ghostscript_path = r'ghostpcl-10.04.0-win64\ghostpcl-10.04.0-win64\gpcl6win64.exe'

    command = [
        ghostscript_path, 
        '-sDEVICE=png16m',  # Ausgabe in 16-bit
        f'-sOutputFile={output_png}',  # Ausgabe-PNG-Datei
        '-r600',  # Ausgabe in 600 DPI
        '-dNOPAUSE', # Usereingaben in Ghostpcl überspringen
        '-dBATCH',
        '-dSAFER',
        '-dQUIET',
        pcl_file,  # Eingabe-PCL-Datei
        '-dNOPAUSE', 
        '-dBATCH', 
        '-dSAFER', 
        '-dQUIET', 
    ]
    

    subprocess.run(command, check=True)

def png_to_tiff(png_file, output_tiff):
    with Image.open(png_file) as img:
        # speichert das .tiff in 600 dpi, wie die eingelesene .png
        img.save(output_tiff, format='TIFF', dpi=(600, 600))

def pcl_to_tiff(pcl_file, output_tiff):
    temp_png = 'temp_output.png'
    pcl_to_png(pcl_file, temp_png)
    png_to_tiff(temp_png, output_tiff)
    if os.path.exists(temp_png):
        os.remove(temp_png)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PCL Dateien", "*.pcl")])
    if file_path:
        entry_pcl_file.delete(0, tk.END)
        entry_pcl_file.insert(0, file_path)

def convert_file():
    pcl_file = entry_pcl_file.get()
    output_tiff = filedialog.asksaveasfilename(defaultextension=".tiff",
                                                 filetypes=[("TIFF Dateien", "*.tiff")])
    if pcl_file and output_tiff:
        try:
            pcl_to_tiff(pcl_file, output_tiff)
            messagebox.showinfo("Fertig", f"Die Datei wurde erfolgreich konvertiert: {output_tiff}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

root = tk.Tk()
root.title("PCL zu TIFF Konverter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Wählen Sie eine PCL-Datei:")
label.pack()

entry_pcl_file = tk.Entry(frame, width=50)
entry_pcl_file.pack(side=tk.LEFT, padx=(0, 10))

btn_browse = tk.Button(frame, text="Durchsuchen", command=browse_file)
btn_browse.pack(side=tk.LEFT)

btn_convert = tk.Button(root, text="Konvertieren", command=convert_file)
btn_convert.pack(pady=(10, 0))

root.mainloop()
