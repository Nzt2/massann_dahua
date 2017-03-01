# Masscan-Dahua
Script to search in the range IP adress DVR, NVR, IPC Dahua
with the default settings.
And forms of XML device file for use in the import to program Smart PSS
## Status: Work in Progress
- Linux version don`t work

## Requirements
- Python 3
- masscan - from [masscan](https://github.com/robertdavidgraham/masscan)
- Smart PSS - from [Smart Pss] (http://www.dahuasecurity.com/download_2.html)

### Usage
`./masscan_dahua.py -f scan.txt -t threads number`

import Ip_Smart_pss.xml to Smart Pss
