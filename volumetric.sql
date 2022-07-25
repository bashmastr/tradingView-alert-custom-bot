-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 25, 2022 at 07:08 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `telegram_bot`
--

-- --------------------------------------------------------

--
-- Table structure for table `volumetric`
--

CREATE TABLE `volumetric` (
  `ID` int(255) NOT NULL,
  `TICKER` varchar(255) NOT NULL,
  `REMARKS` text NOT NULL,
  `CURRENTPRICE` varchar(255) NOT NULL,
  `VOLUME` varchar(255) NOT NULL,
  `TIMEFRAME` varchar(255) NOT NULL,
  `TIME` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `volumetric`
--

INSERT INTO `volumetric` (`ID`, `TICKER`, `REMARKS`, `CURRENTPRICE`, `VOLUME`, `TIMEFRAME`, `TIME`) VALUES
(1, 'UU21SDT', '4/5 check ltf volume', '0.1215', '12917005', 'Dsdf', '2029-08-13 12:12:20'),
(2, 'UU21SDT', '4/5 check ltf volume', '0.1215', '12917005', 'Dsdf', '2029-08-13 12:12:20'),
(3, 'UU21SDT', '4/5 check ltf volume', '0.1215', '12917005', 'Dsdf', '2029-08-13 12:14:20'),
(4, 'UU21SDT', '4/5 check ltf volume', '0.1215', '12917005', 'Dsdf', '2029-08-13 12:15:20');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `volumetric`
--
ALTER TABLE `volumetric`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `volumetric`
--
ALTER TABLE `volumetric`
  MODIFY `ID` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
