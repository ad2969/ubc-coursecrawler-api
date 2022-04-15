![Heroku](https://heroku-badge.herokuapp.com/?app=ubc-coursecrawler-api&root=test)

# ubc-coursecrawler-api
Web-scraping API for UBC Coursecrawler. The frontend counterpart is [here](https://github.com/ad2969/ubc-coursecrawler)

> **Status** - v0.1 Prototype. See the [CHANGELOG](CHANGELOG.md).

**Technology Stack**:
- [Django](https://www.djangoproject.com/) web framework, for implementing API logic
- [Selenium](https://www.selenium.dev/), for running the browser driver for scraping
- [Redis](https://redis.io/) database, for storing data
- [Heroku](https://www.heroku.com/), for hosting the application

**Current functionality**:
- Retrieves (by recursive scraping through university websites)
- Stores (caches) scraped data into redis cloud db.

**Supported institutions**:
- [University of British Columbia (UBC)](https://courses.students.ubc.ca/cs/courseschedule)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development. See [development](#development) for best practices/specific notes on the repository and see [deployment](#deployment) for notes on how to deploy the project onto the live system.
### Prerequisites

- Python, v3.9.12 (Download [here](https://www.python.org/downloads/))
- Pipenv, version 2021.11.15 (Download [here](https://pypi.org/project/pipenv/))

### Installation and Running

1. Clone the repo:

    ```
    $ git clone https://github.com/ad2969/ubc-coursecrawler-api
    ```

2. Install the packages:

    ```
    $ cd ubc-coursecrawler-api
    ```

    and

    ```
    $ pipenv install
    ```

3. Download the latest version of [chromedriver](https://chromedriver.chromium.org/downloads) and place in the root directory (or somewhere convenient)

4. Setup your [environmental files](#environmental-files)

5. Start the local server by running the following in the repo directory:

   ```
   $ pipenv run python3 manage.py runserver
   ```

   > By default, django should run on port *8000*

<hr />

## Development

Development is recommended to be done on a system where [pylint](https://pypi.org/project/pylint/) is installed, and using [VSCode](https://code.visualstudio.com/)
### Code Style

- In order to enforce consistency, use double quotation marks (`"`) where possible, including for comments and docstrings. Single quotation marks can be used inside comments.

### Environmental Files

Dotenv files (`.env.*`) are not included in the repository. They contain sensitive variables that are important for running the API. If it's your first time, request them from one of the [repository moderators](#repository-moderators).

Additionally, if developing locally, you will need to add a new variable, `CHROMEDRIVER_PATH`, that contains the path to a valid [chromedriver](https://chromedriver.chromium.org/home)

### Files and Services

:warning: TO-DO: Organize and document filing system.

### Testing and Documentation

:warning: TO-DO: Create swagger documentation for the API.

### Deployment

:warning: TO-DO: Create staging environment.

The API is hosted on a [Heroku](https://www.heroku.com/) server with customized buildpacks to run the selenium driver.

1. To deploy the application to Heroku, you'll need to setup authentication to Heroku on your local machine. Contact one of the [repository moderators](#repository-moderators) to do this.

2. After setting up Heroku locally, run the scripts in `/scripts/heroku-deploy.sh` to launch a deployment.

3. Document new releases in the [CHANGELOG](CHANGELOG.md). Release versioning will follow concepts specified by Tom Preston-Werner's [semver](https://semver.org/)


## Scripts

- `$ python3 manage.py runserver` - Spins up the Django server, hot-reloads on changes

- `$ python3 manage.py makemigrations` - (unused) Creates the migrations - SQL scripts - from the defined models

- `$ python3 manage.py migrate` - (unused) Runs the migrations - SQL scripts - that were created


## Contributing

See [CONTRIBUTING][CONTRIBUTING.md]
