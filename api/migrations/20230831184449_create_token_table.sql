-- migrate:up
CREATE TABLE token (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    token VARCHAR(255) NOT NULL,
    expire_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES auth(id)
);

-- migrate:down
SET FOREIGN_KEY_CHECKS=0; -- to disable them
DROP TABLE IF EXISTS token;
SET FOREIGN_KEY_CHECKS=1; -- to re-enable them
