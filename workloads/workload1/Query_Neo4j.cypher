

//IS1 
MATCH (p1:Person)-[e:IS_LOCATED_IN]->(p2:Place)
WHERE  p1.id=7375
RETURN p1.firstName,  p1.lastName, p1.birthday,p1.locationIP, p1.browserUsed ,p2.name



#IS2
// recent messages (Post or Comment) created by a given Person 1129
MATCH (p:Person {id: 1129})<-[:HAS_CREATOR]-(m)
WHERE m:Post OR m:Comment
WITH m, p
ORDER BY m.creationDate DESC
LIMIT 10

// for each message, find the original Post and its author
OPTIONAL MATCH (m)-[:REPLY_OF*0..]->(origPost:Post)-[:HAS_CREATOR]->(origPoster:Person)
WITH 
  m AS message,
  coalesce(origPost, m) AS post,    // if m is a Post càd m doesnt have a REPLY_OF et donc  origPost is NULL so coalesce returns the first arg non-NULL which is m
  coalesce(origPoster, p) AS origPoster // same here
RETURN 
  message.id AS messageId,
  message.creationDate AS messageDate,
  post.id AS postId,
  origPoster.id AS originalPosterId
ORDER BY messageDate DESC
LIMIT 10;


//IS3 
MATCH (p:Person {id: 94})-[r:KNOWS]->(friend:Person)
RETURN friend.id AS friendId, r.creationDate AS since


// IS4 
MATCH (m:Post|Comment)
WHERE m.id = 618475290625
RETURN m.content AS content, m.creationDate AS creationDate

//IS5 
MATCH (m:Post|Comment)-[:HAS_CREATOR]->(a:Person)
WHERE  m.id = 618475290625
RETURN a.id AS authorId

//IS6 
MATCH (m)
WHERE m.id = 1236950581250

OPTIONAL MATCH (m:Post)<-[:CONTAINER_OF]-(f:Forum)-[:HAS_MODERATOR]->(mod:Person)
OPTIONAL MATCH (m:Comment)-[:REPLY_OF]->(p:Post)<-[:CONTAINER_OF]-(f2:Forum)-[:HAS_MODERATOR]->(mod2:Person)

RETURN 
    coalesce(f, f2) AS forum,
    coalesce(mod, mod2) AS moderator


//IS7 

MATCH (origMsg)
WHERE origMsg.id = 2061584302089

MATCH (reply:Comment)-[:REPLY_OF]->(origMsg)


MATCH (replyAuthor:Person)<-[:HAS_CREATOR]-(reply)
MATCH (origAuthor:Person)<-[:HAS_CREATOR]-(origMsg)


OPTIONAL MATCH (replyAuthor)-[:KNOWS]-(origAuthor)

WITH reply, replyAuthor, origAuthor,
     CASE
         WHEN replyAuthor = origAuthor THEN false
         WHEN (replyAuthor)-[:KNOWS]-(origAuthor) THEN true
         ELSE false
     END AS knows

RETURN reply.id AS reply_id,
       replyAuthor.id AS replyAuthorId,
       origAuthor.id AS messageAuthorId,
       knows

//IC1 

// Parameters 
WITH 2199023256684 AS personId, "Boy" AS firstName

// k-length variable path
MATCH (start:Person {id: personId})
MATCH path = (start)-[:KNOWS*1..3]->(other:Person)
WHERE start <> other AND other.firstName = firstName

// Distance = length of the path
WITH DISTINCT other, length(path) AS dist

// Person info
OPTIONAL MATCH (other)-[:IS_LOCATED_IN]->(city:Place)
WITH other, dist, city

// Workplaces
OPTIONAL MATCH (other)-[:WORK_AT]->(company)-[:IS_LOCATED_IN]->(companyPlace:Place)
WITH other, dist, city,
     collect(DISTINCT companyPlace.name) AS companies

// Study places
OPTIONAL MATCH (other)-[:STUDY_AT]->(school)-[:IS_LOCATED_IN]->(schoolPlace:Place)
WITH other, dist, city, companies,
     collect(DISTINCT schoolPlace.name) AS universities

RETURN
    other.id AS person_id,
    dist,
    other.lastName AS ln,
    other.birthday AS br,
    other.creationDate AS cr,
    other.gender AS gr,
    other.browserUsed AS brw,
    other.locationIP AS ip,
    other.email AS em,
    other.speaks AS sp,
    city.name AS city_name,
    companies,
    universities

//IC3 
//query to find  Parameters

MATCH (op:Person)-[:IS_LOCATED_IN]->(homeCity:Place)-[:IS_PART_OF*0..]->(homeCountry:Place)
WHERE homeCountry.type = 'country'
WITH op, homeCountry

//main query
// messages created by op (Post ou Comment)
MATCH (op)<-[:HAS_CREATOR]-(m)
WHERE m:Post OR m:Comment

// country of the message
MATCH (m)-[:IS_LOCATED_IN]->(msgCity:Place)-[:IS_PART_OF*0..]->(msgCountry:Place)
WHERE msgCountry.type = 'country'
  AND msgCountry <> homeCountry 
  AND msgCountry.name <> "Israel"        

WITH op, homeCountry, msgCountry.name AS countryName,
     count(m) AS msgCount, min(m.creationDate) AS minDate, max(m.creationDate) AS maxDate
ORDER BY msgCount DESC

// collec countries , we keep two
WITH op, homeCountry, collect({country: countryName, cnt: msgCount, minD: minDate, maxD: maxDate}) AS byCountry
WHERE size(byCountry) >= 2

WITH op, homeCountry, byCountry[0] AS c1, byCountry[1] AS c2

// trouver un ami ou ami-d’ami
MATCH (p1:Person)-[:KNOWS*1..2]-(op)
WHERE p1 <> op

RETURN
  p1.id                       AS personId,
  op.id                       AS otherPersonId,
  op.firstName                AS firstName,
  op.lastName                 AS lastName,
  homeCountry.name            AS homeCountry,
  c1.country                  AS countryX,
  c2.country                  AS countryY,
  c1.minD                     AS minDateX,
  c1.maxD                     AS maxDateX,
  c2.minD                     AS minDateY,
  c2.maxD                     AS maxDateY
  

LIMIT 20;

#requete IC3
// PARAMETERS
WITH 
 2199023256684 AS personId,
 "Bosnia_and_Herzegovina"	 AS countryX,
 "Northern_Ireland" AS countryY,
 1221035678258 AS startDate,
 2 As DurationDays,
 (1221035678258 + 2*86400000) AS endDate


// Friends & friends-of-friends

MATCH (start:Person {id: personId})
MATCH fof = (start)-[:KNOWS*1..2]->(p:Person)
WHERE p <> start
WITH DISTINCT p, countryX, countryY, startDate, endDate

// Person must NOT live in country X or Y

MATCH (p)-[:IS_LOCATED_IN]->(:Place)-[:IS_PART_OF]->(pcountry:Place)
WHERE pcountry.name <> countryX AND pcountry.name <> countryY
WITH DISTINCT p, countryX, countryY, startDate, endDate


// Messages created in the time interval

OPTIONAL MATCH (p)<-[:HAS_CREATOR]-(m)
WHERE (m:Post OR m:Comment)
  AND m.creationDate >= startDate
  AND m.creationDate < endDate

// Message country
OPTIONAL MATCH (m)-[:IS_LOCATED_IN]->(mcountry:Place)
WITH p, countryX, countryY,
     collect(mcountry.name) AS msgCountries

// Count messages in X and Y

WITH 
   p,
   countryX,
   countryY,
   size([x IN msgCountries WHERE x = countryX]) AS xCount,
   size([y IN msgCountries WHERE y = countryY]) AS yCount
WHERE xCount > 0 AND yCount > 0


// Person info

RETURN 
    p.id AS personId,
    p.firstName AS firstName,
    p.lastName AS lastName,
    xCount,
    yCount,
    xCount + yCount AS totalCount



//IC13 
MATCH path = shortestPath(
  (p1:Person {id: 933})-[:KNOWS*..]->(p2:Person {id: 32985348834483})
)
RETURN 
  CASE 
    WHEN p1.id= p2.id THEN 0
    WHEN path IS NULL THEN -1
    ELSE length(path)
  END AS pathLength;



//IC14
// query to find two ids of person in 3-length knows path
MATCH (p1:Person)-[:KNOWS*3]->(p2:Person)
RETURN DISTINCT p1.id, p2.id
limit 1;
sf01 933 32985348834483
sf03 933 32985348834886
sf1 3528 8796093026629


//main query

MATCH p = allShortestPaths((p1:Person {id: 933})-[:KNOWS*]->(p2:Person {id: 32985348834483}))
WITH p, nodes(p) AS persons
UNWIND range(0, size(persons)-2) AS i
WITH p, persons[i] AS a, persons[i+1] AS b


OPTIONAL MATCH (a)<-[:HAS_CREATOR]-(reply1:Comment)-[:REPLY_OF]->(msg1:Post)-[:HAS_CREATOR]->(b)
WITH p, a, b, COUNT(DISTINCT reply1) AS repliesToPost
OPTIONAL MATCH (a)<-[:HAS_CREATOR]-(reply2:Comment)-[:REPLY_OF]->(msg2:Comment)-[:HAS_CREATOR]->(b)

WITH p, a, b, repliesToPost, COUNT(DISTINCT reply2) AS repliesToComment

WITH p, a, b, (repliesToPost * 1.0 + repliesToComment * 0.5) AS ab_weight


OPTIONAL MATCH (b)<-[:HAS_CREATOR]-(reply3:Comment)-[:REPLY_OF]->(msg3:Post)-[:HAS_CREATOR]->(a)
WITH p, a, b, ab_weight, COUNT(DISTINCT reply3) AS repliesToPostRev
OPTIONAL MATCH (b)<-[:HAS_CREATOR]-(reply4:Comment)-[:REPLY_OF]->(msg4:Comment)-[:HAS_CREATOR]->(a)
WITH p, a, b, ab_weight, repliesToPostRev, COUNT(DISTINCT reply4) AS repliesToCommentRev


WITH p, (ab_weight + repliesToPostRev*1.0 + repliesToCommentRev*0.5) AS pair_weight


WITH p, SUM(pair_weight) AS total_weight
RETURN p AS path,length(p) AS len, total_weight






