# PH COA 2020 National Government Audit Data Scraper
---
### _NOTE: Results cannot be replicated as COA website now has a CAPTCHA._
---
### Supported Platform
The code is written in **Python**.
Since .doc files require conversion to .docx, only **Windows with Microsoft Word** is supported for now.

If your platform is currently unsupported, you may still download the extracted text from the `txt/` directory in this repository.

### Contents
- [Disclaimer](#disclaimer)
- [Installation](#installation)
- [Running the Scripts](#running)
- [Exploring the Dataset](#explore)
- [Analyzing the Dataset](#analyze)
- [Visualizing the Dataset](#visualize)

<a name="disclaimer"></a>
## Disclaimer
The owner of this repository is not in any way affiliated with the Commission on Audit (COA) or the Philippine National Government. This is a purely private endeavor to make COA document data more accessible for text analysis methods.

Source: https://coa.gov.ph/index.php/national-government-agencies/2020/

<a name="installation"></a>
## Installation
Navigate to the repository folder and create a virtual environment.
```
cd coa-dataset
python -m venv .
```
_For more information on virtual environments, see the [venv module documentation](https://docs.python.org/3/library/venv.html)._

Activate the virtual environment and install the required packages from `requirements.txt`.
```
Scripts\activate.bat
pip install -r requirements.txt
```
The `docx2python` module is already available at `Lib/site-packages` as edits were made to obtain more properties from .docx files. A pull request for this feature is [currently pending](https://github.com/ShayHill/docx2python/pull/22).

<a name="running"></a>
## Running the Scripts
The scripts should be executed in the following order:
1. `fullprocess.py`-
  This runs `ripper.py` and `downloader.py`. The global variable `ZIP_PATH` corresponding to .ZIP download path can be edited by changing the respective `global_vars` dictionary key.

    1. `ripper.py` - This creates `fstruct.json` corresponding to the hierarchy of government agencies and `links.json` which lists government agencies and respective links.

    1. `downloader.py` - This creates `com2zip.json` which lists government agencies and .ZIP filenames containing their data.

1. `unzipper.py` - This unzips the .ZIP files in `ZIP_PATH` to `DEST` and creates `com2files.json` to log the process.

1. `to_text.py` - This parses files in `DEST` whose filenames match the groups in `AUD_DOC` to .TXT files in `TXT`. Supplying multiple regex expressions results in types corresponding to 0-indexed group index, e.g. first expression is `{"type": 0}`. A log of scraped files and their properties can be found in `file2txtlog.json`. Files with errors and government agencies that whose filenames did not match the regular expression are reported in the `unhandled` key.

<a name="explore"></a>
## Exploring the Dataset
Text files in the `txt/` directory contains data on government agencies with an Executive Summary. If there is none, the following are accessed in order of availability: Audit Report, Management Letter, and Observations.

Document type, page count and other properties may be obtained from `file2txtlog.json`.

<a name="analyze"></a>
## Analyzing the Dataset
File data is available in the `properties/` folder.
- `bdt.csv` - count and sum data by `type` (Regex match string)
- `docx.csv` - docx files' data as .csv
- `pdf.csv` - pdf files' data as .csv
- `bigdf.csv` - docx and pdf data combined
- `text_analysis.csv` - text features of each parsed document
- `no_ratings.csv` - text features -> word frequencies of each document to explain 'no opinion/rating'

For data analysis, `bigdf.csv` should provide an overview of the files while `text_analysis.csv` gives basic features that may be generated from the text files.

To replicate the creation of these files, install additional packages from `requirements_a.txt` and run `get_properties.py`.
```
pip install -r requirements_a.txt
python get_properties.py
```

<a name="visualize"></a>
## Visualizing the Data
<div class='tableauPlaceholder' id='viz1629884278708' style='position: relative' align='center'><noscript><a href='https://public.tableau.com/app/profile/kgreyy/viz/2020COAAnnualAuditReportsViz/Overviewof2020COAAnnualAuditReports' target='_blank'><img alt='Overview of 2020 COA Annual Audit Reports ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;20&#47;2020COAAnnualAuditReportsViz&#47;Overviewof2020COAAnnualAuditReports&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='2020COAAnnualAuditReportsViz&#47;Overviewof2020COAAnnualAuditReports' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;20&#47;2020COAAnnualAuditReportsViz&#47;Overviewof2020COAAnnualAuditReports&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>

---

### TODO:
- [ ] TF-IDF Analysis
- [ ] Parse tables/accounting metrics
- [ ] Make charts!
