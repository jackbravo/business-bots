-- Esquema SQLite NPV v1: aplicar solo sobre un archivo autorizado.
CREATE TABLE IF NOT EXISTS npv_schema_versions (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP_TZ NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00','now'))
);
CREATE TABLE IF NOT EXISTS npv_sources (
    source_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    category VARCHAR NOT NULL
);
CREATE TABLE IF NOT EXISTS npv_ingestion_runs (
    run_id VARCHAR PRIMARY KEY,
    source_id VARCHAR NOT NULL REFERENCES npv_sources(source_id),
    retrieved_at TIMESTAMP_TZ NOT NULL,
    loaded_at TIMESTAMP_TZ NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00','now')),
    content_hash VARCHAR NOT NULL,
    request_url VARCHAR,
    row_count INTEGER NOT NULL,
    new_revisions INTEGER NOT NULL,
    CHECK (row_count >= 0 AND new_revisions >= 0)
);
CREATE TABLE IF NOT EXISTS npv_indicators (
    indicator_id VARCHAR PRIMARY KEY,
    source_id VARCHAR NOT NULL REFERENCES npv_sources(source_id),
    source_series_id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    unit VARCHAR NOT NULL,
    frequency VARCHAR NOT NULL CHECK (frequency IN ('daily','monthly','quarterly','annual')),
    UNIQUE (source_id, source_series_id)
);
CREATE TABLE IF NOT EXISTS npv_observations (
    indicator_id VARCHAR NOT NULL REFERENCES npv_indicators(indicator_id),
    geography VARCHAR NOT NULL,
    period VARCHAR NOT NULL,
    revision INTEGER NOT NULL CHECK (revision > 0),
    value DECIMAL_TEXT,
    status VARCHAR NOT NULL CHECK (status IN ('available','unavailable')),
    run_id VARCHAR NOT NULL REFERENCES npv_ingestion_runs(run_id),
    first_retrieved_at TIMESTAMP_TZ NOT NULL,
    last_checked_at TIMESTAMP_TZ NOT NULL,
    CHECK ((status = 'available' AND value IS NOT NULL) OR (status = 'unavailable' AND value IS NULL)),
    PRIMARY KEY (indicator_id, geography, period, revision)
);
CREATE TABLE IF NOT EXISTS npv_documents (
    document_id VARCHAR PRIMARY KEY,
    source_id VARCHAR NOT NULL REFERENCES npv_sources(source_id),
    title VARCHAR NOT NULL,
    published_on DATE_ISO,
    registered_at TIMESTAMP_TZ NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00','now')),
    original_locator VARCHAR NOT NULL,
    content_hash VARCHAR NOT NULL,
    byte_count BIGINT NOT NULL CHECK (byte_count > 0),
    supersedes_document_id VARCHAR REFERENCES npv_documents(document_id),
    UNIQUE (source_id, content_hash)
);
CREATE VIEW IF NOT EXISTS npv_current_observations AS
SELECT indicator_id, geography, period, revision, value, status, run_id,
       first_retrieved_at, last_checked_at
FROM (
    SELECT *, row_number() OVER (
        PARTITION BY indicator_id, geography, period ORDER BY revision DESC
    ) AS position
    FROM npv_observations
) WHERE position = 1;
INSERT INTO npv_schema_versions(version) VALUES (1) ON CONFLICT DO NOTHING;
