# Scotia Rentals

The purpose of this application is to create a safe envorionment for landlords and renters to interact with each other. By providing discreet user work flows, scotia rentals aims to provide a flawless user experience that accomodates all parties to their maximum potential.

## Description

"Scotia Rentals" is a full-stack web application that facilitates seamless interactions between landlords and renters, leveraging AWS cloud resources for improved scalability, reliability, and performance. The front end of this application is developed using React and the back end is developed using Flask/Python.

## Getting Started

### High-Level Software Dependencies

- Working IDE - Preferably VSCode
- Unix or Windows-based Operating System.
- AWS Account (free-tier would suffice)
- NodeJS -> https://nodejs.org/en/download/package-manager
- ReactJS -> https://react.dev/learn/installation
- Python 3+ -> https://www.python.org/downloads/
- Pip -> https://packaging.python.org/en/latest/tutorials/installing-packages/

###### _Note: Pip is used to install all required Python libraries such as Flask. For the libraries needed, refer to the "requirements.txt" file located in the "server" directory._

### Hosting Application Locally

#### Cloud Setup

- This project currently utilizes 7 services from AWS:
  - VPC
  - ElasticBeanstalk
  - EC2
  - Secrets Manager
  - AWS Backup
  - AWS RDS (MySQL)
  - S3
- On your AWS account, create instances of the following services: VPC, EC2, RDS (Aurora MySQL Compatible), S3, AWS Backup (Optional Based on your budget)

###### _Note: The front-end may require more compute power than the minimal settings provided for a typical EC2 instance on AWS._

###### _Note: While configuring AWS services, be wary of the prices and opt to choose the options that fit your applications demands and budget._

- For the VPC, configure security groups to allow the correct inbound/outbound connections (for simplicity add inbound/outbound anywhere @0.0.0.0).
- For the RDS, ensure that it's publically accessible & corresponding route tables have IGW's

#### Frontend Setup (Local-Development)

- Clone this repository into your local machine.
- Navigate (cd) to the "client" folder.
- Run `npm install --force` to install the required dependencies for the front-end application
- Run `npm start` to run the front-end application locally.

#### Backend Setup (Local-Development)

- Navigate (cd) to the "server" folder.
- Refer to the requirements.txt and install all required libraries via `pip install {library_name}`
- Create an Access Key via AWS
- Retrieve the Access key and Secret access key id's via your AWS account and replace the following lines of code in the 'application.py' folder:
  - db_host -> With the endpoint name of the RDS instance created previously
  - db_port -> With the port of the RDS instance created
  - db_user & db_password -> With the credentials used to create the RDS
  - db_name -> With the name you gave to the RDS
  - region_name_val -> With the region name your AWS account is operating in
  - aws_access_key_id_val -> With the id of the access key you created
  - aws_secret_access_key_val -> With the id of the secret access key you created
- Run the backend application using: `python application.py`
- At this point, the application will require you to reconfigure API endpoints to be interactive.
- Once you reach this stage, refer to "Hostng the Application on the Cloud (AWS)" in order to fully integrate and get the application up and running.

### Hosting the Application on the Cloud (AWS)

###### _Note: It is ***HIGHLY*** recommended to complete all previous steps prior to following the subsequent instructions._

#### Frontend Setup

- To configure the front-end using EC2 + NGINX please refer to my video (https://www.youtube.com/watch?v=f8IwHnqSl2U)
- Time Stamp: 8:41 - 14:31

#### Backend Setup

- Navigate (cd) into the "server" folder.
  - Compress the "application.py" and "requirements.txt" files into a single ZIP file
  - On AWS create a new ElasticBeanstalk Application.
    - Use "scotia-rentals.us-east-1.elasticbeanstalk.com" as the domain name
    - Use the latest version of Python as the platform
    - For the Application Code, upload the ZIP file.
    - Update the remaining settings to your discretion (update security group rules accordingly)

## Authors

Uchenna Chima

- https://www.linkedin.com/in/uchenna-chima-15123b152/
- https://www.youtube.com/@uchecodez

## Version History

- 0.2

  - Working on improvements with Davide Pollicino - https://github.com/omonimus1
  - New Features/Improvements
    - Added a detailed README
    - Added Dependency Management with Dependabot.
    - Added Linters (ESLint & Flake8)
    - Integrated a P.O.C Payment feature with Square
    - TODO: Modularized The Application's Backend By Utilizing The MVC Design Pattern
    - TODO: Added Automated tests (e2e & e2n (end-to-end, end-to-node)) using Microsoft Playwright Framework
    - TODO: Added unit tests using PyTest
    - TODO: Integrate CI/CD Pipeline
    - TODO: Containerized Application using Docker

- 0.1

  - Initial Release (As published on YouTube: https://www.youtube.com/watch?v=f8IwHnqSl2U)
