# Cassandra

1、集群特性
2、列式存储，table -> keyspace
3、集合类型
4、自定义数据类型


?尝试集群
?sstable
?commit log
?数据存储方式



Cassandra，卡珊德拉，为希腊、罗马神话中特洛伊的公主，阿波罗的祭司。
因神蛇以舌为她洗耳，获阿波罗的赐予而有了预言能力。
又因抗拒阿波罗，预言不被人相信，成为一名不被人所听信的女先知。
特洛伊战争后被俘虏，并遭杀害。



Cassandra 是一套开源分布式 NoSQL 数据库系统。它最初由 Facebook 开发，2010 年时成为 Apache 顶级项目。


世界由非结构化数据构成


Redis 注重的是快速高效的缓存而非大量数据的存储和查询
MongoDB 无法保证数据有效性和完整性，官方建议不要使用 MongoDB 保存重要的不可丢失的信息
HBase 只负责数据管理，它需要配合 HDFS 和 zookeeper 来搭建集群，主从结构，有单点失效问题的可能; Cassandra 是一个数据存储和数据管理系统， p2p 架构，无单点失效问题。



拓展和复制对很多开发者用户来说，是一个难题。这个问题在过往的企业规模小的时候，不是一个大问题。而在今天，它很迅速地成为大问题。

Cassandra 特点是从一开始设计就解决这个问题。
Cassandra 在集群规模管理方面非常出色。
在机器拓展部署上，表现特别出色。
自带的备份机制，保证各个数据中心的数据安全。
增加集群容量时，你只需启动一台新机器，并告诉 Cassandra 那里的新节点，然后，它完成其他剩下的事情。






# docker
```
docker run --name cass -p 9042:9042 -e CASSANDRA_BROADCAST_ADDRESS=x.x.x.x -d cassandra:3
docker run --name cass2 -d -e CASSANDRA_SEEDS=x.x.x.x cassandra:3

docker run --name cass -p 9042:9042 -v /d/share/cassandra:/var/lib/cassandra -d cassandra:3
```


# conf
/etc/cassandra/cassandra.yaml

重点配置项
```
cluster_name: 'Test Cluster'
seeds: "172.17.0.2"
listen_address: 172.17.0.2
broadcast_address: 172.17.0.2
storage_port: 7000
native_transport_port: 9042

data_file_directories:
    - /var/lib/cassandra/data
commitlog_directory: /var/lib/cassandra/commitlog
saved_caches_directory: /var/lib/cassandra/saved_caches
```

https://cassandra.apache.org/doc/latest/configuration/cassandra_config_file.html



# CQL

标识符大小写不敏感
Abc = abc

加上双引号后大小写敏感
"Abc" != "abc"

"abc" = abc = Abc = aBc

"a""bc" -> a"bc


# 常量
```
constant ::=  string | integer | float | boolean | uuid | blob | NULL
string   ::=  '\'' (any character where ' can appear if doubled)+ '\''
              '$$' (any character other than '$$') '$$'
integer  ::=  re('-?[0-9]+')
float    ::=  re('-?[0-9]+(\.[0-9]*)?([eE][+-]?[0-9+])?') | NAN | INFINITY
boolean  ::=  TRUE | FALSE
uuid     ::=  hex{8}-hex{4}-hex{4}-hex{4}-hex{12}
hex      ::=  re("[0-9a-fA-F]")
blob     ::=  '0' ('x' | 'X') hex+
```

'a''bc' = $$a'bc$$ -> a'bc


# comment
```
-- This is a comment
// This is a comment too
/* This is
   a multi-line comment */
```


# 自定义数据类型
```
CREATE TYPE phone (
    country_code int,
    number text,
)

CREATE TYPE address (
    street text,
    city text,
    zip text,
    phones map<text, phone>
)

CREATE TABLE user (
    name text PRIMARY KEY,
    addresses map<text, address>
)
```

```
INSERT INTO user (name, addresses)
    VALUES ('Tony', {
        'home' : {
            street: '1600 Pennsylvania Ave NW',
            city: 'Washington',
            zip: '20500',
            phones: { 'mobile' : { country_code: 1, number: '202 456-1111' },
                      'landline' : { country_code: 1, number: '202 456-2222' } }
        },
        'work' : {
            city: 'Washington',
            phones: { 'fax' : { country_code: 1, number: '101 123-3333' } }
        }
    })
```


# 创建 keyspace
```
CREATE KEYSPACE excelsior
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};
```


# 创建 column family (table)
```
CREATE TABLE monkeySpecies (
    species text PRIMARY KEY,
    common_name text,
    population varint,
    average_size int
) WITH comment='Important biological records';

CREATE TABLE timeline (
    userid uuid,
    posted_month int,
    posted_time uuid,
    body text,
    posted_by text,
    PRIMARY KEY (userid, posted_month, posted_time)
) WITH compaction = { 'class' : 'LeveledCompactionStrategy' };

CREATE TABLE loads (
    machine inet,
    cpu int,
    mtime timeuuid,
    load float,
    PRIMARY KEY ((machine, cpu), mtime)
) WITH CLUSTERING ORDER BY (mtime DESC);
```



# key
Cassandra中所有的数据都只能根据Primary Key中的字段来排序, 因此, 如果想根据某个column来排序, 必须将该column加到Primary key中

```
CREATE TABLE sample3 (
  id text,
  gmt_create bigint,
  name text,
  score text,
  PRIMARY KEY ((id), gmt_create)
);
```

```
id  | gmt_create | name  | score
-----+------------+-------+--------
id3 |       1925 | name3 | score3
id3 |       1926 | name4 | score4
id1 |       1923 | name1 | score1
id2 |       1924 | name2 | score2
```

```
+-------------+----------------+-------------------+----------------------+
|             |  name = 1925:  |  name=1925:name   |    name=1925:score   |
|             |  value =       |  value=6e616d6533 |  value=73636f726533  |
|             |  timestamp     |     timestamp     |       timestamp      |
|    id 3     +----------------+-------------------+----------------------+
|             |  name = 1926:  |  name=1926:name   |    name=1926:score   |
|             |  value=        |  value=6e616d6534 |  value=73636f726534  |
|             |  timestamp     |     timestamp     |       timestamp      |
+-------------+----------------+-------------------+----------------------+
|             |  name = 1923:  |  name=1923:name   |    name=1923:score   |
|    id 1     |  value =       |  value=6e616d6531 |  value=73636f726531  |
|             |  timestamp     |     timestamp     |       timestamp      |
+-------------+----------------+-------------------+----------------------+
|             |  name = 1924:  |  name=1924:name   |    name=1924:score   |
|    id 2     |  value =       |  value=6e616d6532 |  value=73636f726532  |
|             |  timestamp     |     timestamp     |       timestamp      |
+-------------+----------------+-------------------+----------------------+
```


# CRUD
```
SELECT name, occupation FROM users WHERE userid IN (199, 200, 207);
SELECT JSON name, occupation FROM users WHERE userid = 199;
SELECT COUNT (*) AS user_count FROM users;
SELECT * FROM users WHERE birth_year = 1981 AND country = 'FR' ALLOW FILTERING;


INSERT INTO NerdMovies (movie, director, main_actor, year) VALUES ('Serenity', 'Joss Whedon', 'Nathan Fillion', 2005) USING TTL 86400;
INSERT INTO NerdMovies JSON $${"movie": "Serenity", "director": "Joss Whedon", "year": 2005}$$;


UPDATE NerdMovies USING TTL 400 SET director   = 'Joss Whedon', main_actor = 'Nathan Fillion', year = 2005 WHERE movie = 'Serenity';


DELETE FROM NerdMovies USING TIMESTAMP 1240003134 WHERE movie = 'Serenity';
DELETE phone FROM Users WHERE userid IN (C73DE1D3-AF08-40F3-B124-3FF3E5109F22, B70DE1D0-9908-4AE3-BE34-5573E5B09F14);


BEGIN BATCH
   INSERT INTO users (userid, password, name) VALUES ('user2', 'ch@ngem3b', 'second user');
   UPDATE users SET password = 'ps22dhds' WHERE userid = 'user3';
   INSERT INTO users (userid, password) VALUES ('user4', 'ch@ngem3c');
   DELETE name FROM users WHERE userid = 'user1';
APPLY BATCH;
```



# Secondary Index
```
create index idx_score on sample3(score);
```

当secondary index的column是类似于'国家'这样有许多重复纪录的字段时, 读取时相当高效的(因为n个节点都进行一个磁盘搜素, 时间复杂度O(n), 然而查询到的纪录数有可能是x条, 大多数情况下x>n, 平均下来时非常高效的), 但是当secondary index的column是类似于email这样几乎每个人唯一的字段时, 是非常低效的, 因为按照email进行查询是, 每一次查询几乎只能命中一条纪录, 而secondary index搜索的时间复杂度则是O(n)。


# allow filtering

`ALLOW FILTERING`是一种非常消耗计算机资源的查询方式。
如果您的表包含例如100万行，并且其中95％具有满足查询条件的值，则查询仍然相对有效，您应该使用ALLOW FILTERING。

另一方面，如果您的表包含100万行，并且只有2行包含满足查询条件值，则查询效率极低。Cassandra将无需加载999,998行。如果经常使用查询，则最好在acc_pedal_stroke列上添加索引。

不幸的是，Cassandra无法区分上述两种情况，因为它们取决于表格的数据分布。因此，卡桑德拉会警告你并依靠你做出好的选择。





# Materialized Views 
```
CREATE MATERIALIZED VIEW monkeySpecies_by_population AS
    SELECT * FROM monkeySpecies
    WHERE population IS NOT NULL AND species IS NOT NULL
    PRIMARY KEY (population, species)
    WITH comment='Allow query by population instead of species';
```

```
CREATE TABLE t (
    k int,
    c1 int,
    c2 int,
    v1 int,
    v2 int,
    PRIMARY KEY (k, c1, c2)
)
```

```
// Correct
CREATE MATERIALIZED VIEW mv1 AS
    SELECT * FROM t WHERE k IS NOT NULL AND c1 IS NOT NULL AND c2 IS NOT NULL
    PRIMARY KEY (c1, k, c2)

// Correct
CREATE MATERIALIZED VIEW mv1 AS
    SELECT * FROM t WHERE k IS NOT NULL AND c1 IS NOT NULL AND c2 IS NOT NULL
    PRIMARY KEY (v1, k, c1, c2)


// Error: cannot include both v1 and v2 in the primary key as both are not in the base table primary key
CREATE MATERIALIZED VIEW mv1 AS
    SELECT * FROM t WHERE k IS NOT NULL AND c1 IS NOT NULL AND c2 IS NOT NULL AND v1 IS NOT NULL
    PRIMARY KEY (v1, v2, k, c1, c2)

// Error: must include k in the primary as it's a base table primary key column
CREATE MATERIALIZED VIEW mv1 AS
    SELECT * FROM t WHERE c1 IS NOT NULL AND c2 IS NOT NULL
    PRIMARY KEY (c1, c2)
```


# Security

```
CREATE ROLE bob WITH PASSWORD = 'password_b' AND LOGIN = true AND SUPERUSER = true;
CREATE ROLE alice WITH PASSWORD = 'password_a' AND LOGIN = true AND ACCESS TO DATACENTERS {'DC1', 'DC3'};
CREATE ROLE alice WITH PASSWORD = 'password_a' AND LOGIN = true AND ACCESS TO ALL DATACENTERS;
CREATE ROLE IF NOT EXISTS other_role;

ALTER ROLE bob WITH PASSWORD = 'PASSWORD_B' AND SUPERUSER = false;

GRANT role_a TO role_b;

REVOKE report_writer FROM alice;

LIST ROLES OF alice;

CREATE USER alice WITH PASSWORD 'password_a' SUPERUSER;
CREATE USER bob WITH PASSWORD 'password_b' NOSUPERUSER;

GRANT SELECT ON ALL KEYSPACES TO data_reader;
GRANT MODIFY ON KEYSPACE keyspace1 TO data_writer;
GRANT DROP ON keyspace1.table1 TO schema_owner;
GRANT EXECUTE ON FUNCTION keyspace1.user_function( int ) TO report_writer;
GRANT DESCRIBE ON ALL ROLES TO role_admin;
GRANT ALL PERMISSIONS ON ALL KEYSPACES TO user_name;

REVOKE SELECT ON ALL KEYSPACES FROM data_reader;
```

# aggregates
```
SELECT COUNT (*) FROM plays;
SELECT MIN (players), MAX (players), SUM (players), AVG (players) FROM plays WHERE game = 'quake';
```


# Datetime Arithmetic
```
SELECT * FROM myTable WHERE t = '2017-01-01' - 2d
```

