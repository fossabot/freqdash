<h1 align="center">
<img src="https://user-images.githubusercontent.com/51025241/209450888-c9160c81-38d8-44dd-93d9-96b4a6922074.png">
</h1>

<p align="center">
A python (3.11+) and Fastapi script to display a dashboard for your <a href="https://www.freqtrade.io/en/stable/">freqtrade</a> database(s).
</p>
<p align="center">
<img alt="GitHub Pipenv locked Python version" src="https://img.shields.io/github/pipenv/locked/python-version/ecoppen/freqdash">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Quickstart
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fecoppen%2Ffreqdash.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fecoppen%2Ffreqdash?ref=badge_shield)


- Clone the repo `git clone https://github.com/ecoppen/freqdash.git`
- Navigate to the repo root `cd freqdash`
- Navigate to the config folder `cd config`
- Create the config file from template `cp config.json.example config.json`
- Populate the `config.json` files as required using a text editor e.g. `nano config.json`
- Navigate back to the repo root `cd ..`
- Install pipenv `pip install pipenv`
- Install required packages `pipenv install`
- Activate the environment `pipenv shell`
- Start the webserver in development mode `uvicorn freqdash.main:app --reload`

### Developers
- Install developer requirements from pipenv `pipenv install --dev`
- Install pre-commit hooks `pre-commit install`


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fecoppen%2Ffreqdash.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fecoppen%2Ffreqdash?ref=badge_large)