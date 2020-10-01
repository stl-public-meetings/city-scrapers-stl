# CONTRIBUTING

Before contributing, please read our [code of conduct](https://github.com/stl-public-meetings/city-scrapers-stl/blob/main/CODE_OF_CONDUCT.md). We welcome everyone to
[fill out this form](https://airtable.com/shr7a4qgK9rs2yzle) to join our Slack channel and meet the community!

## Don't want to code?

We have ongoing conversations about what sort of data we should collect and how it should be collected. Help us make these decisions by commenting on issues with a non-coding label and joining our [slack channel](https://airtable.com/shr7a4qgK9rs2yzle).

We always welcome help researching sources for public meetings. Help us answer questions like: Are we scraping events from the right websites? Are there local agencies that we're missing? Should events be updated manually or by a scraper?

If there are any public meetings that you would like us to create a scraper for, please fill out [this form](https://airtable.com/shrFCciN4g1CYLK9A) to make a request.

When reviewing scraper requests, we might consider things such as:

* Are these one-off meetings or recurring?
* If they are one-off meetings, do we expect more in the future to be announced using a similar structure?
* Is there historical data that could also be scraped using the same spider and might that be useful?
* What is the estimated time and effort to write the scraper vs manual entry (i.e. if it takes 2-3 minutes to manually enter a single meeting and there are x number of meetings, how does that compare to the time taken to write the scraper)

# Ready to code with us?

We want this project to be accessible to everyone, especially newcomers to open source and Python in general. Here are some steps for getting started contributing.

If you get stuck, checkout our [troubleshooting section](https://github.com/ledaliang/city-scrapers-stl/blob/0016-documentation/CONTRIBUTING.md#troubleshooting) and feel free to reach out with any questions in [slack](https://airtable.com/shr7a4qgK9rs2yzle).

## 1. Find an open issue to work on

You can find open issues by using the ["help wanted"](https://github.com/stl-public-meetings/city-scrapers-stl/labels/help%20wanted) label. Issues labeled ["good first issue"](https://github.com/stl-public-meetings/city-scrapers-stl/labels/good%20first%20issue) and ["spider"](https://github.com/stl-public-meetings/city-scrapers-stl/labels/spider) are a good starting point for beginners. Issues that are currently being worked on by someone are labeled "claimed".

Each spider is a web scraper that helps us extract meeting information from a government website.

Once you've found an issue that interests you, check out the site and see if the links are still active and if it seems doable to you. If everything looks good, comment on the issue that you're interested, and we'll mark it "claimed" so others know you're working on it. We try to limit contributors to working on one issue at a time.

We ask that you let us know if you are no longer able to work on an issue so that others can have a chance. Any issue that doesn't have acivity for 30 days after being claimed may be reassigned. If an issue labeled "claimed" doesn't have any activity in a month or so, you can comment and ask if it's available.

Notice something that's not working as expected or see a site that we should be scraping? Open an issue to let us know!

## 2. Setup

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

We suggest using [Pipenv](https://pipenv.pypa.io/en/latest/), which is a package management took for Python that combines managing dependencies and virtual environments. After installing Pipenv, run the following command to set up an environment:
```
$ pipenv sync --dev --three
```
The `pipenv shell` command activates the virtual environment. You can exit this environment by running `exit`.

## 3. Make changes

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
The path to your spider is in `city-scrapers-stl/city-scrapers/spiders/`. If you ran the `scrapy genspider` command from above, you will find that it has auto-generated some parse methods.
For those who are new to using [Scrapy](https://docs.scrapy.org/en/latest/index.html), we recommend following this [quick tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html) to get an understanding of how the spiders work.
If you have questions on what the parse methods do or the values of each `Meeting` item, you can read more at the bottom of [this page](https://cityscrapers.org/docs/development/#contribute) or reach out to us with questions. Feel free to refer to a completed spider to get an example of what we are looking for. We wish you happy coding!

## 4. Testing

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

## 5. Open a pull request

In this project, making a pull request is just a way to start a conversation about a piece of code. Whether you're finished with your changes or looking for some feedback, open a pull request.

We have a pull request template that includes a checklist of things to do before a pull request is done. Fill that out as much as you can (don't worry if you can't check everything off at first) when you open the pull request.

We use Github Actions for running checks on code to make review easier. This includes everything from running automated tests of functionality to making sure there's consistent code style. When you open a pull request, you'll see a list of checks below the comments. Passing checks are indicated by green checkmarks, and failing checks with red Xs. You can see outputs from each check by clicking the details link next to them.

### i. New pull requests

Open a new pull request by going to the "Pull requests" tab and clicking on the green "New pull request" button.

Click on "Compare across forks" if you don't immediately see your repository.

# Troubleshooting

### Committing from command line

For those who have never used git inside the terminal before, here is a brief intro on how to commit and push your changes.
```
git add .
git commit -m "<COMMIT MESSAGE>"
git push
```
The `.` will select all of your files, if you only want to commit a specific file, you can replace `.` with a specific file name. Don't forget to push! The commit command will only commit changes locally, you need to push in order to see your changes in GitHub. [Here](https://github.com/UnseenWizzard/git_training) is a tutorial for git if you want to learn more about what exactly these commands are doing.

### Keep to date with our repo

If the `main` branch of your fork is a few commits behind `stl-public-meetings:main`, run the following commands to get `main` synced to your local.

```
git chekout main
git fetch upstream
git merge upstream/main
git push
```

### Use the Scrapy shell to test code
Use the folling commands to open the Scrapy shell:
```
cd /path/to/city-scrapers-stl
pipenv shell
scrapy shell <URL>
```
Scrapy shell is a great way to test out little bits of code. [Here](https://www.youtube.com/watch?list=PLyCZ96_3y5LXfPVZkHjhHRuIWhcjvCyQA&v=7PJ02VtjKhs&feature=emb_logo) is a short video tutorial on how to use it and [here](https://docs.scrapy.org/en/latest/topics/shell.html) is the Scrapy documentation.

# Responsiveness

We'll do our best to be responsive, we encourage you reach out in [Slack](https://airtable.com/shr7a4qgK9rs2yzle). We are a team of full time students so we appreciate your patience.
