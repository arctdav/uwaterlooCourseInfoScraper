# Web Scraper for Uwaterloo course information

This Python library scraps all UWaterloo course information from its website: http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html

This library only supports Python3.6+

Please do not spam their website. 

## Getting Started

Make sure you have Python 3.6+

### Prerequisites

In your terminal/shell, type:
```
python -m pip install --upgrade pip
```
Then install bs4, requests

```
python -m pip install requests bs4
```

### Installing

Type the following to terminal/shell to install

```
pip install -i https://test.pypi.org/simple/ uwaterlooCourseInfoScraper
```


If installation successful, you will see something like this:

```
Successfully installed uwaterlooCourseInfoScraper-1.0.7
```

### A Simple Example

```
import uwaterlooCourseInfoScraper as uwcis

print(uwcis.getCourseEnrollInfo(1201, "CS", 135))
# OUTPUT: 
# Request Successful
# [{'Class': XXXX, 'CompSec': 'LEC 001', 'EnrlCap': 90, 'EnrlTot': 71, 'Instructor': 'XXXX'}, {'Class': XXXX, 'CompSec': 
# 'LEC 002', 'EnrlCap': 90, 'EnrlTot': 65, 'Instructor': 'XXXX'}, {'Class': 6002, 'CompSec': 'TST 201', 'EnrlCap': 180, 
# 'EnrlTot': 136, 'Instructor': 'XXXX'}]
```

## Built With

* [requests](https://requests.readthedocs.io/en/master/) - Python3 HTTP requests package
* [csv](https://docs.python.org/3/library/csv.html) - Python3 Library to interact with .csv files
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Python3 HTML Parser

## Authors

* **arctdav** - *Initial work* - [UW-course-info-scraping](https://github.com/arctdav/UW-course-info-scraping)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

