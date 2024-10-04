DROP TABLE IF EXISTS daily_performance;

CREATE TABLE daily_performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,       -- Stores the stock ticker symbol
    daily_change FLOAT NOT NULL,       -- Daily percentage change as a float
    week_change FLOAT NOT NULL,        -- Weekly percentage change as a float
    bi_weekly_change FLOAT NOT NULL,   -- Bi-weekly change as a float
    monthly_change FLOAT NOT NULL,     -- Monthly change as a float
    quarterly_change FLOAT NOT NULL,   -- Quarterly change as a float
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- Timestamp when the record is created
);
