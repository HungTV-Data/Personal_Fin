CREATE TABLE Dim_Sources (
    Source_ID SERIAL PRIMARY KEY,
    Source_Name VARCHAR(100) NOT NULL, -- Example: "Chase Bank Account", "My Wallet"
    Source_Type_ID INT REFERENCES Dim_Source_Types(Source_Type_ID)
);
