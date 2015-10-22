DROP TABLE IF EXISTS carrerer.eixos;
CREATE TABLE carrerer.eixos(
  id serial NOT NULL,
  geom geometry(MultiLineStringZ,25831),
  objectid integer,
  layer character varying(254),
  color integer,
  elevation numeric,
  ilayer integer,
  nom_via character varying(100),
  nom_via2 character varying(100),
  codi_via integer,
  codi_via1 integer,
  CONSTRAINT eixos_pkey PRIMARY KEY (id)
);
CREATE INDEX sidx_eixos_geom ON carrerer.eixos USING gist(geom);


DROP TABLE IF EXISTS carrerer.portals;
CREATE TABLE carrerer.portals(
  id serial NOT NULL,
  geom geometry(MultiPoint,25831),
  fontname character varying(254),
  fontsize numeric,
  bold integer,
  italic integer,
  underline integer,
  verticalal integer,
  horizontal integer,
  angle numeric,
  layer character varying(254),
  color integer,
  elevation numeric,
  style character varying(254),
  text character varying(254),
  height numeric,
  txtangle numeric,
  vertalign character varying(32),
  ilayer integer,
  refcat character varying(14),
  num_portal integer,
  num_duplic character varying(10),
  codi_via integer,
  CONSTRAINT portals_pkey PRIMARY KEY (id)
);
CREATE INDEX sidx_portals_geom ON carrerer.portals USING gist(geom);


DROP TABLE IF EXISTS carto.municipis_catalunya;
CREATE TABLE carto.municipis_catalunya(
  id serial NOT NULL,
  geom geometry(MultiPolygon,25831),
  id_muni numeric(6,2),
  codi_ine character varying(5),
  codi_muni character varying(6),
  codi_ens character varying(254),
  nom_muni character varying(45),
  cap_com character varying(254),
  codi_com character varying(2),
  nom_com character varying(254),
  codi_prov character varying(2),
  icodi_prov character varying(254),
  nom_prov character varying(254),
  sup_muni numeric(9,5),
  cif character varying(254),
  habitants numeric(14,6),
  altitud numeric(11,6),
  CONSTRAINT municipis_catalunya_pkey PRIMARY KEY (id)
);
CREATE INDEX municipis_catalunya_geom_idx ON carto.municipis_catalunya USING gist(geom);

  
DROP TABLE IF EXISTS carto.ur_masa;
CREATE TABLE carto.ur_masa(
  id serial NOT NULL,
  geom geometry(MultiPolygon,25831),
  pcat1 character varying(7),
  pcat2 character varying(7),
  mapa integer,
  delegacio integer,
  municipio integer,
  masa character varying(5),
  hoja character varying(7),
  tipo character varying(1),
  coorx double precision,
  coory double precision,
  numsymbol integer,
  area integer,
  fechaalta integer,
  fechabaja integer,
  ninterno numeric,
  CONSTRAINT ur_masa_pkey PRIMARY KEY (id)
);
CREATE INDEX sidx_ur_masa_geom ON carto.ur_masa USING gist(geom);


DROP TABLE IF EXISTS carto.ur_parcela;
CREATE TABLE carto.ur_parcela(
  id serial NOT NULL,
  geom geometry,
  pcat1 character varying(7),
  pcat2 character varying(7),
  coory double precision,
  via integer,
  numero integer,
  numerodup character varying(1),
  numsymbol integer,
  area integer,
  fechaalta integer,
  fechabaja integer,
  ninterno numeric,
  mapa integer,
  delegacio integer,
  municipio integer,
  masa character varying(5),
  hoja character varying(7),
  tipo character varying(1),
  parcela character varying(5),
  coorx double precision,
  refcat character varying(14),
  CONSTRAINT ur_parcela_pkey PRIMARY KEY (id)
);
CREATE INDEX sidx_ur_parcela_geom ON carto.ur_parcela USING gist(geom);


DROP TABLE IF EXISTS topo.plani_line;
CREATE TABLE topo.plani_line(
  id serial NOT NULL,
  geom geometry(MultiLineStringZ,25831),
  color integer,
  elevation numeric,
  shape_leng numeric,
  ilayer integer,
  desc_layer character varying(100),
  CONSTRAINT plani_line_pkey PRIMARY KEY (id)
);
CREATE INDEX sidx_plani_line_geom ON topo.plani_line USING gist(geom);



