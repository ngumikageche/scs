#  Spam Classification System

## Installation Requirements
- Python v3.8 or greater
- Ubuntu version 20.04.6

## Installation Instructions

### Setting up the Project
  1. clone the repo
  2. create a vertual environment using 
    ```
    python3 -m venv venv
    ```
  3. activate the virtual env 
  ```
  source venv/bin/activate
  ```
  4. install the requirements 
  ```
  pip install -r requirements.txt
  ```
  6. setup the sqlserver learn here https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04
  7. intialize the tables and first user  
    ```
    python3 initialize_db_table.py
    ```
  8. run the project
  ```
  python3 run.py
  ```
  9. go to your browser and go to 127.0.0.1:8000
  
