# Redone FE512 Project
CREATE DATABASE redone512; # The relational database on MySQL server
SHOW DATABASES; # Confirm that the required database has been created
USE redone512; # Switch to the empty database I need to work with
SHOW TABLES;

DROP TABLE IF EXISTS balance_sheet;

# ==========================================================5 stock tables and 1 company information table and 1 balance sheet table========================================================== #
# 5 stock tables first
CREATE TABLE apple(
# Date for each transaction must be unique
date DATE PRIMARY KEY,
open DECIMAL(5,2) UNSIGNED NULL, # Don't use float() datatype when we input exact value
high DECIMAL(5,2) UNSIGNED NULL,
low DECIMAL(5,2) UNSIGNED NULL,
close DECIMAL(5,2) UNSIGNED NULL,
volume INT(11) UNSIGNED NULL
);

CREATE TABLE amazon(
# Date for each transaction must be unique
date DATE PRIMARY KEY,
open DECIMAL(5,2) UNSIGNED NULL, # Don't use float() datatype when we input exact value
high DECIMAL(5,2) UNSIGNED NULL,
low DECIMAL(5,2) UNSIGNED NULL,
close DECIMAL(5,2) UNSIGNED NULL,
volume INT(11) UNSIGNED NULL
);

CREATE TABLE jpmorgan(
# Date for each transaction must be unique
date DATE PRIMARY KEY,
open DECIMAL(5,2) UNSIGNED NULL, # Don't use float() datatype when we input exact value
high DECIMAL(5,2) UNSIGNED NULL,
low DECIMAL(5,2) UNSIGNED NULL,
close DECIMAL(5,2) UNSIGNED NULL,
volume INT(11) UNSIGNED NULL
);

CREATE TABLE facebook(
# Date for each transaction must be unique
date DATE PRIMARY KEY,
open DECIMAL(5,2) UNSIGNED NULL, # Don't use float() datatype when we input exact value
high DECIMAL(5,2) UNSIGNED NULL,
low DECIMAL(5,2) UNSIGNED NULL,
close DECIMAL(5,2) UNSIGNED NULL,
volume INT(11) UNSIGNED NULL
);

CREATE TABLE tesla(
# Date for each transaction must be unique
date DATE PRIMARY KEY,
open DECIMAL(5,2) UNSIGNED NULL, # Don't use float() datatype when we input exact value
high DECIMAL(5,2) UNSIGNED NULL,
low DECIMAL(5,2) UNSIGNED NULL,
close DECIMAL(5,2) UNSIGNED NULL,
volume INT(11) UNSIGNED NULL
);

# ==========================================================Import the data gathered from Bloomberg Terminal to those tables I have just created========================================================== #
LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\career\\Josephine\\Redone Projects\\Database(512)\\apple.txt'
INTO TABLE apple
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;
SELECT * FROM aapl;
SELECT date FROM 
#UPDATE apple
#SET date = '2017-10-31'
#WHERE open = 108.53;

rename TABLE apple TO AAPL;
rename TABLE amazon TO AMZN;
rename TABLE jpmorgan TO JPM;
rename TABLE facebook TO FB;
rename TABLE tesla TO TSLA;

LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\career\\Josephine\\Redone Projects\\Database(512)\\amazon.txt'
INTO TABLE amazon
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;
SELECT * FROM amazon;

UPDATE amazon
SET date = '2017-10-27'
WHERE open = 671.50;

LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\career\\Josephine\\Redone Projects\\Database(512)\\jpmorgan.txt'
INTO TABLE jpmorgan
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;
SELECT * FROM jpmorgan;

UPDATE jpmorgan
SET date = '2017-10-23'
WHERE open = 67.31;

LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\career\\Josephine\\Redone Projects\\Database(512)\\facebook.txt'
INTO TABLE facebook
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;
SELECT * FROM facebook;

UPDATE facebook
SET date = '2017-10-25'
WHERE open = 107.19;

LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\career\\Josephine\\Redone Projects\\Database(512)\\tesla.txt'
INTO TABLE tesla
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;
SELECT * FROM tesla;

UPDATE tesla
SET date = '2017-10-11'
WHERE open = 217.35;

# ==========================================================Then 1 company information table and 1 balance sheet table are created here========================================================== #
CREATE TABLE company_information (
ticker VARCHAR(6) PRIMARY KEY,
company_name VARCHAR(50) NOT NULL,
CIK CHAR(10) NOT NULL, # An identifier for one company, fixed with 10 digits
SIC CHAR(4) NOT NULL # Classifing an industry, fixed with 4 digits
);

CREATE TABLE balance_sheet (
filing_number CHAR(9) NOT NULL,
filing_date DATE NOT NULL,
ticker VARCHAR(6) PRIMARY KEY,
total_assets MEDIUMINT(6) NOT NULL,
total_current_assets MEDIUMINT(6) NOT NULL,
total_other_assets MEDIUMINT(6) NOT NULL,
total_liabilities MEDIUMINT(6) NOT NULL,
long_term_debt MEDIUMINT(6) NOT NULL,
total_shareholder_equity MEDIUMINT(6) NOT NULL,
FOREIGN KEY (ticker) REFERENCES company_information(ticker)
);

# ==========================================================Insert the information in the table just created========================================================== #
INSERT INTO company_information
(ticker, company_name, CIK, SIC)
VALUES
('AAPL', 'Apple INC', '0000320193', '3571'),
('AMZN', 'Amazon COM INC', '0001018724', '5961'),
('JPM', 'JPMorgan CHASE & CO', '0000019617', '6021'),
('FB', 'Facebook Inc', '0001326801', '7370'),
('TSLA', 'Tesla Motors INC', '0001318605', '3711');
select * from company_information;

INSERT INTO balance_sheet
(ticker,filing_number,filing_date,total_assets,total_current_assets,total_other_assets,total_liabilities,long_term_debt,total_shareholder_equity)
VALUES
('AAPL','001-36743','2017-10-31',321686,106869,8283,193437,75427,128249),
('AMZN','000-22513','2017-10-27',65444,36474,3373,33899,8235,13384),
('JPM','001-05805','2017-10-23',2351698,20490,105572,2104125,288651,247573),
('FB','001-35551','2017-10-25',49407,21652,796,5189,3157,44218),
('TSLA','001-34756','2017-10-11',8092460,2791568,74633,2816274,633166,1088944);
select * from balance_sheet;

select * from balance_sheet where ticker = 'aapl';






