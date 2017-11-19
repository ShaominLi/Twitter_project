--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.8
-- Dumped by pg_dump version 9.5.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: comment_like; Type: TABLE; Schema: public; Owner: g1
--

CREATE TABLE comment_like (
    userid bigint,
    commentid bigint
);


ALTER TABLE comment_like OWNER TO g1;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: g1
--

CREATE TABLE comments (
    commentid integer NOT NULL,
    postid bigint,
    userid bigint,
    comment text,
    date time with time zone
);


ALTER TABLE comments OWNER TO g1;

--
-- Name: comments_commentid_seq; Type: SEQUENCE; Schema: public; Owner: g1
--

CREATE SEQUENCE comments_commentid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comments_commentid_seq OWNER TO g1;

--
-- Name: comments_commentid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: g1
--

ALTER SEQUENCE comments_commentid_seq OWNED BY comments.commentid;


--
-- Name: friends; Type: TABLE; Schema: public; Owner: g1
--

CREATE TABLE friends (
    friendid bigint,
    userid bigint
);


ALTER TABLE friends OWNER TO g1;

--
-- Name: post; Type: TABLE; Schema: public; Owner: g1
--

CREATE TABLE post (
    postid integer NOT NULL,
    userid bigint,
    date time with time zone,
    comment text
);


ALTER TABLE post OWNER TO g1;

--
-- Name: post_like; Type: TABLE; Schema: public; Owner: g1
--

CREATE TABLE post_like (
    postid bigint,
    userid bigint
);


ALTER TABLE post_like OWNER TO g1;

--
-- Name: post_postid_seq; Type: SEQUENCE; Schema: public; Owner: g1
--

CREATE SEQUENCE post_postid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE post_postid_seq OWNER TO g1;

--
-- Name: post_postid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: g1
--

ALTER SEQUENCE post_postid_seq OWNED BY post.postid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: g1
--

CREATE TABLE users (
    userid integer NOT NULL,
    name text,
    password text,
    email text,
    country text,
    inscription_date time with time zone
);


ALTER TABLE users OWNER TO g1;

--
-- Name: users_userid_seq; Type: SEQUENCE; Schema: public; Owner: g1
--

CREATE SEQUENCE users_userid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_userid_seq OWNER TO g1;

--
-- Name: users_userid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: g1
--

ALTER SEQUENCE users_userid_seq OWNED BY users.userid;


--
-- Name: commentid; Type: DEFAULT; Schema: public; Owner: g1
--

ALTER TABLE ONLY comments ALTER COLUMN commentid SET DEFAULT nextval('comments_commentid_seq'::regclass);


--
-- Name: postid; Type: DEFAULT; Schema: public; Owner: g1
--

ALTER TABLE ONLY post ALTER COLUMN postid SET DEFAULT nextval('post_postid_seq'::regclass);


--
-- Name: userid; Type: DEFAULT; Schema: public; Owner: g1
--

ALTER TABLE ONLY users ALTER COLUMN userid SET DEFAULT nextval('users_userid_seq'::regclass);


--
-- Name: FK_commentid; Type: CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT "FK_commentid" PRIMARY KEY (commentid);


--
-- Name: PK_postid; Type: CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY post
    ADD CONSTRAINT "PK_postid" PRIMARY KEY (postid);


--
-- Name: PK_users; Type: CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY users
    ADD CONSTRAINT "PK_users" PRIMARY KEY (userid);


--
-- Name: FKI_CL_commentid; Type: INDEX; Schema: public; Owner: g1
--

CREATE INDEX "FKI_CL_commentid" ON comment_like USING btree (commentid);


--
-- Name: FKI_CL_userid; Type: INDEX; Schema: public; Owner: g1
--

CREATE INDEX "FKI_CL_userid" ON comment_like USING btree (userid);


--
-- Name: FKI_comments_postid; Type: INDEX; Schema: public; Owner: g1
--

CREATE INDEX "FKI_comments_postid" ON comments USING btree (postid);


--
-- Name: FKI_comments_userid; Type: INDEX; Schema: public; Owner: g1
--

CREATE INDEX "FKI_comments_userid" ON comments USING btree (userid);


--
-- Name: FKI_friends_friendid; Type: INDEX; Schema: public; Owner: g1
--

CREATE INDEX "FKI_friends_friendid" ON friends USING btree (friendid);


--
-- Name: FKI_friends_userid; Type: INDEX; Schema: public; Owner: g1
--

CREATE INDEX "FKI_friends_userid" ON friends USING btree (userid);


--
-- Name: FKI_post_like_postid; Type: INDEX; Schema: public; Owner: g1
--

CREATE INDEX "FKI_post_like_postid" ON post_like USING btree (postid);


--
-- Name: FKI_post_like_userid; Type: INDEX; Schema: public; Owner: g1
--

CREATE INDEX "FKI_post_like_userid" ON post_like USING btree (userid);


--
-- Name: FKI_post_userid; Type: INDEX; Schema: public; Owner: g1
--

CREATE INDEX "FKI_post_userid" ON post USING btree (userid);


--
-- Name: FK_CL_commentid; Type: FK CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY comment_like
    ADD CONSTRAINT "FK_CL_commentid" FOREIGN KEY (commentid) REFERENCES comments(commentid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: FK_CL_userid; Type: FK CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY comment_like
    ADD CONSTRAINT "FK_CL_userid" FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: FK_comments_postid; Type: FK CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT "FK_comments_postid" FOREIGN KEY (postid) REFERENCES post(postid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: FK_comments_userid; Type: FK CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT "FK_comments_userid" FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: FK_friends_friendid; Type: FK CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY friends
    ADD CONSTRAINT "FK_friends_friendid" FOREIGN KEY (friendid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: FK_friends_userid; Type: FK CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY friends
    ADD CONSTRAINT "FK_friends_userid" FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: FK_post_like_postid; Type: FK CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY post_like
    ADD CONSTRAINT "FK_post_like_postid" FOREIGN KEY (postid) REFERENCES post(postid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: FK_post_like_userid; Type: FK CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY post_like
    ADD CONSTRAINT "FK_post_like_userid" FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: FK_post_userid; Type: FK CONSTRAINT; Schema: public; Owner: g1
--

ALTER TABLE ONLY post
    ADD CONSTRAINT "FK_post_userid" FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

