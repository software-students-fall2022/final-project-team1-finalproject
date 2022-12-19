# Prerequisite

* Make sure that you have completed the [README.md](../) steps for setting up the virtual environment.

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

* Go to GitHub Actions and open the most recent successful run of "web scraper workflow".
* Click on that job.
* Look at the details of the job.
* Click on "execute unit tests" section.
* You will then see the coverage details.
