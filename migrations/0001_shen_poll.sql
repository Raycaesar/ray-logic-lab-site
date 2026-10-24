-- D1 / SQLite: one current response per random browser UUID.
-- Warning: browser UUIDs can be reset or fabricated; this is not one human = one vote.
CREATE TABLE IF NOT EXISTS shen_poll_votes (
  voter_id TEXT PRIMARY KEY NOT NULL,
  choice TEXT NOT NULL CHECK(choice IN ('A','B','C','D')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS shen_poll_votes_choice_idx ON shen_poll_votes(choice);
