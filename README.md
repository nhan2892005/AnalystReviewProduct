# Analyst Product's Review

## Project Objective: 
Develop an AI assistant product that summarizes product reviews from previous buyers, enabling potential customers to quickly access the actual quality of products.

## Tech Skills: 
Python, SQL

## Process:
- Data collection
- Analysis, processing, and storage in a data warehouse
- Design ML/DL models for analysis, with training data sourced from the data warehouse

## Task 1: Crawl Data base on Tiki API

This task set up in `CrawlData` folder.

- Step 1: Request data from Tiki API to collect categories

- Step 2: Request data from Tiki API to collect products in each category

- Step 3: Request data from Tiki API to collect reviews of each product

## Task 2: Cleaning data and transform to staging

This task set up in `ExtractData` folder, and staging data is stored in `Records` folder.

- Step 1: Clean data and change it to the right format

- Step 2: Transform data to staging

## Task 3: Load data to Data Warehouse

In this task, I use Docker to set up a PostgreSQL database and load data to the database.

## Deployed:
- [Tiki Assistant](https://tikiassistant.netlify.app)
  
You can access the product review summary by search keyword or product URL.