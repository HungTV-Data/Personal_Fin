CREATE TABLE Dim_Source_Types (
    Source_Type_ID SERIAL PRIMARY KEY,
    Source_Type_Name text NOT NULL -- Example: "Bank Account", "Cash Wallet"
);