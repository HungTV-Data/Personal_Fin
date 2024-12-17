CREATE TABLE Fact_Transactions (
    Transaction_ID SERIAL PRIMARY KEY,
    Source_ID INT REFERENCES Dim_Sources(Source_ID),
    Category_ID INT REFERENCES Dim_Categories(Category_ID),
    Date_ID INT REFERENCES Dim_Dates(Date_ID),
    User_ID INT REFERENCES Dim_Users(User_ID),
    Amount DECIMAL(10,2) NOT NULL,
    Transaction_Type VARCHAR(10) CHECK (Transaction_Type IN ('Income', 'Spent'))
);
