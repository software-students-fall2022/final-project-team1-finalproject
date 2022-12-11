# Prerequisite

* Make sure that you have completed the [README.md](../README.md) steps for setting up the virtual environment.

# Get Code Coverage information

* cd to the web-scraper directory. Assuming you are currently at this directory, run the following:
    ```
    cd ../
    ```
* Run pytest with coverage
    ```
    pytest --cov
    ```

# Alternative way to get coverage information

* Go to GitHub Actions and look at the most recent successful run of the unit tests.
* Open the details of the job. It is under the "Jobs" section of the navigation bar.
* Click on "execute unit tests" section.
* You will then see the coverage details.