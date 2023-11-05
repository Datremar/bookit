-- migrate:up
-- noqa: disable=all
CREATE TRIGGER set_default_expire_token_date
BEFORE INSERT ON token
FOR EACH ROW
BEGIN
    IF NEW.expire_date IS NULL THEN
        SET NEW.expire_date = NOW() + INTERVAL 3 DAY;
    END IF;
END;

-- migrate:down
SET FOREIGN_KEY_CHECKS=0; -- to disable them
DROP TRIGGER IF EXISTS set_default_expire_date;
SET FOREIGN_KEY_CHECKS=1; -- to re-enable them
