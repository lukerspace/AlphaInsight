CREATE TABLE IF NOT EXISTS coppock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    ticker VARCHAR(100)  NOT NULL,
    value FLOAT NOT NULL,
    category VARCHAR(100) NOT NULL,
    sysdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLK', 18.54, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLY', -10.34, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLI', -4.75, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLP', 12.34, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLF', -15.67, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLE', -22.15, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLU', 9.56, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLRE', -5.45, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLC', 14.32, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLV', -8.76, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'XLB', 3.89, 'coppock_value');
INSERT INTO coppock (date, ticker, value, category) VALUES ('2024-10-31', 'SPY', 22.10, 'coppock_value');




 DELETE FROM coppock WHERE date > '2024-10-04';