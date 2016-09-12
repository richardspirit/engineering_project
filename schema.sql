drop table if exists requests;
create table requests (
  reqid integer primary key autoincrement,
  title text not null,
  description text not null,
  client text not null,
  priority integer not null,
  target_date text not null,
  ticket_url text not null,
  product_area text not null
);
