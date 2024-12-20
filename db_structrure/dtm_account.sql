CREATE TABLE dim_account (
    Account_ID text PRIMARY KEY,
    Account_Type varchar(4) NOT NULL,
    Expired_date text,
    Bank_ID text
);