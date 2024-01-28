-- Create the taskdb database
CREATE DATABASE IF NOT EXISTS taskdb;

-- Switch to the taskdb database
USE taskdb;

-- Create the tasks table
CREATE TABLE IF NOT EXISTS tasks (
    task_name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    PRIMARY KEY (task_name, date, time)
);
