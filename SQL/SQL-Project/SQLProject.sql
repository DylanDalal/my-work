create database cop4710t25db;

use cop4710t25db; 

CREATE TABLE Property (address VARCHAR(50), ownerName VARCHAR(30), price INTEGER, PRIMARY KEY(address));

CREATE TABLE BusinessProperty(type CHAR(20), size INTEGER, address VARCHAR(50) REFERENCES Property, ownerName VARCHAR(30) REFERENCES Property, price INTEGER REFERENCES Property, FOREIGN KEY(address) REFERENCES Property(address));

CREATE TABLE House ( bedrooms INTEGER, bathrooms INTEGER, size INTEGER, address VARCHAR(50) REFERENCES Property, ownerName VARCHAR(30) REFERENCES Property, price INTEGER REFERENCES Property, FOREIGN KEY(address) REFERENCES Property(address));

CREATE TABLE Agent(agentId INTEGER, name VARCHAR(30), phone CHAR(12), firmId INTEGER, dateStarted DATE, PRIMARY KEY(agentId));

CREATE TABLE Firm (id INTEGER, name VARCHAR(30), address VARCHAR(50), PRIMARY KEY(id));

CREATE TABLE Buyer(id INTEGER, name VARCHAR(30), phone CHAR(12), propertyType CHAR(20), bedrooms INTEGER, bathrooms INTEGER, businessPropertyType CHAR(20), minimumPreferredPrice INTEGER, maximumPreferredPrice INTEGER, PRIMARY KEY(id));

CREATE TABLE Listings(address VARCHAR(50), agentId INTEGER, mlsNumber INTEGER, dateListed DATE, PRIMARY KEY(mlsNumber));

CREATE TABLE Works_With( buyerID INT, agentID INT, FOREIGN KEY (buyerId) REFERENCES Buyer (id),
FOREIGN KEY (agentId) REFERENCES Agent (agentId) );

//Insert data to tables

INSERT INTO Property (address,ownerName,price) 
VALUES 
('16 WalMart Rd','Sam Walton',567000000), 
('17 Kmart Dr','Sebastian Kresge',680395), 
('19 SteinMart Way','Sam Stein',654321), 
('20 Bealls Circle','Bob Beall',78000000), 
('444 Ross Blvd','Stuart Maldow',678999),
('123 Circle St','Jimmy Dean', 500000), 
('56 West Dr','Daniel Shadrick',10000000), 
('78 Mountain Ln','Louis Erwin',68995), 
('12 Bisbee Dr','Rosemary Haynes', 324699), 
('789 ShellIsland Way','Bubba Jebco', 3245999);

INSERT INTO House (bedrooms,bathrooms,size,address) 
VALUES 
(4,3,110000,'123 Circle St'), 
(5,2,150000,'56 West Dr'), 
(2,2,35000,'78 Mountain Ln'), 
(3,2,45000,'12 Bisbee Dr'), 
(4,4,780000,'789 ShellIsland Way');

INSERT INTO BusinessProperty(type,size,address) 
VALUES 
('Retail',1500000,'16 WalMart Rd'), 
('Retail',1200000,'17 Kmart Dr'), 
('Office Space',425000,'19 SteinMart Way'), 
('Retail',1600000,'20 Bealls Circle'), 
('Retail',1400000,'444 Ross Blvd');

INSERT INTO Firm (id,name,address) 
VALUES 
(1,'Skeeters','1600 Allen Rd'), 
(2,'Petes Real Estate','432 Call St'), 
(3,'Jimmys Commercial Property','222 College Ave'), 
(4,'Blue Realty','70 Feli Way'), 
(5,'Sweets' Suites','555 Park Ave');

INSERT INTO Agent (agentId,name,phone,firmId,dateStarted) 
VALUES 
(000,'Skeeter Jr','555-555-5555',1,'2001-09-11'), 
(001,'Bob Barker','850-588-7625',2,'1972-12-23'), 
(002,'Bill Nice','567-555-5555',3,'2015-11-11'), 
(003,'Jim Fallon','727-988-4242',4,'2003-12-14'), 
(004,'Famish Howard','800-867-5309',5,'1989-02-09');

INSERT INTO Listings (address,agentId,mlsNumber,dateListed) 
VALUES 
('123 Circle St',000,22001,'2020-05-05'), 
('56 West Dr',001,21901,'2019-04-19'), 
('78 Mountain Ln',002,22101,'2021-03-03'), 
('12 Bisbee Dr',001,22002,'2020-12-12'), 
('789 ShellIsland Way',004,22003,'2020-09-07'), 
('16 WalMart Rd',002,21501,'2015-07-04'), 
('17 Kmart Dr',002,21502,'2015-09-01'), 
('19 SteinMart Way',003,21101,'2011-11-11'), 
('20 Bealls Circle',003,22103,'2021-11-30'), 
('444 Ross Blvd',002,21201,'2012-04-20');

INSERT INTO Buyer (id,name,phone,propertyType,bedrooms,bathrooms,businessPropertyType,minimumPreferredPrice,maximumPreferredPrice) 
VALUES 
(1000,'Andrew Jackson','727-892-0907','House',2,1,'NONE',10000,100000), 
(1001,'Charlie Sheen','229-883-3083','BusinessProperty',3,4,'Corporation',50000,3000000), 
(1002,'Dwayne Wade','223-712-4298','House',4,2,'NONE',25000,1000000), 
(1003,'Howard Duck','912-798-0456','BusinessProperty',3,3,'Corporation',30000,6000000000), 
(1004,'Bucky Roberts','233-989-4211','House',3,2,'NONE',25000,4150000);

INSERT INTO Works_With (buyerId,agentId) 
VALUES 
(1000,000), 
(1001,002), 
(1001,003), 
(1002,004), 
(1003,002), 
(1004,003), 
(1003,001), 
(1003,004);