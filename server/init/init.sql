CREATE DATABASE IF NOT EXISTS `os-worksheet-3`;
USE `os-worksheet-3`;

CREATE TABLE IF NOT EXISTS `periodic_report` (
  `time` int(11) NOT NULL,
  `accel_x` int(11) NOT NULL,
  `accel_y` int(11) NOT NULL,
  `accel_z` int(11) NOT NULL,
  `temp` int(11) NOT NULL,
  `light_level` int(11) NOT NULL,
  `touch_pin0` bit(1) NOT NULL,
  `touch_pin1` bit(1) NOT NULL,
  `touch_pin2` bit(1) NOT NULL,
  PRIMARY KEY (`time`),
  UNIQUE KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

