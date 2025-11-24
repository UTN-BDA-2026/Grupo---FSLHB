--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Clubes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Clubes" (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    razon_social character varying(150),
    contacto character varying(100),
    email character varying(100),
    cancha_local character varying(100),
    domicilio character varying(150),
    telefono character varying(50),
    web character varying(150),
    arbitro_id integer
);


ALTER TABLE public."Clubes" OWNER TO postgres;

--
-- Name: Clubes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Clubes_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Clubes_id_seq" OWNER TO postgres;

--
-- Name: Clubes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Clubes_id_seq" OWNED BY public."Clubes".id;


--
-- Name: Equipos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Equipos" (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    categoria character varying(50),
    club_id integer NOT NULL
);


ALTER TABLE public."Equipos" OWNER TO postgres;

--
-- Name: Equipos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Equipos_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Equipos_id_seq" OWNER TO postgres;

--
-- Name: Equipos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Equipos_id_seq" OWNED BY public."Equipos".id;


--
-- Name: Incidencias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Incidencias" (
    id integer NOT NULL,
    partido_id integer NOT NULL,
    club_id integer NOT NULL,
    jugadora_id integer NOT NULL,
    tipo character varying(20) NOT NULL,
    color character varying(20),
    minuto integer,
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT "Incidencias_tipo_check" CHECK (((tipo)::text = ANY ((ARRAY['gol'::character varying, 'tarjeta'::character varying])::text[]))),
    CONSTRAINT incidencias_tipo_check CHECK (((tipo)::text = ANY ((ARRAY['gol'::character varying, 'tarjeta'::character varying, 'lesion'::character varying])::text[])))
);


ALTER TABLE public."Incidencias" OWNER TO postgres;

--
-- Name: Incidencias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Incidencias_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Incidencias_id_seq" OWNER TO postgres;

--
-- Name: Incidencias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Incidencias_id_seq" OWNED BY public."Incidencias".id;


--
-- Name: Jugadoras; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Jugadoras" (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    dni character varying(20),
    fecha_nacimiento character varying(20),
    categoria character varying(50),
    club_id integer DEFAULT 1 NOT NULL
);


ALTER TABLE public."Jugadoras" OWNER TO postgres;

--
-- Name: Jugadoras_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Jugadoras_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Jugadoras_id_seq" OWNER TO postgres;

--
-- Name: Jugadoras_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Jugadoras_id_seq" OWNED BY public."Jugadoras".id;


--
-- Name: NotasPartido; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."NotasPartido" (
    id integer NOT NULL,
    partido_id integer NOT NULL,
    detalle text
);


ALTER TABLE public."NotasPartido" OWNER TO postgres;

--
-- Name: NotasPartido_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."NotasPartido_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."NotasPartido_id_seq" OWNER TO postgres;

--
-- Name: NotasPartido_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."NotasPartido_id_seq" OWNED BY public."NotasPartido".id;


--
-- Name: Partidos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Partidos" (
    id integer NOT NULL,
    torneo character varying(100) NOT NULL,
    categoria character varying(50) NOT NULL,
    fecha_numero integer,
    bloque character varying(5),
    fecha_hora timestamp without time zone,
    cancha character varying(100),
    club_local_id integer NOT NULL,
    club_visitante_id integer NOT NULL,
    estado character varying(20) DEFAULT 'programado'::character varying NOT NULL,
    goles_local integer,
    goles_visitante integer,
    equipo_local_id integer,
    equipo_visitante_id integer
);


ALTER TABLE public."Partidos" OWNER TO postgres;

--
-- Name: Partidos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Partidos_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Partidos_id_seq" OWNER TO postgres;

--
-- Name: Partidos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Partidos_id_seq" OWNED BY public."Partidos".id;


--
-- Name: PrecargaJugadoras; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PrecargaJugadoras" (
    id integer NOT NULL,
    partido_id integer NOT NULL,
    club_id integer NOT NULL,
    jugadora_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public."PrecargaJugadoras" OWNER TO postgres;

--
-- Name: PrecargaJugadoras_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."PrecargaJugadoras_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."PrecargaJugadoras_id_seq" OWNER TO postgres;

--
-- Name: PrecargaJugadoras_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."PrecargaJugadoras_id_seq" OWNED BY public."PrecargaJugadoras".id;


--
-- Name: Resultados; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Resultados" (
    id integer NOT NULL,
    club_local character varying(100) NOT NULL,
    club_visitante character varying(100) NOT NULL,
    goles_local integer NOT NULL,
    goles_visitante integer NOT NULL,
    fecha date NOT NULL
);


ALTER TABLE public."Resultados" OWNER TO postgres;

--
-- Name: Resultados_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Resultados_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Resultados_id_seq" OWNER TO postgres;

--
-- Name: Resultados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Resultados_id_seq" OWNED BY public."Resultados".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: arbitro_partido; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.arbitro_partido (
    id integer NOT NULL,
    partido_id integer NOT NULL,
    arbitro_id integer NOT NULL,
    rol character varying(32)
);


ALTER TABLE public.arbitro_partido OWNER TO postgres;

--
-- Name: arbitro_partido_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.arbitro_partido_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.arbitro_partido_id_seq OWNER TO postgres;

--
-- Name: arbitro_partido_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.arbitro_partido_id_seq OWNED BY public.arbitro_partido.id;


--
-- Name: arbitros; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.arbitros (
    id integer NOT NULL,
    nombre character varying(80) NOT NULL,
    apellido character varying(80) NOT NULL,
    dni character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.arbitros OWNER TO postgres;

--
-- Name: arbitros_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.arbitros_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.arbitros_id_seq OWNER TO postgres;

--
-- Name: arbitros_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.arbitros_id_seq OWNED BY public.arbitros.id;


--
-- Name: cuerpo_tecnico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cuerpo_tecnico (
    id integer NOT NULL,
    club_id integer NOT NULL,
    nombre character varying(80) NOT NULL,
    apellido character varying(80) NOT NULL,
    dni character varying(20) NOT NULL,
    rol character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.cuerpo_tecnico OWNER TO postgres;

--
-- Name: cuerpo_tecnico_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cuerpo_tecnico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cuerpo_tecnico_id_seq OWNER TO postgres;

--
-- Name: cuerpo_tecnico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cuerpo_tecnico_id_seq OWNED BY public.cuerpo_tecnico.id;


--
-- Name: cuerpo_tecnico_partido; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cuerpo_tecnico_partido (
    id integer NOT NULL,
    partido_id integer NOT NULL,
    club_id integer NOT NULL,
    cuerpo_tecnico_id integer NOT NULL,
    rol character varying(32) NOT NULL
);


ALTER TABLE public.cuerpo_tecnico_partido OWNER TO postgres;

--
-- Name: cuerpo_tecnico_partido_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cuerpo_tecnico_partido_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cuerpo_tecnico_partido_id_seq OWNER TO postgres;

--
-- Name: cuerpo_tecnico_partido_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cuerpo_tecnico_partido_id_seq OWNED BY public.cuerpo_tecnico_partido.id;


--
-- Name: noticia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.noticia (
    id integer NOT NULL,
    titulo character varying(200) NOT NULL,
    resumen text,
    contenido text NOT NULL,
    imagen character varying(255),
    fecha character varying(50)
);


ALTER TABLE public.noticia OWNER TO postgres;

--
-- Name: noticia_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.noticia_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.noticia_id_seq OWNER TO postgres;

--
-- Name: noticia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.noticia_id_seq OWNED BY public.noticia.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    password text NOT NULL,
    club_id integer,
    is_operador boolean NOT NULL,
    puede_cargar_incidencias boolean NOT NULL,
    puede_precargar_equipos boolean NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: Clubes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Clubes" ALTER COLUMN id SET DEFAULT nextval('public."Clubes_id_seq"'::regclass);


--
-- Name: Equipos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Equipos" ALTER COLUMN id SET DEFAULT nextval('public."Equipos_id_seq"'::regclass);


--
-- Name: Incidencias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Incidencias" ALTER COLUMN id SET DEFAULT nextval('public."Incidencias_id_seq"'::regclass);


--
-- Name: Jugadoras id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Jugadoras" ALTER COLUMN id SET DEFAULT nextval('public."Jugadoras_id_seq"'::regclass);


--
-- Name: NotasPartido id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."NotasPartido" ALTER COLUMN id SET DEFAULT nextval('public."NotasPartido_id_seq"'::regclass);


--
-- Name: Partidos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Partidos" ALTER COLUMN id SET DEFAULT nextval('public."Partidos_id_seq"'::regclass);


--
-- Name: PrecargaJugadoras id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PrecargaJugadoras" ALTER COLUMN id SET DEFAULT nextval('public."PrecargaJugadoras_id_seq"'::regclass);


--
-- Name: Resultados id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Resultados" ALTER COLUMN id SET DEFAULT nextval('public."Resultados_id_seq"'::regclass);


--
-- Name: arbitro_partido id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arbitro_partido ALTER COLUMN id SET DEFAULT nextval('public.arbitro_partido_id_seq'::regclass);


--
-- Name: arbitros id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arbitros ALTER COLUMN id SET DEFAULT nextval('public.arbitros_id_seq'::regclass);


--
-- Name: cuerpo_tecnico id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cuerpo_tecnico ALTER COLUMN id SET DEFAULT nextval('public.cuerpo_tecnico_id_seq'::regclass);


--
-- Name: cuerpo_tecnico_partido id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cuerpo_tecnico_partido ALTER COLUMN id SET DEFAULT nextval('public.cuerpo_tecnico_partido_id_seq'::regclass);


--
-- Name: noticia id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.noticia ALTER COLUMN id SET DEFAULT nextval('public.noticia_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Data for Name: Clubes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Clubes" (id, nombre, razon_social, contacto, email, cancha_local, domicilio, telefono, web, arbitro_id) FROM stdin;
1	Cuadro Nacional	CUADRO NACIONAL			CUADRO NACIONAL	Los Cedros 60			\N
3	San Jorge	SAN JORGE			SAN JORGE	Av. Guillermo Rawson & Alsina			\N
4	25 de Mayo	\N	\N	\N	\N	\N	\N	\N	\N
5	Fenix	\N	\N	\N	\N	\N	\N	\N	\N
6	Cuam	\N	\N	\N	\N	\N	\N	\N	\N
7	UTN	\N	\N	\N	\N	\N	\N	\N	\N
8	Guerreras Goudge	\N	\N	\N	\N	\N	\N	\N	\N
9	Monte Comán	\N	\N	\N	\N	\N	\N	\N	\N
10	Deportivo Malargüe	\N	\N	\N	\N	\N	\N	\N	\N
11	Emaus	\N	\N	\N	\N	\N	\N	\N	\N
12	Maristas Sub 14	\N	\N	\N	\N	\N	\N	\N	\N
13	Xeneizes	\N	\N	\N	\N	\N	\N	\N	\N
14	Sureñas	\N	\N	\N	\N	\N	\N	\N	\N
15	Deportivo Argentino	\N	\N	\N	\N	\N	\N	\N	\N
16	Cuadro Benegas	\N	\N	\N	\N	\N	\N	\N	\N
17	Cerbero	\N	\N	\N	\N	\N	\N	\N	\N
18	Morenas	\N	\N	\N	\N	\N	\N	\N	\N
19	Gacelas	\N	\N	\N	\N	\N	\N	\N	\N
20	Tenis Club	\N	\N	\N	\N	\N	\N	\N	\N
21	Banco Mendoza	\N	\N	\N	\N	\N	\N	\N	\N
22	Banco Municipal	\N	\N	\N	\N	\N	\N	\N	\N
23	Belgrano	\N	\N	\N	\N	\N	\N	\N	\N
24	Volantes	\N	\N	\N	\N	\N	\N	\N	\N
25	Panteras	\N	\N	\N	\N	\N	\N	\N	\N
26	Las Paredes	\N	\N	\N	\N	\N	\N	\N	\N
27	Maristas	\N	\N	\N	\N	\N	\N	\N	\N
28	Ohana	\N	\N	\N	\N	\N	\N	\N	\N
29	Deportivo Legendarias	\N	\N	\N	\N	\N	\N	\N	\N
30	Rebeldes	\N	\N	\N	\N	\N	\N	\N	\N
31	Ateneo	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: Equipos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Equipos" (id, nombre, categoria, club_id) FROM stdin;
1	25 de Mayo	Caballeros	4
2	Fenix	Caballeros	5
3	Cuadro Nacional	Caballeros	1
4	San Jorge	Caballeros	3
5	Cuam	Caballeros	6
9	San Jorge A	Damas A	3
10	San Jorge B	Damas B	3
12	Cuadro Nacional B	Damas A	1
13	Cuadro Nacional C	Damas B	1
16	UTN	Damas A	7
17	UTN	Mamis	7
18	Guerreras Goudge	Damas A	8
19	Guerreras Goudge	Mamis	8
20	Cuadro Nacional	Mamis	1
21	Monte Coman A	Damas A	9
22	Monte Coman B	Damas C	9
23	25 de Mayo	Damas A	4
24	25 de Mayo	Mamis	4
26	Cuadro Nacional A	Damas A	1
27	Gacelas	Damas B	19
28	Gacelas	Mamis	19
29	Tenis Club	Damas B	20
30	Tenis Club	Mamis	20
31	Belgrano	Damas C	23
32	Belgrano	Mamis	23
33	Deportivo Malargue	Damas A	10
34	Emaus	Damas A	11
35	Maristas Sub 14	Damas A	12
37	Xeneizes	Damas B	13
38	Deportivo Argentino	Damas B	15
39	Cuadro Benegas	Damas B	16
40	Cerbero	Damas B	17
41	Morenas	Damas B	18
42	Sure¤as	Damas B	14
43	Banco Mendoza	Damas C	21
44	Banco Municipal	Damas C	22
45	Volantes	Damas C	24
46	Panteras	Damas C	25
47	Las Paredes	Damas C	26
48	Maristas	Mamis	27
49	Ohana	Mamis	28
50	Deportivo Legendarias	Mamis	29
51	Rebeldes	Mamis	30
52	Ateneo	Mamis	31
\.


--
-- Data for Name: Incidencias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Incidencias" (id, partido_id, club_id, jugadora_id, tipo, color, minuto, created_at) FROM stdin;
1	3	1	55	gol	\N	12	2025-10-14 00:56:29.935831
2	3	1	48	tarjeta	amarilla	30	2025-10-14 00:56:45.517681
3	3	1	55	gol	\N	10	2025-10-14 20:10:08.237106
4	3	3	57	tarjeta	amarilla	10	2025-10-14 20:10:16.900785
5	3	1	55	gol	\N	10	2025-10-14 20:11:32.973579
6	3	1	52	tarjeta	amarilla	12	2025-10-14 20:11:39.783091
7	3	3	57	gol	\N	10	2025-10-14 20:11:46.727225
8	3	3	62	tarjeta	roja	28	2025-10-14 20:11:57.421709
9	4	5	65	gol	\N	10	2025-10-29 13:13:40.35335
10	4	5	65	gol	\N	12	2025-10-29 13:34:38.850112
11	4	4	72	tarjeta	verde	5	2025-10-29 13:34:50.377075
12	7	3	92	gol	\N	5	2025-10-30 22:01:00.909728
13	7	1	87	gol	\N	30	2025-10-30 22:01:05.871861
14	7	3	97	tarjeta	verde	2	2025-10-30 22:01:12.554292
15	7	1	90	tarjeta	roja	6	2025-10-30 22:01:19.952275
16	7	3	92	gol	\N	10	2025-10-30 22:08:17.305333
17	7	1	89	gol	\N	5	2025-10-30 22:08:22.600508
18	7	3	97	tarjeta	verde	30	2025-10-30 22:09:47.179778
19	7	1	91	tarjeta	roja	2	2025-10-30 22:09:57.803686
20	4	4	75	gol	\N	30	2025-10-30 22:21:25.613246
21	4	5	68	tarjeta	amarilla	6	2025-10-30 22:21:31.60228
22	4	4	76	tarjeta	verde	15	2025-10-30 22:21:37.340578
\.


--
-- Data for Name: Jugadoras; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Jugadoras" (id, nombre, apellido, dni, fecha_nacimiento, categoria, club_id) FROM stdin;
47	Hernan	Peñalbe	44538065	2002-11-21	DAMAS A	1
48	JugadorCuadro	Prueba2	53423425	2004-06-17	Caballeros	1
49	JugadorCuadro	Prueba3	123456	2004-06-17	Caballeros	1
50	JugadorCuadro	Prueba4	1234567	2004-06-17	Caballeros	1
51	JugadorCuadro	Prueba4	1234568	2004-06-17	Caballeros	1
52	JugadorCuadro	Prueba5	1234569	2004-06-17	Caballeros	1
53	JugadorCuadro	Prueba6	1234560	2004-06-17	Caballeros	1
54	JugadorCuadro	Prueba7	1234561	2004-06-17	Caballeros	1
55	JugadorCuadro	Prueba1	1234562	2004-06-17	Caballeros	1
56	JugadorSanJorge	Prueba1	12345622	2003-06-13	Caballeros	3
57	JugadorSanJorge	Prueba2	12345623	2003-06-13	Caballeros	3
58	JugadorSanJorge	Prueba4	12345624	2003-06-13	Caballeros	3
59	JugadorSanJorge	Prueba3	12345625	2003-06-13	Caballeros	3
60	JugadorSanJorge	Prueba6	12345626	2003-06-13	Caballeros	3
61	JugadorSanJorge	Prueba7	12345629	2003-06-13	Caballeros	3
62	JugadorSanJorge	Prueba5	12345620	2003-06-13	Caballeros	3
63	DamasB	Prueba1	7654321	2003-05-16	Damas B	5
64	Jugador	prueba1	123456789	2002-06-14	Caballeros	5
65	Jugador	prueba2	123456780	2002-06-22	Caballeros	5
66	Jugador	prueba3	1234567891	2002-11-15	Caballeros	5
67	Jugador	prueba4	1234567892	2002-06-14	Caballeros	5
68	Jugador	prueba5	1234567893	2002-08-16	Caballeros	5
69	Jugador	prueba6	1234567894	2002-06-14	Caballeros	5
70	Jugador	prueba7	1234567895	2002-06-14	Caballeros	5
71	Jugador25	prueba1	87654321	2002-06-14	Caballeros	4
72	Jugador25	prueba2	87654322	2002-06-14	Caballeros	4
73	Jugador25	prueba3	87654323	2002-06-14	Caballeros	4
74	Jugador25	prueba4	87654324	2002-06-14	Caballeros	4
75	Jugador25	prueba5	87654325	2002-06-14	Caballeros	4
76	Jugador25	prueba6	87654326	2002-06-14	Caballeros	4
77	Jugador25	prueba7	87654327	2002-06-14	Caballeros	4
85	Jugador1	PruebaB	27457847	2004-07-23	DAMAS A	1
86	Jugador2	PruebaB	27457846	2004-07-23	DAMAS A	1
87	Jugador3	PruebaB	27457845	2004-07-23	DAMAS A	1
88	Jugador4	PruebaB	27457844	2004-07-23	DAMAS A	1
89	Jugador5	PruebaB	27457843	2004-07-23	DAMAS A	1
90	Jugador6	PruebaB	27457842	2004-07-23	DAMAS A	1
91	Jugador7	PruebaB	27457841	2004-07-23	DAMAS A	1
92	Jugador	PruebaA	098765441	2002-06-20	DAMAS A	3
93	Jugador2	PruebaA	12345323	2002-06-20	DAMAS A	3
94	Jugador3	PruebaA	4453806545	2002-06-20	DAMAS A	3
95	Jugador5	PruebaA	42532453	2002-06-20	DAMAS A	3
96	Jugador4	PruebaA	5342342242	2002-06-20	DAMAS A	3
97	Jugador6	PruebaA	234354563	2002-06-20	DAMAS A	3
98	Jugador7	PruebaA	98765434	2002-06-20	DAMAS A	3
\.


--
-- Data for Name: NotasPartido; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."NotasPartido" (id, partido_id, detalle) FROM stdin;
\.


--
-- Data for Name: Partidos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Partidos" (id, torneo, categoria, fecha_numero, bloque, fecha_hora, cancha, club_local_id, club_visitante_id, estado, goles_local, goles_visitante, equipo_local_id, equipo_visitante_id) FROM stdin;
3	Clausura Caballeros (2025)	caballeros	1	A	2025-10-18 10:00:00	Cancha Municipal	3	1	jugado	\N	\N	\N	\N
5	Clausura Damas	Damas A	1	A	2025-10-25 18:00:00	Cuadro Nacional	7	8	programado	\N	\N	\N	\N
6	Clausura Damas	Damas A	1	A	2025-10-25 23:00:00	Maristas	11	12	programado	\N	\N	\N	\N
8	Clausura Damas	Damas A	1	A	2025-10-25 18:00:00	Cuadro Nacional	7	8	programado	\N	\N	16	18
9	Clausura Damas	Damas A	1	A	2025-10-25 20:00:00	Cuadro Nacional	9	4	programado	\N	\N	21	23
10	Clausura Damas	Damas A	1	A	2025-10-25 22:00:00	Poli N°2	1	10	programado	\N	\N	26	33
11	Clausura Damas	Damas A	1	A	2025-10-25 23:00:00	Maristas	11	12	programado	\N	\N	34	35
12	Clausura Damas	Damas A	2	A	2025-11-01 16:00:00	San Jorge	3	7	programado	\N	\N	9	16
13	Clausura Damas	Damas A	2	A	2025-11-01 18:00:00	Cuadro Nacional	1	8	programado	\N	\N	12	18
14	Clausura Damas	Damas A	2	A	2025-11-01 20:00:00	Cuadro Nacional	9	1	programado	\N	\N	21	26
15	Clausura Damas	Damas A	2	A	2025-11-01 22:00:00	Poli N°2	4	10	programado	\N	\N	23	33
16	Clausura Damas	Damas A	2	A	2025-11-01 23:00:00	San Jorge	11	3	programado	\N	\N	34	9
7	Clausura Damas	Damas A	1	A	2025-10-25 16:00:00	Poli N°2	3	1	jugado	\N	\N	9	12
4	Clausura Caballeros (2025)	caballeros	1	B	2025-10-18 12:00:00	Cancha Municipal	5	4	jugado	\N	\N	\N	\N
\.


--
-- Data for Name: PrecargaJugadoras; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."PrecargaJugadoras" (id, partido_id, club_id, jugadora_id, created_at) FROM stdin;
9	3	1	48	2025-10-13 23:41:57.163476
10	3	1	49	2025-10-13 23:41:57.163476
11	3	1	50	2025-10-13 23:41:57.163476
12	3	1	51	2025-10-13 23:41:57.163476
13	3	1	52	2025-10-13 23:41:57.163476
14	3	1	53	2025-10-13 23:41:57.163476
15	3	1	54	2025-10-13 23:41:57.163476
16	3	1	55	2025-10-13 23:41:57.163476
17	3	3	56	2025-10-13 23:53:47.548257
18	3	3	57	2025-10-13 23:53:47.548257
19	3	3	58	2025-10-13 23:53:47.548257
20	3	3	59	2025-10-13 23:53:47.548257
21	3	3	60	2025-10-13 23:53:47.548257
22	3	3	61	2025-10-13 23:53:47.548257
23	3	3	62	2025-10-13 23:53:47.548257
31	4	4	71	2025-10-20 23:28:03.225212
32	4	4	72	2025-10-20 23:28:03.225212
33	4	4	73	2025-10-20 23:28:03.225212
34	4	4	74	2025-10-20 23:28:03.225212
35	4	4	75	2025-10-20 23:28:03.225212
36	4	4	76	2025-10-20 23:28:03.225212
37	4	4	77	2025-10-20 23:28:03.225212
38	4	5	64	2025-10-29 13:10:31.145762
39	4	5	65	2025-10-29 13:10:31.145762
40	4	5	66	2025-10-29 13:10:31.145762
41	4	5	67	2025-10-29 13:10:31.145762
42	4	5	68	2025-10-29 13:10:31.145762
43	4	5	69	2025-10-29 13:10:31.145762
44	4	5	70	2025-10-29 13:10:31.145762
45	7	3	92	2025-10-30 21:28:17.673037
46	7	3	93	2025-10-30 21:28:17.673037
47	7	3	94	2025-10-30 21:28:17.673037
48	7	3	95	2025-10-30 21:28:17.673037
49	7	3	96	2025-10-30 21:28:17.673037
50	7	3	97	2025-10-30 21:28:17.673037
51	7	3	98	2025-10-30 21:28:17.673037
52	7	1	47	2025-10-30 21:28:32.168834
53	7	1	85	2025-10-30 21:28:32.168834
54	7	1	86	2025-10-30 21:28:32.168834
55	7	1	87	2025-10-30 21:28:32.168834
56	7	1	88	2025-10-30 21:28:32.168834
57	7	1	89	2025-10-30 21:28:32.168834
58	7	1	90	2025-10-30 21:28:32.168834
59	7	1	91	2025-10-30 21:28:32.168834
\.


--
-- Data for Name: Resultados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Resultados" (id, club_local, club_visitante, goles_local, goles_visitante, fecha) FROM stdin;
1	Club A	Club B	2	1	2025-08-31
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
bb38acd6bd8d
\.


--
-- Data for Name: arbitro_partido; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.arbitro_partido (id, partido_id, arbitro_id, rol) FROM stdin;
\.


--
-- Data for Name: arbitros; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.arbitros (id, nombre, apellido, dni, created_at) FROM stdin;
\.


--
-- Data for Name: cuerpo_tecnico; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cuerpo_tecnico (id, club_id, nombre, apellido, dni, rol, created_at) FROM stdin;
2	4	Ténico	Caballeros	034958934	DT	2025-10-20 21:27:00.308574
3	4	Preparador	fisico1	453453453	PF	2025-10-20 21:27:16.917945
4	5	Tecnico	Hombre	76543456	DT	2025-10-29 10:20:06.690916
5	5	Preparador	Hombres	353453454	PF	2025-10-29 10:20:21.334273
6	1	Tenico	B	3124123123	DT	2025-10-30 19:05:00.791944
7	1	Preparador	B	634534534	PF	2025-10-30 19:05:14.466598
8	3	Tecnico	A	64345434543	DT	2025-10-30 19:06:40.196365
9	3	Preparador	A	35376856	PF	2025-10-30 19:06:49.438262
\.


--
-- Data for Name: cuerpo_tecnico_partido; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cuerpo_tecnico_partido (id, partido_id, club_id, cuerpo_tecnico_id, rol) FROM stdin;
1	4	4	2	director_tecnico
2	4	4	3	preparador_fisico
3	7	3	8	director_tecnico
4	7	3	9	preparador_fisico
5	7	1	6	director_tecnico
6	7	1	7	preparador_fisico
7	4	5	4	director_tecnico
8	4	5	5	preparador_fisico
\.


--
-- Data for Name: noticia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.noticia (id, titulo, resumen, contenido, imagen, fecha) FROM stdin;
31	Hockey Acción: última fecha de la fase regular	Programa de partidos confirmados para la última fecha de la fase regular del Torneo Apertura Hockey Acción.	La Dirección de Deportes de San Rafael confirmó el programa de partidos válidos por la última fecha de la fase regular del Torneo Apertura correspondiente al Programa Hockey Acción.\n\nViernes 20\n11.30 hs. Poli 2. Primera C: Belgrano vs. Banco Municipal\n\n12.45 hs. Poli 2. Primera B: San Jorge B vs. Deportivo Argentino\n\n14 hs. Poli 2. Mamis: Guerreras vs. Gacelas\n\n15 hs. Poli 2. Mamis: Cuadro Nacional vs. Villa 25 de Mayo\n\nSábado 21\n\n14 hs. Poli 2. Primera C: Panteras vs. Cerbero B\n\n14 hs. Cancha de Cuadro Nacional. Mamis: Cuadro Nacional vs. UTN\n\n15.10 hs. Poli 2. Primera B: Cerbero A vs. San Luis\n\n15.15 hs. Cancha de Cuadro Nacional. Mamis: Ateneo vs. Maristas\n\n16.15 hs, Poli 2. Primera A: Guerreras vs. UTN\n\nDomingo 22\n\n9 hs. Poli 2. Primera A: Morenas vs. Maristas Sub 14\n\n9 hs. Cancha de Cuadro Nacional. Mamis: Belgrano vs. Deportivo Legendarias\n\n10 hs. Cancha de Cuadro Nacional. Primera A: San Jorge A vs. Monte Comán\n\n10.15 hs. Poli 2. Primera A: Guerreras vs. Cuadro Benegas\n\n11.20 hs. Cancha de Cuadro Nacional. Mamis: Rebeldes vs. Villa 25 de Mayo\n\n11.30 hs. Poli 2. Caballeros: San Jorge vs. Fénix\n\n12.30 hs. Cancha de Cuadro Nacional. Mamis: Ohana vs. Tenis Club\n\n12.45 hs. Poli 2. Caballeros: Villa 25 de Mayo vs. Cuadro Nacional	UltimaFecha.png	
32	Hockey Acción: así están las posiciones	Descubre cómo están las posiciones en el Torneo Apertura Hockey Acción tras los últimos resultados.	Se disputó una nueva fecha del Torneo Apertura del programa Hockey Acción que organiza la Dirección de Deportes de San Rafael.\n\nA continuación, repasamos y compartimos todos los resultados.\n\n<b>Primera A</b>\n\nCuadro Nacional B vs. UTN: 1-0\n\nCuadro Benegas vs. Marista: 0-6\n\nCuadro Nacional vs. Villa 25 de mayo: 1-0\n\nMonte Comán vs. Guerreras Goudge: 4-0\n\n<b>Caballeros</b>\n\nFénix vs. Cuadro Nacional: 2-0\n\nSan Jorge vs. Villa 25 de mayo: 0-0\n\n<b>Primera B</b>\n\nCuadro Nacional vs. Sureñas: 1-1\n\nSan Jorge vs. San Luis: 2-1\n\nDeportivo Malargüe vs. Deportivo Argentino: 1-2\n\nDeportivo Malargüe vs. San Jorge B: 3-0\n\nCerbero vs. Cuadro Nacional: 5-0\n\nTenis Club vs. Emaus: 0-3\n\n<b>Primera C</b>\n\nVolantes vs. Gacelas: 0-3\n\nMonte Comán B vs. Albinegras: 3-1\n\nVolantes vs. Pacifico: 1-1\n\nCerbero B vs. Banco Municipal: 0-4\n\n<b>Mamis</b>\n\nCuadro Nacional vs. Ateneo: 1-2\n\nBelgrano vs. Ohana: 2-0\n\nRebeldes vs. Maristas: 1-2\n\nDeportivo Legendarias vs. UTN: 4-0\n\nTenis Club vs. Guerreras: 0-0	Posicion.png	
33	Torneo Juvenil: grandes promesas en acción	El Torneo Juvenil reunió a los mejores talentos de la región en una jornada llena de emoción y competencia.	El pasado fin de semana se llevó a cabo el esperado Torneo Juvenil, donde jóvenes promesas del hockey demostraron su talento en la cancha.\n\n<b>Resultados destacados:</b>\n\nJuveniles A\n\nSan Jorge vs. Cuadro Nacional: 2-1\n\nMaristas vs. Villa 25 de Mayo: 3-0\n\nJuveniles B\n\nTenis Club vs. Deportivo Argentino: 1-1\n\nCerbero vs. UTN: 4-2\n\n<b>Próximos encuentros:</b>\n\nLa próxima fecha se disputará el sábado 28 de julio en el Poli 2, con partidos desde las 9:00 hs. ¡No te lo pierdas!	TorneoJuvenil.png	
36	Convocatoria a juveniles	Se abre la inscripción para la categoría juvenil.	Invitamos a todas las jugadoras nacidas entre 2008 y 2011 a sumarse a la categoría juvenil. Las inscripciones se realizan en la secretaría del club de lunes a viernes de 17 a 20 hs.	noticia4.jpg	
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, username, password, club_id, is_operador, puede_cargar_incidencias, puede_precargar_equipos) FROM stdin;
1	CuadroNacional.sr	scrypt:32768:8:1$pBSWhwVrZDdLtIaa$67d5cd90d06bce792ab827dd01792cb01f9312f350bf457be259b5bd4a1998e976ea5b97fbead780164275b915c285969a732929127d2b85eebbbc1e24a99047	1	f	f	f
3	SanJorge.sr	scrypt:32768:8:1$wCagPPTJ6bbSFsYi$59e55ac43c6b981b2b682c6ba9c3e922c2910fdb1913ff70b3c53747db5bd1492a27cda7d3c633ec7cb560894693937b85e5817fd38b8fab4205fb68ebcff714	3	f	f	f
4	25deMayo.sr	scrypt:32768:8:1$LpMRYGxt011aEkCC$53688eee5d7c5f08439e16583e01b9809ea0c90f4b0c9d4c945df56ece1257a935026f8ab0a5a4f81c366be5b6b4160bef8b8810a0dcf9ba961b4e7bf5c55258	4	f	f	f
5	Fenix.sr	scrypt:32768:8:1$qt6Lmo8JUmBKEXt7$413e129d48940f4682ed21e37eeb46fc271bb3d01dd2b277aa54c3de6b7c66f033c6dbe872071f8562e52706aa502f74076f83db8797b93434ae6fe8a486c2f4	5	f	f	f
6	Cuam.sr	scrypt:32768:8:1$1qWyUlygd1aieiQH$656964acf45b0790369d7fe4cbaa2e7e7a2dae882503318ad32c343966ad99ac55f2a699baa7b80bace1900eaf36549025b6bc40d2c229ad94b496f5fb1944f7	6	f	f	f
7	UTN.sr	scrypt:32768:8:1$OzaFVJpQxtMvNYus$2a6527f72865d0311fc2ce31cd36103205ee7378b7c836d2bd060f9f1dea0355d9cb73b9cf4a63a6138a55112688461f5c33d576b53d2539cf271ca92d38299e	7	f	f	f
8	GuerrerasGoudge.sr	scrypt:32768:8:1$LkNUKObExyEwnytQ$97d83bdd5fe4225865d0b202071d2bc186056d1eb31589b38987a92f09c613e1255ebd42ee93cba98335377cbc710f47dde04d850f1c6f2290ba59cf81169038	8	f	f	f
9	MonteComan.sr	scrypt:32768:8:1$hByqNTw82m8FzOMr$6248b489b878b19b195acca4a8db565079e403e4f4f1194697cdb1ff107912601ec160467aa13341bc290f58d6e084ca7764c1b93d79ef515784ab07e4c2715b	9	f	f	f
10	DeportivoMalargue.sr	scrypt:32768:8:1$UEMEirP2pVq1ay4N$67812dbe76d3c3d3dcad493fec64ce92ec450c57163f27dec2b827e3042bf9848f4988b3a6516868b53eb2315bd60846361f834a64a132b11019ee8a851e744a	10	f	f	f
11	Emaus.sr	scrypt:32768:8:1$Yk4RILFSL3WRdPGf$94e75d322abc28eaf049acf9182c84108feb434773ef9702bcac10ccb8f9a5d064bc86d343e52a94133a5cabd4e76c63112747721e4c6f22b5892061a6f51f80	11	f	f	f
12	MaristasSub14.sr	scrypt:32768:8:1$w7DnyimeY4pmigCI$5d9e1535f3f910ac1a263db7adf01cc69794dd07d3d57f28ec2af45fca8571c511e2d2e33b25e471fea96199275b15b2a2021897a5dba703525538f79dbb275f	12	f	f	f
13	Xeneizes.sr	scrypt:32768:8:1$PzgJJvjpLc50Mo3s$339bb4379e46fd31e934a26499cd7adb358f493a05ec03313e217f6801bc383cf9a14f897bb1a6006db99e980bc3c1a3c7b49ab9e597092f04ea1e058e125bbe	13	f	f	f
14	Sureñas.sr	scrypt:32768:8:1$TVQ0cNk7hwsAz7Zj$c751c544ae5f87ddf8063f74ae4726b3d45ffdc7e3c470dcab561a8a1242083a38d842f4bc0e4d21150e332c72b67b3ded9846b4938a7cd63ce2b2d466c24041	14	f	f	f
15	DeportivoArgentino.sr	scrypt:32768:8:1$ov21qLBeWvIlJe5k$7f0dd6a09662e90a41a9e0d2f3a31d59319486c91bce3a1f72a0b0d10bf9cc3ca395d09ad855e704642ef3466e78f5dfdfba9c9dfedbdaf0f0ffacb846a16f76	15	f	f	f
16	CuadroBenegas.sr	scrypt:32768:8:1$4N2Ozo0zjGf25mCY$4ab4ccafc89448e31526cc8846beabcdb5bbab90b08d22b9863316d09f085d8199ec7e386ed54198e1f09d8af287e6e1b0ef3ab587d69a894df36ff429f4a9da	16	f	f	f
17	Cerbero.sr	scrypt:32768:8:1$6FASLwUbHcCkOrYX$f600caced3abc731fec4a557ccadf9470f4b8e3026a0786bc9097819d2f284f9f54fd0921392d07bbdf22c0a66a6a0a85a308db6d9b5bc0fc3bd0114b4d0c4a5	17	f	f	f
18	Morenas.sr	scrypt:32768:8:1$tAjneMQLi3tPtAAa$308e5dbd2c06c5f31eb0ff753cb1729b25fc9a28f29cf869bf63973e6130fb5dfc0555e7b3dd7f8f6e313c7b5cc299c2d6054e04212dcd829b8083d58ed13e23	18	f	f	f
19	Gacelas.sr	scrypt:32768:8:1$y2Q5L082LGrFSxCG$d2bc2f5a50fa6f18714d1f47a823c287f26b1cd52940bb5260a79a8c66daa5b8a86ea5a7773576a9d455e9e8edf0cbf1bc81fc4ad119e67789071920bb990b5e	19	f	f	f
20	TenisClub.sr	scrypt:32768:8:1$2CZRjLlLHbOwkF8v$e994ad5369afd0d627795964f877bca9d2469cd55046ea586cf5efefb6543c249feb414177f4cc638bb74795b9c79598e364c3bcb03cf56c4b9ff80045f3f5bf	20	f	f	f
21	BancoMendoza.sr	scrypt:32768:8:1$qd7kdLOodQUbEZNl$8a28d865fb9d6c94ef0076df374ef16b524b7d55a87f44f3ce2877d83ae798710a6707e7e62b79c9b3039385206143b82afcfeceffdb72752c884bed767ea419	21	f	f	f
22	BancoMunicipal.sr	scrypt:32768:8:1$7e9NfHp1vJIq3kZa$89370a6e246e1b703a837816490881debd88da5d43966a9f55403e0800652c6c3d9f0b0db32a3aec8ec516012a7f669279123d8c5c937238a145ce2a25b09534	22	f	f	f
23	Belgrano.sr	scrypt:32768:8:1$zOz8XsznpnocF38V$44a5d362e085f0e674c035a9e28fb37c58fe9b59a83c72ef76f33018fb8ce515c59d7a08faa2032fd686813268352cea685aef434bce9879b41853a5d4476db5	23	f	f	f
24	Volantes.sr	scrypt:32768:8:1$lTP9MZScg3saeEWq$3fa200d9513efd39e8a855bab1d3556ce437a4eb83da25197edd189c60dec59ee2bc155dbbd33edd0ff063994b47ceb2614d056897f474e80b98f877b798bd26	24	f	f	f
25	Panteras.sr	scrypt:32768:8:1$I46jf8r4oxStYCXK$f1f50118110e0d70e5991a0a041aceb57ba479474c7beb0b54239877656fe938dc524fa5db504dd6f35eb9f019ce8c302387ace5ebaf9e0efea46d24ce861c9b	25	f	f	f
26	LasParedes.sr	scrypt:32768:8:1$DTxlqFozDcDAnK17$79ffa17f3407f37a9cda38f1d617f4709659ccfae17ccb506f03effd0c6526709aec2202597d44e73d353e102b0f18ac1666227fa0ade98e38a9e3873cceeccb	26	f	f	f
27	Maristas.sr	scrypt:32768:8:1$a9sDlkmwaS14qlxu$b8034414abbc4e2b678beab6689e549b038186a05440b881e771b666c854029466eadd0f21f73f814d7e071b28fcdf3877837e684b069d4a45a48541e503987a	27	f	f	f
28	Ohana.sr	scrypt:32768:8:1$18horNdPKS1IkfRW$26aa7eec692df0991c1b3927cc2cedac7dcd8ea8aed0e30dc3eb906425bd45ab60ccae206d1fb5ff7f5c44e7f2403c5066d4db34a787137b193b08570339d4da	28	f	f	f
29	DeportivoLegendarias.sr	scrypt:32768:8:1$fk4iVll605t8G4II$4a016daecab380ad21f98a0f8295a8e75dbe1c429b2bdc63dfe2da7f8e6f09dc32e1561302fb3b6e3bc2d69e877b2b0bcf56de5586ca6a5b9792ec87f10e9d59	29	f	f	f
30	Rebeldes.sr	scrypt:32768:8:1$JPaeMQFw7W5ngh2b$edbf5701f2e76d03ac6f25e9438b8a5e91edc6429d772086c86c5eec6029b22121a418a50ab678a6ac272c5fddecf3d1d8fb793e28b4ee46a34ccc600790debe	30	f	f	f
31	Ateneo.sr	scrypt:32768:8:1$BGPPHUH9eekUIATp$f42059cba7d5f7f696fed17547459256b965cf1fab97ad9ee25af39a444ba1d177af5d7848b056ca507329c1d8e9d258edc423d83c3cd8885144cd56dc76a50e	31	f	f	f
33	Juli.sr	scrypt:32768:8:1$g3doTtM0lVdSGSfz$0704fef7bf4e614cd12794e4ce063f8d8778d8e1b67f23f8f933afbb9db75d5ae681740c0879d3f3385b334946102e4f58eaab82306715ca7c671b6502648db7	\N	t	t	t
\.


--
-- Name: Clubes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Clubes_id_seq"', 31, true);


--
-- Name: Equipos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Equipos_id_seq"', 52, true);


--
-- Name: Incidencias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Incidencias_id_seq"', 22, true);


--
-- Name: Jugadoras_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Jugadoras_id_seq"', 98, true);


--
-- Name: NotasPartido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."NotasPartido_id_seq"', 1, false);


--
-- Name: Partidos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Partidos_id_seq"', 16, true);


--
-- Name: PrecargaJugadoras_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."PrecargaJugadoras_id_seq"', 59, true);


--
-- Name: Resultados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Resultados_id_seq"', 1, true);


--
-- Name: arbitro_partido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.arbitro_partido_id_seq', 1, false);


--
-- Name: arbitros_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.arbitros_id_seq', 1, false);


--
-- Name: cuerpo_tecnico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cuerpo_tecnico_id_seq', 9, true);


--
-- Name: cuerpo_tecnico_partido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cuerpo_tecnico_partido_id_seq', 8, true);


--
-- Name: noticia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.noticia_id_seq', 36, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 33, true);


--
-- Name: Clubes Clubes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Clubes"
    ADD CONSTRAINT "Clubes_pkey" PRIMARY KEY (id);


--
-- Name: Equipos Equipos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Equipos"
    ADD CONSTRAINT "Equipos_pkey" PRIMARY KEY (id);


--
-- Name: Incidencias Incidencias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Incidencias"
    ADD CONSTRAINT "Incidencias_pkey" PRIMARY KEY (id);


--
-- Name: Jugadoras Jugadoras_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Jugadoras"
    ADD CONSTRAINT "Jugadoras_pkey" PRIMARY KEY (id);


--
-- Name: NotasPartido NotasPartido_partido_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."NotasPartido"
    ADD CONSTRAINT "NotasPartido_partido_id_key" UNIQUE (partido_id);


--
-- Name: NotasPartido NotasPartido_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."NotasPartido"
    ADD CONSTRAINT "NotasPartido_pkey" PRIMARY KEY (id);


--
-- Name: Partidos Partidos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Partidos"
    ADD CONSTRAINT "Partidos_pkey" PRIMARY KEY (id);


--
-- Name: PrecargaJugadoras PrecargaJugadoras_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PrecargaJugadoras"
    ADD CONSTRAINT "PrecargaJugadoras_pkey" PRIMARY KEY (id);


--
-- Name: Resultados Resultados_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Resultados"
    ADD CONSTRAINT "Resultados_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: arbitro_partido arbitro_partido_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arbitro_partido
    ADD CONSTRAINT arbitro_partido_pkey PRIMARY KEY (id);


--
-- Name: arbitros arbitros_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arbitros
    ADD CONSTRAINT arbitros_pkey PRIMARY KEY (id);


--
-- Name: cuerpo_tecnico_partido cuerpo_tecnico_partido_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cuerpo_tecnico_partido
    ADD CONSTRAINT cuerpo_tecnico_partido_pkey PRIMARY KEY (id);


--
-- Name: cuerpo_tecnico cuerpo_tecnico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cuerpo_tecnico
    ADD CONSTRAINT cuerpo_tecnico_pkey PRIMARY KEY (id);


--
-- Name: noticia noticia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.noticia
    ADD CONSTRAINT noticia_pkey PRIMARY KEY (id);


--
-- Name: arbitro_partido uq_arbitro_partido_arbitro; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arbitro_partido
    ADD CONSTRAINT uq_arbitro_partido_arbitro UNIQUE (partido_id, arbitro_id);


--
-- Name: cuerpo_tecnico_partido uq_ct_partido_club_rol; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cuerpo_tecnico_partido
    ADD CONSTRAINT uq_ct_partido_club_rol UNIQUE (partido_id, club_id, rol);


--
-- Name: PrecargaJugadoras uq_precarga_partido_club_jugadora; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PrecargaJugadoras"
    ADD CONSTRAINT uq_precarga_partido_club_jugadora UNIQUE (partido_id, club_id, jugadora_id);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_username_key UNIQUE (username);


--
-- Name: Incidencias Incidencias_club_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Incidencias"
    ADD CONSTRAINT "Incidencias_club_id_fkey" FOREIGN KEY (club_id) REFERENCES public."Clubes"(id);


--
-- Name: Incidencias Incidencias_jugadora_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Incidencias"
    ADD CONSTRAINT "Incidencias_jugadora_id_fkey" FOREIGN KEY (jugadora_id) REFERENCES public."Jugadoras"(id);


--
-- Name: Incidencias Incidencias_partido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Incidencias"
    ADD CONSTRAINT "Incidencias_partido_id_fkey" FOREIGN KEY (partido_id) REFERENCES public."Partidos"(id);


--
-- Name: NotasPartido NotasPartido_partido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."NotasPartido"
    ADD CONSTRAINT "NotasPartido_partido_id_fkey" FOREIGN KEY (partido_id) REFERENCES public."Partidos"(id);


--
-- Name: Partidos Partidos_club_local_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Partidos"
    ADD CONSTRAINT "Partidos_club_local_id_fkey" FOREIGN KEY (club_local_id) REFERENCES public."Clubes"(id);


--
-- Name: Partidos Partidos_club_visitante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Partidos"
    ADD CONSTRAINT "Partidos_club_visitante_id_fkey" FOREIGN KEY (club_visitante_id) REFERENCES public."Clubes"(id);


--
-- Name: Partidos Partidos_equipo_local_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Partidos"
    ADD CONSTRAINT "Partidos_equipo_local_id_fkey" FOREIGN KEY (equipo_local_id) REFERENCES public."Equipos"(id);


--
-- Name: Partidos Partidos_equipo_visitante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Partidos"
    ADD CONSTRAINT "Partidos_equipo_visitante_id_fkey" FOREIGN KEY (equipo_visitante_id) REFERENCES public."Equipos"(id);


--
-- Name: PrecargaJugadoras PrecargaJugadoras_club_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PrecargaJugadoras"
    ADD CONSTRAINT "PrecargaJugadoras_club_id_fkey" FOREIGN KEY (club_id) REFERENCES public."Clubes"(id);


--
-- Name: PrecargaJugadoras PrecargaJugadoras_jugadora_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PrecargaJugadoras"
    ADD CONSTRAINT "PrecargaJugadoras_jugadora_id_fkey" FOREIGN KEY (jugadora_id) REFERENCES public."Jugadoras"(id);


--
-- Name: PrecargaJugadoras PrecargaJugadoras_partido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PrecargaJugadoras"
    ADD CONSTRAINT "PrecargaJugadoras_partido_id_fkey" FOREIGN KEY (partido_id) REFERENCES public."Partidos"(id);


--
-- Name: arbitro_partido arbitro_partido_arbitro_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arbitro_partido
    ADD CONSTRAINT arbitro_partido_arbitro_id_fkey FOREIGN KEY (arbitro_id) REFERENCES public.arbitros(id);


--
-- Name: arbitro_partido arbitro_partido_partido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arbitro_partido
    ADD CONSTRAINT arbitro_partido_partido_id_fkey FOREIGN KEY (partido_id) REFERENCES public."Partidos"(id);


--
-- Name: cuerpo_tecnico cuerpo_tecnico_club_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cuerpo_tecnico
    ADD CONSTRAINT cuerpo_tecnico_club_id_fkey FOREIGN KEY (club_id) REFERENCES public."Clubes"(id);


--
-- Name: cuerpo_tecnico_partido cuerpo_tecnico_partido_club_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cuerpo_tecnico_partido
    ADD CONSTRAINT cuerpo_tecnico_partido_club_id_fkey FOREIGN KEY (club_id) REFERENCES public."Clubes"(id);


--
-- Name: cuerpo_tecnico_partido cuerpo_tecnico_partido_cuerpo_tecnico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cuerpo_tecnico_partido
    ADD CONSTRAINT cuerpo_tecnico_partido_cuerpo_tecnico_id_fkey FOREIGN KEY (cuerpo_tecnico_id) REFERENCES public.cuerpo_tecnico(id);


--
-- Name: cuerpo_tecnico_partido cuerpo_tecnico_partido_partido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cuerpo_tecnico_partido
    ADD CONSTRAINT cuerpo_tecnico_partido_partido_id_fkey FOREIGN KEY (partido_id) REFERENCES public."Partidos"(id);


--
-- Name: usuarios fk_club; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT fk_club FOREIGN KEY (club_id) REFERENCES public."Clubes"(id);


--
-- Name: Equipos fk_equipo_club; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Equipos"
    ADD CONSTRAINT fk_equipo_club FOREIGN KEY (club_id) REFERENCES public."Clubes"(id);


--
-- Name: Jugadoras fk_jugadora_club; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Jugadoras"
    ADD CONSTRAINT fk_jugadora_club FOREIGN KEY (club_id) REFERENCES public."Clubes"(id);


--
-- PostgreSQL database dump complete
--

