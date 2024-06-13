# Scotia Rentals

The purpose for this application is to create a safe envorionment for landlords and renters to interact with eachother. By providing discreet user work flows, scotia rentals aims to provide a flawless user experience that accomodates all parties to their maximum potential.

## Description

"Scotia Rentals" is a full-stack web application that facilitates seamless interactions between landlords and renters, leveraging AWS cloud resources for improved scalability, reliability, and performance. The front end of this application is developed using React and the back end is developed using Flask/Python. 

## Getting Started

### Dependencies

* Working IDE - Preferably VSCode
* Unix or Windows-based Operating System.
* AWS Account (free-tier would suffice)
* NodeJS -> https://nodejs.org/en/download/package-manager
* ReactJS -> https://react.dev/learn/installation
* Python 3+ -> https://www.python.org/downloads/
* Pip -> https://packaging.python.org/en/latest/tutorials/installing-packages/
###### _Note: Pip is used to install all required Python libraries such as Flask. For the libraries needed, refer to the "requirements.txt" file located in the "server" directory._

### Hosting Application Locally

#### Cloud Setup
* This project currently utilizes 7 services from AWS:
   - VPC
   - ElasticBeanstalk
   - EC2
   - Secrets Manager
   - AWS Backup
   - AWS RDS (Aurora)
   - S3
     
* On your AWS account, create instances using the following services: VPC, EC2, RDS (Aurora), S3, AWS Backup
###### _Note: The front-end may require more compute power than the minimal settings provided for a typical EC2 instance on AWS._
* For the VPC, configure security groups to allow the correct inbound/outbound connections (for simplicity add inbound/outbound anywhere @0.0.0.0).

#### Frontend Setup (Local-Development)
* Clone this repository into your local machine.
* Navigate (cd) to the "client" folder.
* Run ```npm install --force``` to install the required dependencies for the front-end application
* Run ```npm start``` to run the front-end application locally.

#### Backend Setup (Local-Development)
* Step-by-step bullets
```
code blocks for commands
```

### Hosting the Application on the cloud - 
###### _Note: It is ***HIGHLY*** recommended to complete all previous steps prior to following the subsequent instructions._

#### Cloud Setup

#### Frontend Setup (Local-Development)

#### Backend Setup (Local-Development)


## Authors

Uchenna Chima
- https://www.linkedin.com/in/uchenna-chima-15123b152/
- https://www.youtube.com/@uchecodez

## Version History

* 0.2
    * Working on improvements with Davide Pollicino
* 0.1
    * Initial Release (As published on YouTube: https://www.youtube.com/watch?v=f8IwHnqSl2U)
