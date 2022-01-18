SELECT agentID, COUNT(buyerID) FROM Works_With GROUP BY agentID;

SELECT Listings.address, Listings.mlsNumber FROM Listings, House WHERE Listings.address = House.address;

SELECT Listings.address FROM Listings, House WHERE Listings.address = House.address AND House.bathrooms = 2 AND House.bedrooms = 3;

SELECT P.address, P.price FROM Property P INNER JOIN House H ON P.address = H.address WHERE H.bedrooms = 3 AND H.bathrooms = 2 AND P.price >= 100000 AND P.price <= 250000 ORDER BY price DESC;

SELECT P.address, P.price FROM Property P INNER JOIN BusinessProperty BP ON P.address = BP.address WHERE BP.type LIKE '%office space%' ORDER BY P.price DESC;

SELECT agentId, a.name as "AgentName", phone, f.name as "FirmName", dateStarted FROM Agent a, Firm f WHERE a.firmId = f.id;

SELECT P.* FROM Property P INNER JOIN Listings L ON P.address = L.address WHERE L.agentId = 001;

SELECT a.name, b.name FROM Works_With w, Agent a, Buyer b WHERE w.agentId = a.agentId AND w.buyerId = b.id ORDER BY a.name;

SELECT agentID, COUNT(buyerID) FROM Works_With GROUP BY agentID;

SELECT P.address,P.ownerName,P.price,H.bedrooms,H.bathrooms,H.size FROM House H INNER JOIN Property P ON H.address = P.address INNER JOIN Buyer B ON P.price >= B.minimumPreferredPrice AND P.price <= B.maximumPreferredPrice AND B.bathrooms = H.bathrooms AND B.bedrooms = H.bedrooms WHERE B.id = 1004 AND B.propertyType = "House" ORDER BY P.price DESC;