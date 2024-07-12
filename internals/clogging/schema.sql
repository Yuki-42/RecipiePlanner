/*
Initialise logs database. More detailed database layout can be found in [docs/database.md](docs/database.md)

LANG=PGSQL
*/

/* Check what database is currently selected */
SELECT CURRENT_DATABASE();

/* Create tables */
CREATE TABLE IF NOT EXISTS recipe_planner.program_logs
(
    id           SERIAL    NOT NULL PRIMARY KEY,
    timestamp    TIMESTAMP NOT NULL,
    level        INT       NOT NULL,
    filename     TEXT      NOT NULL,
    funcname     TEXT      NOT NULL,
    lineno       TEXT      NOT NULL,
    message      TEXT      NOT NULL,
    module       TEXT      NOT NULL,
    name         TEXT      NOT NULL,
    pathname     TEXT      NOT NULL,
    process      TEXT      NOT NULL,
    process_name TEXT      NOT NULL,
    thread       TEXT,
    thread_name  TEXT
);

CREATE TABLE IF NOT EXISTS recipe_planner.requests
(
    id                INT  NOT NULL PRIMARY KEY,
    log_id            INT  NOT NULL,
    view_args         jsonb,
    routing_exception TEXT,
    endpoint          TEXT,
    blueprint         TEXT,
    blueprints        TEXT[],
    accept_languages  TEXT,
    accept_mimetypes  TEXT,
    access_route      TEXT[],
    args              jsonb,
    "authorization"   TEXT,
    base_url          TEXT,
    cookies           jsonb,
    full_path         TEXT,
    host              TEXT,
    host_url          TEXT,
    url               TEXT,
    method            TEXT,
    headers           TEXT,
    remote_addr       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipe_planner.responses
(
    id          SERIAL NOT NULL PRIMARY KEY,
    request_id  INT    NOT NULL,
    expires     TIMESTAMP,
    location    TEXT,
    status      TEXT,
    status_code INT,
    headers     TEXT,
    response    TEXT
);

/* Create indexes that don't exist */
CREATE INDEX IF NOT EXISTS program_logs_timestamp ON recipe_planner.program_logs (timestamp);
CREATE INDEX IF NOT EXISTS program_logs_level ON recipe_planner.program_logs (level);
CREATE INDEX IF NOT EXISTS program_logs_funcname ON recipe_planner.program_logs (funcname);
CREATE INDEX IF NOT EXISTS program_logs_module ON recipe_planner.program_logs (module);
CREATE INDEX IF NOT EXISTS program_logs_name ON recipe_planner.program_logs (name);

CREATE INDEX IF NOT EXISTS requests_log_id ON recipe_planner.requests (log_id);
CREATE INDEX IF NOT EXISTS requests_endpoint ON recipe_planner.requests (endpoint);
CREATE INDEX IF NOT EXISTS requests_blueprint ON recipe_planner.requests (blueprint);
CREATE INDEX IF NOT EXISTS requests_method ON recipe_planner.requests (method);
CREATE INDEX IF NOT EXISTS requests_remote_addr ON recipe_planner.requests (remote_addr);

CREATE INDEX IF NOT EXISTS responses_request_id ON recipe_planner.responses (request_id);
CREATE INDEX IF NOT EXISTS responses_status_code ON recipe_planner.responses (status_code);

/* Create foreign keys */
ALTER TABLE recipe_planner.requests
    ADD FOREIGN KEY (log_id) REFERENCES recipe_planner.program_logs (id);
ALTER TABLE recipe_planner.responses
    ADD FOREIGN KEY (request_id) REFERENCES recipe_planner.requests (id);

/* Give all permissions to the recipe_planner_logger user */
GRANT ALL ON ALL TABLES IN SCHEMA recipe_planner TO recipe_planner_logger;

/* Create views */
DROP VIEW IF EXISTS recipe_planner.web_logs;
DROP VIEW IF EXISTS recipe_planner.simple_requests;
DROP VIEW IF EXISTS recipe_planner.simple_responses;

/* View joins program_logs, requests, and responses. More columns will be manually added */
CREATE VIEW recipe_planner.web_logs(timestamp, method, remote_addr, path, status) AS
SELECT program_logs.timestamp,
       requests.method,
       requests.remote_addr,
       requests.full_path,
       responses.status_code
FROM recipe_planner.program_logs
         JOIN
     recipe_planner.requests ON program_logs.id = requests.log_id
         JOIN
     recipe_planner.responses ON requests.id = responses.request_id;

COMMENT ON VIEW recipe_planner.web_logs IS 'Used for viewing unified web logs.';

ALTER VIEW recipe_planner.web_logs
    OWNER TO recipe_planner_logger;

CREATE VIEW recipe_planner.simple_requests(method, remote_addr, full_path, cookies, args, view_args, id, log_id) AS
SELECT requests.method,
       requests.remote_addr,
       requests.full_path,
       requests.cookies,
       requests.args,
       requests.view_args,
       requests.id,
       requests.log_id
FROM recipe_planner.requests;

COMMENT ON VIEW recipe_planner.simple_requests IS 'Used to view requests in a more logical order and format.';

ALTER TABLE recipe_planner.simple_requests
    OWNER TO recipe_planner_logger;


CREATE VIEW recipe_planner.simple_responses(status, status_code, request_id, headers, response) AS
SELECT response.status,
       response.status_code,
       response.request_id,
       response.headers,
       response.response
FROM recipe_planner.responses response;

COMMENT ON VIEW recipe_planner.simple_responses IS 'Used to view responses in a more logical order and format.';

ALTER TABLE recipe_planner.simple_responses
    OWNER TO recipe_planner_logger;


