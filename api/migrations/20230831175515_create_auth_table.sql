-- migrate:up
CREATE TABLE `auth` (
    `id` INT AUTO_INCREMENT,
    `username` VARCHAR(60) NOT NULL UNIQUE,
    `password` VARCHAR(130) NOT NULL,
    `role` ENUM('admin', 'user', 'mod') NOT NULL DEFAULT 'user',
    `active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME NOT NULL DEFAULT NOW(),
    `updated_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id)
);

INSERT INTO `auth` (`username`, `password`, `role`) VALUES
(
    'admin',
    '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
    'admin'
);
INSERT INTO `auth` (`username`, `password`) VALUES
(
    'user',
    '04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb'
);

-- migrate:down
SET FOREIGN_KEY_CHECKS = 0; -- to disable them
DROP TABLE IF EXISTS `auth`;
SET FOREIGN_KEY_CHECKS = 1; -- to re-enable them
