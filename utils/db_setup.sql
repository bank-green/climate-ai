CREATE EXTENSION vector;

CREATE TYPE feedback AS ENUM
('good', 'bad');

CREATE TYPE answer AS ENUM
('yes', 'no', 'unclear');

CREATE TABLE "public"."Banks"
(
    "tag" text NOT NULL,
    "name" text NOT NULL,
    PRIMARY KEY ("tag")
);

CREATE TABLE "public"."Documents"
(
    "id" serial,
    "bank_tag" text NOT NULL,
    "name" text NOT NULL,
    "file" bytea DEFAULT NULL,
    PRIMARY KEY ("id")
);

ALTER TABLE "public"."Documents" ADD FOREIGN KEY ("bank_tag") REFERENCES "public"."Banks" ("tag") ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TABLE "public"."Embeddings"
(
    "id" serial,
    "document_id" int4 NOT NULL,
    "chunk" text NOT NULL DEFAULT '',
    "embedding" vector(768) NOT NULL,
    PRIMARY KEY ("id")
);

ALTER TABLE "public"."Embeddings" ADD FOREIGN KEY ("document_id") REFERENCES "public"."Documents" ("id") ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TABLE "public"."Questions"
(
    "id" serial,
    "question" text NOT NULL DEFAULT '',
    PRIMARY KEY ("id")
);

CREATE TABLE "public"."Answers"
(
    "id" serial,
    "question_id" int4,
    "llm_answer" text NOT NULL,
    "human_answer" answer DEFAULT NULL,
    "human_feedback" feedback DEFAULT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE "public"."Answers_Embeddings"
(
    "answer_id" int4 NOT NULL,
    "embedding_id" int4 NOT NULL,
    PRIMARY KEY ("answer_id", "embedding_id")
);

ALTER TABLE "public"."Answers_Embeddings" ADD FOREIGN KEY ("answer_id") REFERENCES "public"."Answers" ("id") ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE "public"."Answers_Embeddings" ADD FOREIGN KEY ("embedding_id") REFERENCES "public"."Embeddings" ("id") ON UPDATE CASCADE ON DELETE CASCADE;