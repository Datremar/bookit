-- migrate:up
CREATE TABLE `timesheets` (
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR(60) NOT NULL,
    `timesheet` TEXT NOT NULL,
    `type` ENUM('busy', 'free') NOT NULL DEFAULT 'busy',
    `active` TINYINT(1) NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT NOW(),
    `updated_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id)
);


INSERT INTO `timesheets` (`name`, `timesheet`, `active`) VALUES
('TS1', '{"moday": [{"from": "09:00", "to": "12:00"},{"from": "13:00", "to": "17:00"}],"Tuesday": [{"from": "09:00", "to": "12:00"},{"from": "13:00", "to": "17:00"}],"Wednesday": [{"from": "09:00", "to": "12:00"},{"from": "13:00", "to": "17:00"}],"Thursday": [{"from": "09:00", "to": "12:00"},{"from": "13:00", "to": "17:00"}],"Friday": [{"from": "09:00", "to": "12:00"},{"from": "13:00", "to": "17:00"}],"Saturday": [],"Sunday": []}', 1); -- noqa: disable=LT05

-- migrate:down
SET FOREIGN_KEY_CHECKS = 0; -- to disable them
DROP TABLE IF EXISTS `timesheets`;
SET FOREIGN_KEY_CHECKS = 1; -- to re-enable them
