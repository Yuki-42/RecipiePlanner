/*
Initialise logs database. Visual layout can be found at [db_schema](db_schema.drawio)

LANG=PGSQL
*/

/* Check what database is currently selected */
SELECT CURRENT_DATABASE();

/* Install UUID extension */
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "lo";

/* Create tables */
CREATE TABLE IF NOT EXISTS users
(
    id           UUID PRIMARY KEY   DEFAULT uuid_generate_v4(),
    added        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username     TEXT      NOT NULL,
    email        TEXT      NOT NULL,
    password     TEXT      NOT NULL,
    otp_secret   TEXT,
    backup_codes TEXT[8],
    pfp_img      BYTEA,
    is_active    BOOLEAN   NOT NULL DEFAULT TRUE,
    is_admin     BOOLEAN   NOT NULL DEFAULT FALSE,
    is_banned    BOOLEAN   NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS recipies
(
    id           UUID PRIMARY KEY   DEFAULT uuid_generate_v4(),
    added        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    url          TEXT      NOT NULL,
    name         TEXT,
    description  TEXT,
    ingredients  TEXT[],
    steps        TEXT[],
    is_public    BOOLEAN   NOT NULL DEFAULT FALSE,
    is_deleted   BOOLEAN   NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS comments
(
    id           UUID PRIMARY KEY   DEFAULT uuid_generate_v4(),
    added        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recipe_id    UUID      NOT NULL,
    user_id      UUID      NOT NULL,
    content      TEXT,
    is_deleted   BOOLEAN   NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS ratings
(
    id           UUID PRIMARY KEY   DEFAULT uuid_generate_v4(),
    added        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recipe_id    UUID      NOT NULL,
    user_id      UUID      NOT NULL,
    rating       INT       NOT NULL
);

CREATE TABLE IF NOT EXISTS tags
(
    id           UUID PRIMARY KEY   DEFAULT uuid_generate_v4(),
    added        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recipe_id    UUID      NOT NULL,
    tag          TEXT      NOT NULL,
    added_by     UUID      NOT NULL
);

CREATE TABLE IF NOT EXISTS relations.recipe_tags
(
    id           UUID PRIMARY KEY   DEFAULT uuid_generate_v4(),
    added        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recipe_id    UUID      NOT NULL,
    tag_id       UUID      NOT NULL,
    added_by     UUID      NOT NULL
);

CREATE TABLE IF NOT EXISTS images.originals
(
    id           UUID PRIMARY KEY   DEFAULT uuid_generate_v4(),
    added        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recipe_id    UUID      NOT NULL,
    img          LO
);

CREATE TABLE IF NOT EXISTS images.thumbnails
(
    id           UUID PRIMARY KEY   DEFAULT uuid_generate_v4(),
    added        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    original_id  UUID      NOT NULL,
    img          BYTEA
);

CREATE TABLE IF NOT EXISTS images.attachments
(
    id           UUID PRIMARY KEY   DEFAULT uuid_generate_v4(),
    added        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recipe_id    UUID      NOT NULL,
    img          LO,
    src          TEXT,
    alt          TEXT,
    is_deleted   BOOLEAN   NOT NULL DEFAULT FALSE
);

/* Create indexes */

/* Create relationships */
ALTER TABLE comments
    ADD FOREIGN KEY (recipe_id) REFERENCES recipies (id) ON DELETE CASCADE;
ALTER TABLE comments
    ADD FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE;

ALTER TABLE ratings
    ADD FOREIGN KEY (recipe_id) REFERENCES recipies (id) ON DELETE CASCADE;
ALTER TABLE ratings
    ADD FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE;

ALTER TABLE tags
    ADD FOREIGN KEY (recipe_id) REFERENCES recipies (id) ON DELETE CASCADE;
ALTER TABLE tags
    ADD FOREIGN KEY (added_by) REFERENCES users (id) ON DELETE CASCADE;

ALTER TABLE relations.recipe_tags
    ADD FOREIGN KEY (recipe_id) REFERENCES recipies (id) ON DELETE CASCADE;
ALTER TABLE relations.recipe_tags
    ADD FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE;

ALTER TABLE images.originals
    ADD FOREIGN KEY (recipe_id) REFERENCES recipies (id) ON DELETE CASCADE;

ALTER TABLE images.thumbnails
    ADD FOREIGN KEY (original_id) REFERENCES images.originals (id) ON DELETE CASCADE;

ALTER TABLE images.attachments
    ADD FOREIGN KEY (recipe_id) REFERENCES recipies (id) ON DELETE CASCADE;
