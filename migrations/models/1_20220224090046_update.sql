-- upgrade --
CREATE UNIQUE INDEX "uid_user_email_1b4f1c" ON "user" ("email");
CREATE UNIQUE INDEX "uid_user_usernam_9987ab" ON "user" ("username");
-- downgrade --
DROP INDEX "idx_user_usernam_9987ab";
DROP INDEX "idx_user_email_1b4f1c";
