# Tesseract PDF Reader OCR
A simple application that reads a PDF file
and parses the text using the Tesseract OCR.

## Execution
Make sure Tesseract is installed. If it isn't in the PATH
environment variable, add it, or set/export TESSERACT_CMD
as the location of the Tesseract executable binary.
E. g.
- Bash
  ``` bash
  export TESSERACT_CMD='/path/to/tesseract'
  ```
- PowerShell
  ``` powershell
  $Env:Tesseract_Cmd = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```
- Windows Command Prompt
  ``` cmd
  set "TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe"
  ```

Windows and Macintosh users would also need to have Poppler installed and added to PATH, which can be downloaded [here](https://blog.alivate.com.au/poppler-windows/).
Alternatively, it can be installed using Miniconda/Anaconda on Windows.
```
conda install -c conda-forge poppler
```
On Mac, it can be installed using `brew`./
```
brew install poppler
```
Most Linux distributions will already have it installed. If not, it will need to be installed manually.
```
sudo apt install poppler-utils
```

Once that has been finalized, install the other Python requirements.
```
pip3 install -r requirements.txt
```

After that, execute `reader.py` using Python 3 or above.
```
python reader.py
```

Enter the location of the PDF file. The output will be generated in the `out/txt/out_text.txt` file.

## Note
Don't expect outstanding results
when using a PDF file already containing parsed text. It might
so happen that the resulting image generated from the text
is wrongly parsed.

<div align='center'>Made with ❤ by Manvendra and Param</div>