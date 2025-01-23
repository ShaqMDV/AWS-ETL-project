-- Create the branches table
CREATE TABLE branches
(
    branch_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL
);

-- Create the transactions table
CREATE TABLE transactions
(
    payment_id SERIAL PRIMARY KEY,
    branch_id INT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

-- Create the products table
CREATE TABLE products
(
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    variant VARCHAR(255),
    size VARCHAR(50),
    price NUMERIC(10, 2) NOT NULL
);

-- Create the product_transactions table
CREATE TABLE product_transactions
(
    product_transactions_id SERIAL PRIMARY KEY,
    payment_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (payment_id) REFERENCES transactions(payment_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
