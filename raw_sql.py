import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@brent31560733",
    database="ecommerce_10k"
)

print("Connection successful!")
def run_query(sql):
    return pd.read_sql(sql, conn)
tables= run_query("""
SHOW tables
""")
tables

#1. Find all customers from Kenya
kenya_customers=run_query("""
SELECT * FROM customers
WHERE country = 'Kenya'
limit 10;                                               
                          """)
kenya_customers

#2. Count total orders
count_total_orders=run_query("""
select COUNT(*) 
as total_orders 
from orders;                             """)
count_total_orders

#3. Find all cancelled orders
cancelled_orders=run_query("""
select * from orders
where status='Cancelled';                           """)
cancelled_orders

#4. Show products costing above $500
product500=run_query("""
select * from products
where price > 500                     
order by price desc
                                       ;""")
product500

#5. Find customers who signed up in 2024
customers_2024=run_query("""
select * from customers
where year(signup_date)=2024;                         """)
customers_2024

#6. Show customer names with their orders
customers_names=run_query("""
SELECT 
    o.order_id,
    c.full_name,
    o.order_date,
    o.status
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id;                          """)
customers_names

#7. Calculate total revenue
total_revenue=run_query("""
select sum(amount) as total_revenue from payments;                        """)
total_revenue

#8. Revenue generated per country
revenue_per_country=run_query("""
SELECT 
    c.country,
    SUM(p.amount) AS revenue
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN payments p
ON o.order_id = p.order_id
GROUP BY c.country
ORDER BY revenue DESC;                            """)
revenue_per_country

#9. Top 10 highest spending customers
top_10_spending=run_query("""
SELECT 
    c.full_name,
    c.country,
    c.gender,
    c.city,
    o.customer_id,
    p.order_id,
    SUM(p.amount) AS total_spent
FROM ecommerce_10k.customers AS c
JOIN ecommerce_10k.orders AS o
ON c.customer_id = o.customer_id
JOIN ecommerce_10k.payments AS p
ON p.order_id = o.order_id
GROUP BY 
    c.full_name,
    c.country,
    c.gender,
    c.city,
    o.customer_id,
    p.order_id
ORDER BY total_spent DESC
LIMIT 10;
                          """)
top_10_spending

#11. Customers who never placed an order
customers_with_no_order=run_query("""
SELECT c.*
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;                                  """)
customers_with_no_order

#12. Orders without payments
unpaid_orders=run_query("""
select o.order_id, o.status,p.amount from ecommerce_10k.orders
as o
join ecommerce_10k.payments as p
on o.order_id=p.order_id
where amount = 0;
                        """)
unpaid_orders

#13. Average order value
average_order_value=run_query("""
select avg(amount) as average_order_value from ecommerce_10k.payments;      """)
average_order_value

#14. Profit generated per product
profit_per_product=run_query("""
SELECT 
    p.brand,
    SUM(p.price) - SUM(p.cost) AS total_profit
FROM ecommerce_10k.products AS p
JOIN ecommerce_10k.order_items AS oi
ON oi.product_id = p.product_id
JOIN ecommerce_10k.payments AS pa
ON pa.order_id = oi.order_id
GROUP BY p.brand;""")
profit_per_product

#15. Customers spending above average
spending_above_average=run_query("""
SELECT 
    t.customer_id,
    t.full_name,
    t.total_spent
FROM (
    SELECT 
        c.customer_id,
        c.full_name,
        SUM(p.amount) AS total_spent
    FROM ecommerce_10k.customers c
    JOIN ecommerce_10k.orders o
    ON c.customer_id = o.customer_id
    JOIN ecommerce_10k.payments p
    ON o.order_id = p.order_id
    GROUP BY c.customer_id, c.full_name
) t
WHERE t.total_spent > (
    SELECT AVG(order_total)
    FROM (
        SELECT SUM(amount) AS order_total
        FROM ecommerce_10k.payments
        GROUP BY order_id
    ) x
);                                 """)
spending_above_average

#16. Find products with above-average prices
above_average_products=run_query("""
SELECT *
FROM products
WHERE price > (
    SELECT AVG(price)
    FROM products
);                                 """)
above_average_products

#17. Rank customers by spending- use windows function
spending_rank=run_query("""
SELECT 
    c.customer_id,
    c.full_name,
    SUM(p.amount) AS total_spent,
    RANK() OVER (ORDER BY SUM(p.amount) DESC) AS spending_rank
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN payments p
ON o.order_id = p.order_id
GROUP BY c.customer_id, c.full_name;                        """)
spending_rank

#18. Running total of revenue over time
total_revenue_over_time=run_query("""
SELECT 
    payment_date,
    amount,
    SUM(amount) OVER (
        ORDER BY payment_date
    ) AS running_revenue
FROM payments;                                """)
total_revenue_over_time

#19. Previous order date per customer
previous_order_date=run_query("""
SELECT 
    customer_id,
    order_date,
    LAG(order_date) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS previous_order_date
FROM orders;                             """)
previous_order_date

#20. Monthly revenue trend + growth rate
monthly_revenue=run_query("""
SELECT 
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS previous_month_revenue,
    ROUND(
        (
            revenue - LAG(revenue) OVER (ORDER BY month)
        )
        /
        LAG(revenue) OVER (ORDER BY month) * 100,
        2
    ) AS growth_rate_percentage
FROM (
    SELECT 
        DATE_FORMAT(payment_date, '%Y-%m') AS month,
        SUM(amount) AS revenue
    FROM payments
    GROUP BY month
) t;                          """)
monthly_revenue
