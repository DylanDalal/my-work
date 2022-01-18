# MySQLProjectcop4710

CREATE TABLE Property (address VARCHAR(50), ownerName VARCHAR(30), price INTEGER, PRIMARY KEY(address));

CREATE TABLE BusinessProperty(type CHAR(20), size INTEGER, address VARCHAR(50) REFERENCES Property, ownerName VARCHAR(30) REFERENCES Property, price INTEGER REFERENCES Property, FOREIGN KEY(address) REFERENCES Property(address));

CREATE TABLE House ( bedrooms INTEGER, bathrooms INTEGER, size INTEGER, address VARCHAR(50) REFERENCES Property, ownerName VARCHAR(30) REFERENCES Property, price INTEGER REFERENCES Property, FOREIGN KEY(address) REFERENCES Property(address));

CREATE TABLE Agent(agentId INTEGER, name VARCHAR(30), phone CHAR(12), firmId INTEGER, dateStarted DATE, PRIMARY KEY(agentId));

CREATE TABLE  Firm (id INTEGER, name VARCHAR(30), address VARCHAR(50), PRIMARY KEY(id));

CREATE TABLE Buyer(id INTEGER, name VARCHAR(30), phone CHAR(12), propertyType CHAR(20), bedrooms INTEGER, bathrooms INTEGER, businessPropertyType CHAR(20), minimumPreferredPrice INTEGER, maximumPreferredPrice INTEGER, PRIMARY KEY(id));

CREATE TABLE Listings(address VARCHAR(50), agentId INTEGER, mlsNumber INTEGER, dateListed DATE, PRIMARY KEY(mlsNumber));

CREATE TABLE Works_With( buyerID INT REFERENCES Buyer(id),  agentID INT REFERENCES Agent(agentId) );

//Insert data to tables

INSERT INTO Property (address,ownerName,price)
VALUES ('16 WalMart Rd','Sam Walton',567000000),
        ('17 Kmart Dr','Sebastian Kresge',680395),
        ('19 SteinMart Way','Sam Stein',654321),
        ('20 Bealls Circle','Bob Beall',78000000),
        ('444 Ross Blvd','Stuart Maldow',678999)
	('123 Circle St','Jimmy Dean', 500000),
	('56 West Dr','Daniel Shadrick',10000000),
	('78 Mountain Ln','Louis Erwin',68995),
	('12 Bisbee Dr','Rosemary Haynes', 324699),
	('789 ShellIsland Way','Bubba Jebco', 3245999),
	('345 Elbow St','William Holland', 200000);

INSERT INTO House (bedrooms,bathrooms,size,address)
VALUES (4,3,110000,'123 Circle St'),
        (5,2,150000,'56 West Dr'),
        (2,2,35000,'78 Mountain Ln'),
        (3,2,45000,'12 Bisbee Dr'),
        (4,4,780000,'789 ShellIsland Way')
	(3,2, 47000,'345 Elbow St');

INSERT INTO BusinessProperty(type,size,address)
VALUES ('Retail',1500000,'16 WalMart Rd'),
        ('Retail',1200000,'17 Kmart Dr'),
        ('Office Space',425000,'19 SteinMart Way'),
        ('Retail',1600000,'20 Bealls Circle'),
        ('Retail',1400000,'444 Ross Blvd');

INSERT INTO Firm (id,name,address)
VALUES (1,'Skeeters','1600 Allen Rd'),
        (2,'Petes Real Estate','432 Call St'),
        (3,'Jimmys Commercial Property','222 College Ave'),
        (4,'Blue Realty','70 Feli Way'),
        (5,'Sweets' Suites','555 Park Ave');

INSERT INTO Agent (agentId,name,phone,firmId,dateStarted)
VALUES (000,'Skeeter Jr','555-555-5555',1,'2001-09-11'),
        (001,'Bob Barker','850-588-7625',2,'1972-12-23'),
        (002,'Bill Nice','567-555-5555',3,'2015-11-11'),
        (003,'Jim Fallon','727-988-4242',4,'2003-12-14'),
        (004,'Famish Howard','800-867-5309',5,'1989-02-09');

INSERT INTO Listings (address,agentId,mlsNumber,dateListed)
VALUES ('123 Circle St',000,22001,'2020-05-05'),
        ('56 West Dr',001,21901,'2019-04-19'),
        ('78 Mountain Ln',002,22101,'2021-03-03'),
        ('12 Bisbee Dr',001,22002,'2020-12-12'),
        ('789 ShellIsland Way',004,22003,'2020-09-07'),
	('345 Elbow St', 004, 22104,'2021-12-02'),
        ('16 WalMart Rd',002,21501,'2015-07-04'),
        ('17 Kmart Dr',002,21502,'2015-09-01'),
        ('19 SteinMart Way',003,21101,'2011-11-11'),
        ('20 Bealls Circle',003,22103,'2021-11-30'),
        ('444 Ross Blvd',002,21201,'2012-04-20');

INSERT INTO Buyer (id,name,phone,propertyType,bedrooms,bathrooms,businessPropertyType,minimumPreferredPrice,maximumPreferredPrice)
VALUES (1000,'Andrew Jackson','727-892-0907','House',2,1,'NONE',10000,100000),
        (1001,'Charlie Sheen','229-883-3083','BusinessProperty',3,4,'Corporation',50000,3000000),
        (1002,'Dwayne Wade','223-712-4298','House',4,2,'NONE',25000,1000000),
        (1003,'Howard Duck','912-798-0456','BusinessProperty',3,3,'Corporation',30000,6000000000),
        (1004,'Bucky Roberts','233-989-4211','House',3,2,'NONE',25000,4150000);

INSERT INTO Works_With (buyerId,agentId)
VALUES (1000,000),
        (1001,002),
        (1001,003),
        (1002,004),
        (1003,002),
        (1004,003),
        (1003,001),
        (1003,004);



The queries are: 
 
1) Find the addresses of all houses currently listed. 

SELECT Listings.address
FROM Listings, House
WHERE Listings.address = House.address;

2) Find the addresses and MLS numbers of all houses currently listed. 

SELECT Listings.address, Listings.mlsNumber
FROM Listings, House
WHERE Listings.address = House.address;


3) Find the addresses of all 3-bedroom, 2-bathroom houses currently listed. 

SELECT Listings.address
FROM Listings, House
WHERE Listings.address = House.address AND House.bathrooms = 2 AND House.bedrooms = 3;

4) Find  the  addresses  and  prices  of  all  3-bedroom,  2-bathroom  houses  with  prices  in  the  range 
$100,000 to $250,000, with the results shown in descending order of price. 

SELECT P.address, P.price FROM Property P INNER JOIN House H ON P.address = H.address WHERE H.bedrooms = 3 AND H.bathrooms = 2 AND P.price >= 100000 AND P.price <= 250000 ORDER BY price DESC;

5) Find  the  addresses  and  prices  of  all  business  properties  that  are  advertised  as  office  space  in 
descending order of price. 

SELECT P.address, P.price FROM Property P INNER JOIN BusinessProperty BP ON P.address = BP.address WHERE BP.type LIKE '%office space%' ORDER BY P.price DESC;


6) Find  all  the  ids,  names  and  phones  of all  agents,  together  with the  names  of  their  firms  and  the 
dates when they started. 

SELECT agentId, a.name as "AgentName", phone, f.name as "FirmName", dateStarted
FROM Agent a, Firm f
WHERE a.firmId = f.id;

7) Find all the properties currently listed by agent with id “001” (or some other suitable id). 

SELECT P.* FROM Property P INNER JOIN Listings L ON P.address = L.address WHERE L.agentId = 001;

8) Find all Agent.name-Buyer.name pairs where the buyer works with the agent, sorted 
alphabetically by Agent.name.  

SELECT a.name, b.name
FROM Works_With w, Agent a, Buyer b
WHERE w.agentId = a.agentId
AND w.buyerId = b.id
ORDER BY a.name;


9) For each agent, find the total number of buyers currently working with that agent, i.e., the output should be Agent.id-count pairs.  

SELECT agentID, COUNT(buyerID)
FROM Works_With
GROUP BY agentID;

10) For some buyer that is interested in a house, where the buyer is identified by an id (e.g., “001”), find  all  houses  that meet the buyer’s preferences, with the results shown  in  descending  order  of price. 

SELECT P.address,P.ownerName,P.price,H.bedrooms,H.bathrooms,H.size FROM House H INNER JOIN Property P ON H.address = P.address INNER JOIN Buyer B ON P.price >= B.minimumPreferredPrice AND P.price <= B.maximumPreferredPrice AND B.bathrooms = H.bathrooms AND B.bedrooms = H.bedrooms WHERE B.id = 1004 AND B.propertyType = "House" ORDER BY P.price DESC;


