# Image downloader by query

## Installation.

```bash
git clone https://github.com/Kichkun/image_downloader.git
cd image_downloader
pip install .
```

or just install the requirements

```bash
git clone https://github.com/Kichkun/image_downloader.git
cd image_downloader
pip install -r requirements.txt
```

You will also need to install Google Chrome and [chromedriver](https://4admin.space/all/ustanovka-chromedriver-na-macos-high-sierra-dlya-selenium)


**Usage**

- -s - Phrase for search
- -c - Path to chromedriver
- -d - Save images with faces only
- -o - Location of output results
- -b - Launch Google Chrome to be able to see and control the results or to do everything in background

**Example**
```bash
python parser.py -s 'some search' -d True -o 'any folder' -b True
```
