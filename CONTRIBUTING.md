# CONTRIBUTING

Before contributing, please read our [code of conduct](https://github.com/stl-public-meetings/city-scrapers-stl/blob/main/CODE_OF_CONDUCT.md)

## Steps

We want this project to be accessible to everyone, especially newcomers to open source and Python in general. Here are some steps for getting started contributing.

# 1. Find an open issue to work on

You can find open issues by using the ["help wanted"](https://github.com/stl-public-meetings/city-scrapers-stl/labels/help%20wanted) label. Issues labeled ["good first issue"](https://github.com/stl-public-meetings/city-scrapers-stl/labels/good%20first%20issue) and ["spider"](https://github.com/stl-public-meetings/city-scrapers-stl/labels/spider) are a good starting point for beginners. Issues that are currently being worked on by someone are labeled "claimed".

Each spider is a web scraper that helps us extract meeting information from a government website.

Once you've found an issue that interests you, check out the site and see if the links are still active and if it seems doable to you. If everything looks good, comment on the issue that you're interested, and we'll mark it "claimed" so others know you're working on it. We try to limit contributors to working on one issue at a time.

We ask that you let us know if you are no longer able to work on an issue so that others can have a chance. Any issue that doesn't have acivity for 30 days after being claimed may be reassigned. If an issue labeled "claimed" doesn't have any activity in a month or so, you can comment and ask if it's available.

Notice something that's not working as expected or see a site that we should be scraping? Open an issue to let us know!

# 2. Setup

### i. Fork the Repository
If this is your first time contributing to this project, fork our repository by clicking on the "fork" button in the top right corner.
### ii. Clone the fork to your local machine
```
$ git clone https://github.com/YOUR-USERNAME/city-scrapers-stl.git
```
In order to keep your fork up to date with the main repository, we recommend configuring Git to sync your fork.
```
$ git remote add upstream https://github.com/stl-public-meetings/city-scrapers-stl.git
```
Here are some more resources on [forking a repo](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) and [syncing a fork](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork).

### iii. Change directories into the main project folder
```
$ cd city-scrapers-stl
```

### iv. Install dependencies
We suggest using [Pipenv](https://pipenv.pypa.io/en/latest/), which is a package management took for Python that combines managing dependencies and virtual environemnts. After installing Pipenv, run the following command to set up an environment:
```
$ pipenv shell
$ sync --dev --three
```
The `pipenv shell` command activates the virtual environment. You can exit this environment by running `exit`.

# 3. Make changes

### i. Create a new branch
It is good practice to make a new branch for each new issue.
```
$ git checkout -b XXXX-spider-NAMEOFAGENCY
```
`XXXX` is the zero-padded issue number and `NAMEOFAGENCY` is listed in the issue description and should be something like `cc_horticulture`.

### ii. Create a spider
Create a spider from our template with a spider slug, agency name, and a URL to start scraping. Below is an example of generating a spider inside the virtual environment.
```
$ pipenv shell
$ scrapy genspider cc_horticulture "Creve Coeur Horticulture, Ecology and Beautification Committee" https://crevecoeurcitymo.iqm2.com/Citizens/Calendar.aspx
```

### iii. Write the parse methods.
If you have questions on what the parse methods do or the values of each `Meeting` item, you can read more at the bottom of [this page](https://cityscrapers.org/docs/development/#contribute) or reach out to us with questions. Feel free to refer to a completed spider to get an example of what we are looking for. We wish you happy coding!

# 4. Testing

### i. Test crawling
Using the same example as we did above, we have now created a spider named `cc_horticulture`. To run it, run:
```
$ pipenv shell
$ scrapy crawl cc_horticulture
```

### ii. Run the automated tests.
We use the [pytest](https://docs.pytest.org/en/latest/) testing framework to verify the behavior of the project's code. To run this, simply run `pytest` in your project environment.
```
$ pipenv shell
$ pytest
```

### iii. Run linting and style-checking tools
We use [flake8](https://flake8.pycqa.org/en/latest/), [isort](https://isort.readthedocs.io/en/stable/), and [black](https://github.com/psf/black) to check that all code is written in the proper style. To run these tools individually, you can run the following commands:
```
$ pipenv run isort
$ pipenv run black city_scrapers tests
$ pipenv run flake8
```

# 5. Open a pull request
In this project, making a pull request is just a way to start a conversation about a piece of code. Wheter you're finished with your changes or looking for some feedbac, open a pull request.

We have a pull request template that includes a checlist of things to do before a pull request is done. Fill that out as much as you can (don't worry if you can't check everything off at first) when you open the pull request.

We use Github Actions for running checks on code to make review easier. This includes everything from running automated tests of functionality to making sure there's consistent code style. When you open a pull request, you'll see a list of checks below the comments. Passing checks are indicated by green checkmarks, and failing checks with red Xs. You can see outputs from each check by clicking the details link next to them.

### i. New pull requests
Open a new pull request by going to the "Pull requests" tab and clicking on the green "New pull request" button.

Click on "Compare accross forks" if you don't immediately see your repository.
