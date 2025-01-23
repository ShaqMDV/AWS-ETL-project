## Brew and Byte

Template for data engineering bootcamp final project repo, including set up of project sprint boards and issues

## Definition Done:

-   Code Completeness

Code is fully written and adheres to team coding standards.
The feature branch passes all automated tests (unit, integration, and performance tests).
Testing

Unit tests cover at least 80% of the codebase for the specific task.
Integration tests validate that the ETL app components work seamlessly together.
Manual testing has been conducted, and edge cases have been reviewed.

-   Functionality

The feature meets the requirements outlined in the task description.
ETL scripts can extract data from the specified source, transform it as per the rules, and load it into the correct destination.
Performance benchmarks for data processing are met (e.g., process X rows in under Y seconds).

-   Code Review

Pull requests are reviewed by at least 1-2 team members.
Feedback from the review is addressed before merging.

-   Documentation

Code is properly documented with clear comments explaining non-obvious logic.
The task includes updates to project documentation (e.g., README.md, API documentation, or pipeline diagrams).
Deployment Readiness

The feature is tested in a staging environment and shows no critical issues.
Deployment scripts or configurations are updated if required.

-   Client Acceptance

The client has reviewed and approved the functionality if it is a client-facing milestone.
Feedback from the client is addressed.
Issue Closure

The Git issue is updated with a clear summary of the changes made.

## Organize Team Retro:

Make sure Vicki and Brian are present scrum fill the information in top of floor.
If any team member is not able to attend the weekly retro should let the scrum master knows their feedback in the question.

# Coffee Shop ETL Pipeline

This project implements an end-to-end Extract, Transform, Load (ETL) pipeline for a coffee shop chain with multiple branches across the country (UK). The goal of this project is to centralize and analyze transactional data from all branches, enabling business insights through a scalable and efficient solution.

---

## **Project Overview**

### **Problem Statement**

The coffee shop chain faces challenges in consolidating and analyzing transactional data due to its current decentralized data setup. This makes it difficult to derive company-wide insights and generate actionable business intelligence.

### **Solution**

This project builds a robust ETL pipeline to:

-   Collect transaction data from individual branches via AWS S3.
-   Transform raw data to align with a predefined schema.
-   Load the transformed data into an AWS Redshift data warehouse.
-   Visualize and analyze data using Grafana.

---

## **Architecture**

### **Technologies Used**

-   **AWS S3**: For storing raw transaction data.
-   **AWS Lambda**: For processing uploaded CSV files.
-   **AWS Redshift**: For centralized storage and querying of transformed data.
-   **Grafana**: For visualizing and analyzing data.
-   **Python**: For the ETL pipeline logic.
-   **Docker**: For local development and testing.

### **Pipeline Steps**

1. **Data Extraction**

    - Upload daily CSV files containing transactional data to an S3 bucket.
    - Lambda function triggers on file upload to initiate processing.

2. **Data Transformation**

    - Parse and clean raw data to align with the Redshift schema.
    - Remove sensitive information such as customer names and credit card details.
    - Normalize data into relational tables: `branches`, `transactions`, `products`, and `product_transactions`.

3. **Data Loading**

    - Load transformed data into Redshift using Redshift SQL COPY commands.

4. **Data Visualization**
    - Connect Redshift to Grafana to enable query-based dashboards and insights.

---

## **How to Deploy the Pipeline**

### **Prerequisites**

-   AWS account with appropriate IAM permissions.
-   AWS CLI configured.
-   Python 3.9 or later.

### **Deployment Steps**

#### **1. Set Up Deployment Bucket**

```bash
bash deploy.sh <AWS_PROFILE> <YOUR_NAME> <TEAM_NAME> <EC2_INGRESS_IP>
```

-   `AWS_PROFILE`: Your AWS CLI profile name.
-   `YOUR_NAME`: Your name in `first-last` format.
-   `TEAM_NAME`: Your team name.
-   `EC2_INGRESS_IP`: Your public IP address.

#### **2. Upload CSV Files to S3**

Place raw data files into the `NameOfRawDataBucket` created during deployment.

#### **3. Monitor Lambda Function**

Check the Lambda function’s CloudWatch logs for errors or processing status.

#### **4. Query Data in Redshift**

Use a SQL client or Grafana to query tables such as `branches`, `transactions`, `products`, and `product_transactions`.

---

## **File Structure**

```plaintext
.
├── src
│   ├── cafe_etl_lambda.py  # Main Lambda function
│   ├── etl.py                     # Core ETL logic
│   ├── utils
│   │   ├── db_utils.py            # Database utilities
│   │   ├── s3_utils.py            # S3 utilities
│   │   └── sql_utils.py           # SQL utilities
├── deployment-bucket-stack.yml    # CloudFormation template for S3 bucket
├── etl-stack.yml                  # CloudFormation template for ETL pipeline
├── deploy.sh                      # Deployment script
└── README.md                      # Project documentation
└── requirements-lambda.txt
└── requirements.txt

```

---

## **Sample Queries**

### **List All Branches**

```sql
SELECT * FROM branches;
```

### **Total Sales by Payment Method**

```sql
SELECT payment_method, SUM(total_amount) AS total_sales
FROM transactions
GROUP BY payment_method;
```

### **Top-Selling Products**

```sql
SELECT p.name, SUM(pt.quantity) AS total_sold
FROM product_transactions pt
JOIN products p ON pt.product_id = p.product_id
GROUP BY p.name
ORDER BY total_sold DESC;
```

---

## **Future Enhancements**

-   Implement automated data validation and error reporting.
-   Enhance security by encrypting data at rest and in transit.
-   Scale the pipeline to handle additional branches and larger data volumes.

---

## **Acknowledgments**

Special thanks to the AWS team and mentors who guided the implementation of this project.
