-- migrate:up
CREATE TABLE `notifications` (
    `id` int AUTO_INCREMENT,
    `title` varchar(60) NOT NULL UNIQUE,
    `message` text NOT NULL,
    `ack` tinyint(1) NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT NOW (),
    `target_user_id` int,
    PRIMARY KEY (id),
    FOREIGN KEY (target_user_id) REFERENCES auth (id)
);

INSERT INTO `bookings`.`notifications` (`title`, `message`, `target_user_id`)
VALUES ('This is a test!', 'Test notification. With a rly long text :D', 1);

-- migrate:down
SET FOREIGN_KEY_CHECKS = 0; -- to disable them
DROP TABLE IF EXISTS `notifications`;
SET FOREIGN_KEY_CHECKS = 1; -- to re-enable them
