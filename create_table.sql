CREATE TABLE uscredit (
    id SERIAL PRIMARY KEY,
    SeriousDlqin2yrs int,
    RevolvingUtilizationOfUnsecuredLines float,
    age int,
    NumberOfTime30_59DaysPastDueNotWorse int,
    DebtRatio float,
    MonthlyIncome float,
    NumberOfOpenCreditLinesAndLoans int,
    NumberOfTimes90DaysLate int,
    NumberRealEstateLoansOrLines int,
    NumberOfTime60_89DaysPastDueNotWorse int,
    NumberOfDependents int
);