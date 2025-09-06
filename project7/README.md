# Project Scenario 🎩
You are a data engineer at a data analytics consulting company. You have been assigned to a project that aims to de-congest the national highways by analyzing the road traffic data from different toll plazas. Each highway is operated by a different toll operator with a different IT setup that uses different file formats. Your job is to collect data available in different formats and consolidate it into a single file.

# Objectives📝
* In this project you will create a shell script using bash commands to:
  * Extract data from a CSV file
  * Extract data from a TSV file
  * Extract data from a fixed-width file
  * Transform the data
  * Load the transformed data into a new CSV file
  * You will then create a `DAG` to call the shell script.

# Reach/Follow me on 🚀<br>
<p align="left">
  <a href="https://www.linkedin.com/in/mohamed-fawzy-936b661b8/" target="_blank" rel="noreferrer"> <img src="https://img.icons8.com/fluency/2x/linkedin.png" alt="linkedIn" width="50" height="50"/> </a>&nbsp&nbsp
  <a href="mailto:fwzymohamed90@gmail.com" target="_blank" rel="noreferrer"> <img src="https://img.icons8.com/fluency/2x/google-logo.png" alt="googleEmail" width="50" height="50"/> </a>&nbsp&nbsp
  <a href="https://www.facebook.com/mohamed.fwzy.14" target="_blank" rel="noreferrer"> <img src="https://cdn.iconscout.com/icon/free/png-256/facebook-262-721949.png" alt="facebook" width="50" height="50"/> </a>
</p>
<br>

# Prepare the lab environment 📦

1. Start Apache Airflow.
2. Download the dataset from the source to the destination /your path directory/airflow/dags using wget command.
  Source:

```bash
https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz
```

<!-- Side Note: Additional Information -->
> Note: While downloading the file in the terminal use the sudo command before the command used to download the file.
# Directions 🗺

### Task 1.1 - Define DAG arguments
* Define the DAG arguments as per the following details:

|       Parameter                | 🔰 Value  
| -------------------------- | :----------------:| 
| owner	                     |   < You may use any dummy name> |
| start_date	               |   today |
| email	                     |   < You may use any dummy email> |
| email_on_failure	         |   True |
| email_on_retry	           |   True |
| retries	                   |   1 |
| retry_delay	               |   5 minutes |


### Task 1.2 - Define the DAG
* Create a DAG as per the following details.

|       Parameter                | 🔰 Value  
| -------------------------- | :----------------:| 
| DAG id	                   |   `ETL_toll_data` |
| Schedule	                 |   Daily once |
| default_args	             |   as you have defined in the previous step |
| description	               |   Apache Airflow Project |

### Task 1.3 - Create a shell script `Extract_Transform_data.sh` and add the following commands to your tasks:
* Write a command to `unzip the data`.
* Use the downloaded data from the URL given in the first part of this project and uncompress it into the destination directory.
<!-- Side Note: Additional Information -->
> Hint: Read through the file `fileformats.txt` to understand the column details.

### Task 1.4 - Update the shell script to add a command to `Extract Data From CSV file`
* You should extract the fields `Rowid`, `Timestamp`, `Anonymized Vehicle number`, and `Vehicle type` from the `vehicle-data.csv` file and save them into a file named `csv_data.csv`.

### Task 1.5 - Update the shell script to add a command to `Extract Data From TSV file`
* You should extract the fields `Number of axles`, `Tollplaza id`, and `Tollplaza code` from the `tollplaza-data.tsv` file and save it into a file named `tsv_data.csv`.

### Task 1.6 - Update the shell script to add a command to `Extract Data From fixed-width file`
* You should extract the fields `Type of Payment code`, and `Vehicle Code` from the fixed width file `payment-data.txt` and save it into a file named `fixed_width_data.csv`.

### Task 1.7 -Update the shell script to add a command to consolidate data `Extracted from previous tasks`
* You should create a single CSV file named `extracted_data.csv` by combining data from the following files:
- csv_data.csv
- tsv_data.csv
- fixed_width_data.csv

* The final CSV file should use the fields in the order given below:
`Rowid`, `Timestamp`, `Anonymized Vehicle number`, `Vehicle type`, `Number of axles`, `Tollplaza id`, `Tollplaza code`, `Type of Payment code`, and `Vehicle Code`

<!-- Side Note: Additional Information -->
> Hint: Use the bash `paste` command.
`paste` command merges lines of files.
Example : `paste file1 file2 > newfile`

### Task 1.8 -. Update the shell script to add a command to `Transform and load the data`
* You should transform the vehicle_type field in `extracted_data.csv` into capital letters and save it into a file named `transformed_data.csv` in the staging directory.
<!-- Side Note: Additional Information -->
> Note: Copy the shell script to /your path/airflow/dags folder

### Task 1.9 - Create a task `extract_transform_load` in the `ETL_toll_data.py` to call the shell script.
* Save the DAG you defined into a file named `ETL_toll_data.py`
* Define the task pipeline as per the details given below:

|       Task                | 🔰 Functionality  
| -------------------------- | :----------------:| 
| First task                 |   `extract_transform_load` |


# SnapShot and Results 📸
* I provided my solution for this project a python file go and check it out.
* After implementations your results at Airflow should look like this:
   ![dag_runs](https://github.com/Mohamed-fawzyy/Airflow-Pipeline/assets/111665714/d4d7c7d3-ae7d-469c-9617-99b4f097631c)

# Contributing 📝
Contributions are welcome! Please open an issue or pull request for any changes or improvements.


























