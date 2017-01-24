# togbot
A slack bot integrated with Toggl API, for reminders and verification of Toggle reports completion


## Instructions:
1. Generate `conf.yml` containing **SLACK_API_TOKEN** and **TOGGL_API_TOKEN**
2.  ```bash
    docker build -t togbot .
    ```

3.  ```bash
    docker run togbot
    ```