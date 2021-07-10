-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 10, 2021 at 07:01 AM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `health`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE `appointment` (
  `id` int(11) NOT NULL,
  `sid` int(11) NOT NULL,
  `date` varchar(255) NOT NULL,
  `status` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`id`, `sid`, `date`, `status`) VALUES
(1, 2, '2021-06-30', 2),
(2, 2, '2021-07-03', 1),
(3, 1, '2021-06-29', 2),
(4, 2, '2021-07-06', 2),
(5, 2, '2021-07-05', 0),
(6, 8, '2021-07-07', 0);

-- --------------------------------------------------------

--
-- Table structure for table `consult`
--

CREATE TABLE `consult` (
  `aid` int(11) NOT NULL,
  `sid` int(11) NOT NULL,
  `text` text NOT NULL,
  `report` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sdetails`
--

CREATE TABLE `sdetails` (
  `id` int(11) NOT NULL,
  `height` varchar(255) NOT NULL,
  `weight` varchar(255) NOT NULL,
  `allergy` text NOT NULL,
  `disease` text NOT NULL,
  `emergency` varchar(255) NOT NULL,
  `bloodgroup` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sdetails`
--

INSERT INTO `sdetails` (`id`, `height`, `weight`, `allergy`, `disease`, `emergency`, `bloodgroup`) VALUES
(2, '5\'5\"', '22', 'dust', 'na', '2582582582', 'A+'),
(1, '5\'5\"', '22', 'dust', 'na', '2582582582', 'A+'),
(9, '5\'5\"', '22', 'dust', 'na', '2582582582', 'A+'),
(10, '5\'5\"', '22', 'dust', 'na', '2582582582', 'A+'),
(11, '5\'5\"', '22', 'dust', 'na', '258258', 'A+'),
(6, '5\'5\'\'', '50', 'dust', 'na', '', 'A+');

-- --------------------------------------------------------

--
-- Table structure for table `slots`
--

CREATE TABLE `slots` (
  `date` varchar(255) NOT NULL,
  `slots` int(11) NOT NULL DEFAULT 10
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `slots`
--

INSERT INTO `slots` (`date`, `slots`) VALUES
('2021-06-29', 9),
('2021-06-30', 8),
('2021-07-01', 10),
('2021-07-02', 10),
('2021-07-03', 8),
('2021-07-04', 10),
('2021-07-05', 9),
('2021-07-06', 9),
('2021-07-07', 9),
('2021-07-08', 10),
('2021-07-09', 10),
('2021-07-10', 10),
('2021-07-11', 10),
('2021-07-12', 10);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `enroll` varchar(255) NOT NULL,
  `number` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `enroll`, `number`, `email`, `password`) VALUES
(2, 'ABC Patel', '180280BIT', '9898989899', 'abc@abc.com', 'abcabc'),
(3, 'Admin', 'B12345', '1234567890', 'admin@admin.com', 'admin@admin\r\n'),
(5, 'a', 'a123', '123', 'a@a.com', 'aaa'),
(6, 'd', '180280', '9898989899', 'd@d.com', 'dD1ddddd'),
(7, 's', '180280', '123', 's@s.com', 'sS1sssss'),
(8, 'm', '180280', '9898989899', 'm@m.com', 'mM1mmmmm'),
(11, 'X', '180280', '9898989899', 'thisisforpod@gmail.com', 'Thisis4pod');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointment`
--
ALTER TABLE `appointment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointment`
--
ALTER TABLE `appointment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
