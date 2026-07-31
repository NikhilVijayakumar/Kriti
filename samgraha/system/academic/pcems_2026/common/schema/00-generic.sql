CREATE TABLE IF NOT EXISTS domain (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard TEXT NOT NULL,
    key TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    description TEXT NOT NULL DEFAULT '',
    UNIQUE(standard, key)
);

CREATE TABLE IF NOT EXISTS script (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard TEXT NOT NULL,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    purpose TEXT NOT NULL DEFAULT '',
    UNIQUE(standard, name)
);

CREATE TABLE IF NOT EXISTS prompt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard TEXT NOT NULL,
    name TEXT NOT NULL,
    content TEXT NOT NULL DEFAULT '',
    purpose TEXT NOT NULL DEFAULT '',
    UNIQUE(standard, name)
);

CREATE TABLE IF NOT EXISTS usecase (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    domain_id INTEGER REFERENCES domain(id),
    UNIQUE(standard, name)
);

CREATE TABLE IF NOT EXISTS step (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usecase_id INTEGER NOT NULL REFERENCES usecase(id),
    step_order INTEGER NOT NULL,
    kind TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    UNIQUE(usecase_id, step_order)
);

CREATE TABLE IF NOT EXISTS step_script (
    step_id INTEGER NOT NULL REFERENCES step(id),
    script_id INTEGER NOT NULL REFERENCES script(id),
    PRIMARY KEY (step_id, script_id)
);

CREATE TABLE IF NOT EXISTS step_prompt (
    step_id INTEGER NOT NULL REFERENCES step(id),
    prompt_id INTEGER NOT NULL REFERENCES prompt(id),
    PRIMARY KEY (step_id, prompt_id)
);
