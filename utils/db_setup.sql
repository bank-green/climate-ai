CREATE EXTENSION vector;

CREATE TYPE feedback AS ENUM
('good', 'bad');

CREATE TYPE answer AS ENUM
('yes', 'no', 'unclear');

CREATE TABLE "public"."banks"
(
    "tag" text NOT NULL,
    "name" text NOT NULL,
    PRIMARY KEY ("tag")
);

CREATE TABLE "public"."documents"
(
    "id" serial,
    "bank_tag" text NOT NULL,
    "name" text NOT NULL,
    "parsed_text" text NOT NULL,
    "file" bytea DEFAULT NULL,
    PRIMARY KEY ("id")
);

ALTER TABLE "public"."documents" ADD FOREIGN KEY ("bank_tag") REFERENCES "public"."banks" ("tag") ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TABLE "public"."embeddings"
(
    "id" serial,
    "document_id" int4 NOT NULL,
    "chunk" text NOT NULL DEFAULT '',
    "embedding" vector(768) NOT NULL,
    PRIMARY KEY ("id")
);

ALTER TABLE "public"."embeddings" ADD FOREIGN KEY ("document_id") REFERENCES "public"."documents" ("id") ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TABLE "public"."questions"
(
    "id" serial,
    "question" text NOT NULL DEFAULT '',
    "embedding" vector(768) NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE "public"."answers"
(
    "id" serial,
    "question_id" int4,
    "llm_answer" text NOT NULL,
    "human_answer" answer DEFAULT NULL,
    "human_feedback" feedback DEFAULT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE "public"."answers_embeddings"
(
    "answer_id" int4 NOT NULL,
    "embedding_id" int4 NOT NULL,
    PRIMARY KEY ("answer_id", "embedding_id")
);

ALTER TABLE "public"."answers_embeddings" ADD FOREIGN KEY ("answer_id") REFERENCES "public"."answers" ("id") ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE "public"."answers_embeddings" ADD FOREIGN KEY ("embedding_id") REFERENCES "public"."embeddings" ("id") ON UPDATE CASCADE ON DELETE CASCADE;