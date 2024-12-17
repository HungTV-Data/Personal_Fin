CREATE TABLE Dim_Categories (
    Category_ID SERIAL PRIMARY KEY,
    Category_Name VARCHAR(100) NOT NULL, -- Example: "Salary", "Rent", "Groceries"
    Category_Type VARCHAR(10) CHECK (Category_Type IN ('Income', 'Spent')),
    Category_Description VARCHAR(255)
);
