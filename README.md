# E-Commerce SQL Analysis Project (20 Queries)

From raw transactional data to meaningful business insights — this project uses MySQL to analyze an e-commerce dataset through 20 structured SQL queries.

---

## Project Overview

This project explores an e-commerce database to answer real-world business questions using SQL. It focuses on customer behavior, sales performance, product analysis, and profitability.

The goal is to demonstrate strong SQL fundamentals and analytical thinking through practical query-based problem solving.

---

## Dataset Structure

The database used in this project contains the following tables:

### customers
- customer_id
- full_name
- country
- city
- gender

### orders
- order_id
- customer_id
- status

### order_items
- order_id
- product_id
- quantity

### payments
- order_id
- amount

### products
- product_id
- product_name
- brand
- unit_price
- cost_price

---

## Objectives

This project aims to:

- Understand customer purchasing behavior
- Identify high-value customers
- Analyze product profitability
- Evaluate order and payment patterns
- Practice advanced SQL querying techniques

---

## Tools Used

- MySQL
- SQL (JOINs, GROUP BY, CASE, Subqueries)
- Data aggregation techniques
- Analytical thinking with relational data

---

## Key SQL Concepts Applied

- SELECT statements
- INNER JOIN across multiple tables
- Aggregation (SUM, AVG, COUNT)
- GROUP BY for business-level insights
- CASE statements for classification
- Subqueries for advanced analysis
- ORDER BY and LIMIT for ranking results
- Data filtering using WHERE and HAVING

---

## Key Business Questions Answered

This project answers 20 real-world analytical questions such as:

- Who are the top-spending customers?
- What is the average order value?
- Which brands generate the most profit?
- Which products are above or below average price?
- How do customers behave across different regions?
- What is the total revenue per customer?
- Which orders generate the highest payments?

---

## Example Insights

From the analysis, we can uncover:

- High-value customers driving most revenue
- Most profitable product brands
- Pricing distribution across products
- Customer segmentation based on spending
- Order-level vs customer-level performance differences

---

## Sample Queries

### 1. Top Customers by Spending
```sql
SELECT 
    c.customer_id,
    c.full_name,
    SUM(p.amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN payments p ON o.order_id = p.order_id
GROUP BY c.customer_id, c.full_name
ORDER BY total_spent DESC;
 ```

### 2. Product Price Classification
```sql
SELECT 
    product_name,
    unit_price,
    CASE 
        WHEN unit_price > (SELECT AVG(unit_price) FROM products)
        THEN 'above average'
        ELSE 'below average'
    END AS price_category
FROM products;
 ```
### 3. Profit by Brand
```sql
SELECT 
    brand,
    SUM(unit_price - cost_price) AS total_profit
FROM products
GROUP BY brand
ORDER BY total_profit DESC;
 ```
## Key Learnings

Through this project, I gained practical experience in:

Writing efficient SQL queries for business analysis
Combining multiple tables using joins
Extracting insights from raw transactional data
Using aggregation to summarize business performance
Applying conditional logic using CASE statements
