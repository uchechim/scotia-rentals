# Scotia Rentals

A simple overview of use/purpose.

## Description

"Scotia Rentals" is a full-stack web application that facilitates seamless interactions between landlords and renters, leveraging AWS cloud resources for improved scalability, reliability, and performance. The front end of this application is developed using React and the back end is developed using Flask/Python. 

## Getting Started

### Dependencies

* Working IDE - Preferably VSCode
* Unix or Windows-based Operating System.

### Executing program on a local machine

## Cloud Setup
* Ensure you have created an account on AWS (free-tier would suffice)
* This project currently utilizes 7 services from AWS:
   - VPC
   - ElasticBeanstalk
   - EC2
   - Secrets Manager
   - AWS Backup
   - AWS RDS (Aurora)
   - S3
     
* On your AWS account, create instances using the following services: VPC, EC2, RDS (Aurora), S3, AWS Backup
* Note: The front-end may require more compute power than the minimal settings provided on AWS.
* For the VPC, configure security groups to allow the correct inbound/outbound connections (for simplicity add inbound/outbound anywhere @0.0.0.0).

* Frontend Setup
  
* Ensure you have node installed on your machine -> https://nodejs.org/en/download/package-manager
* Clone this repository into your local machine.
* Navigate (cd) to the "client" folder.
* Run ```npm install``` to install the required dependencies for the front-end application


* Backend Setup
* Step-by-step bullets
```
code blocks for commands
```

## Authors

Uchenna Chima
- https://www.linkedin.com/in/uchenna-chima-15123b152/
- https://www.youtube.com/@uchecodez

## Version History

* 0.2
    * Working on improvements with Davide Pollicino
* 0.1
    * Initial Release (As published on YouTube: https://www.youtube.com/watch?v=f8IwHnqSl2U)
