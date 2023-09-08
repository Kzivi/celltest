-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 08 Wrz 2023, 07:13
-- Wersja serwera: 10.4.27-MariaDB
-- Wersja PHP: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `erp`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `celltest`
--

CREATE TABLE `celltest` (
  `number` int(10) UNSIGNED NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `serial` varchar(20) NOT NULL DEFAULT 'none',
  `type` varchar(20) NOT NULL DEFAULT '18650',
  `voltage` decimal(10,4) DEFAULT NULL,
  `impedance` decimal(10,4) DEFAULT NULL,
  `result` tinyint(1) NOT NULL,
  `user` varchar(30) DEFAULT NULL,
  `s_pos` text DEFAULT NULL,
  `p_pos` text DEFAULT NULL,
  `b_sn` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `celltest`
--
ALTER TABLE `celltest`
  ADD PRIMARY KEY (`number`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `celltest`
--
ALTER TABLE `celltest`
  MODIFY `number` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
