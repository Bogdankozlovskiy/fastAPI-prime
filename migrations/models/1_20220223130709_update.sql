-- upgrade --
ALTER TABLE "item" ADD "number" INT NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "item" DROP COLUMN "number";
