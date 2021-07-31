-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Φιλοξενητής: 127.0.0.1
-- Χρόνος δημιουργίας: 25 Φεβ 2021 στις 23:19:52
-- Έκδοση διακομιστή: 10.4.17-MariaDB
-- Έκδοση PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `chargeevolution`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `providers`
--

CREATE TABLE `providers` (
  `provider_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `providers`
--

INSERT INTO `providers` (`provider_id`, `title`) VALUES
(1, 'Schaefer, Durgan and Rau'),
(2, 'Graham, Herman and Strosin'),
(3, 'Champlin-Klein'),
(4, 'Mueller Group'),
(5, 'Kuhlman Inc'),
(6, 'Price, Koepp and Mueller'),
(7, 'Metz, Swaniawski and Wisoky'),
(8, 'Greenholt Inc'),
(9, 'Kris, Kautzer and Kirlin'),
(10, 'Hegmann LLC'),
(11, 'Schmeler Group'),
(12, 'Beatty, Friesen and Bode'),
(13, 'Ritchie Group'),
(14, 'Hahn, Denesik and Harvey'),
(15, 'Shields Inc'),
(16, 'Rowe-Stark'),
(17, 'Keebler, Schmidt and Toy'),
(18, 'Okuneva-Fisher'),
(19, 'Harvey Group'),
(20, 'Gislason, Leannon and DuBuque'),
(21, 'Dietrich-Hodkiewicz'),
(22, 'Abshire LLC'),
(23, 'Cremin, Medhurst and Hyatt'),
(24, 'Gibson, Dicki and O\'Reilly'),
(25, 'Goyette-Flatley'),
(26, 'Larson LLC'),
(27, 'Parker LLC'),
(28, 'Walter-Heller'),
(29, 'Wintheiser Inc'),
(30, 'Moore-Zieme'),
(31, 'Koepp, Erdman and Wilderman'),
(32, 'Ondricka Inc'),
(33, 'Corwin-Rohan'),
(34, 'Orn LLC'),
(35, 'Prohaska-Armstrong'),
(36, 'Armstrong-Robel'),
(37, 'Cartwright, Hartmann and Bednar'),
(38, 'Parker-Balistreri'),
(39, 'Kemmer and Sons'),
(40, 'Conn, Reichel and Kemmer'),
(41, 'Gutmann-Batz'),
(42, 'Murazik Group'),
(43, 'Witting, Carter and Smitham'),
(44, 'Padberg-Koch'),
(45, 'Zemlak-Stehr'),
(46, 'Ondricka Group'),
(47, 'Moore Inc'),
(48, 'Krajcik Inc'),
(49, 'Nader-Dooley'),
(50, 'Hessel-Fay'),
(51, 'Leannon and Sons'),
(52, 'Cole-Tremblay'),
(53, 'Dibbert, Lesch and Pfeffer'),
(54, 'Heidenreich-Leuschke'),
(55, 'Leffler, Heathcote and Greenholt'),
(56, 'Wehner Inc'),
(57, 'Jacobi Group'),
(58, 'Larson, Fadel and Fadel'),
(59, 'Beer, Harvey and Hammes'),
(60, 'Wiegand and Sons'),
(61, 'Weimann-Dooley'),
(62, 'Friesen, Blick and Smith'),
(63, 'Graham, Abshire and Runte'),
(64, 'Reinger-Okuneva'),
(65, 'Jones-Paucek'),
(66, 'McLaughlin-Rogahn'),
(67, 'Weissnat-Casper'),
(68, 'Nikolaus-Schultz'),
(69, 'Abbott and Sons'),
(70, 'Purdy, Cartwright and Sipes'),
(71, 'Borer, Hilpert and Miller'),
(72, 'Hirthe, Brakus and Larson'),
(73, 'Will, Welch and Nicolas'),
(74, 'Johnston LLC'),
(75, 'Champlin-Dibbert'),
(76, 'Cremin, Cremin and Gerhold'),
(77, 'Predovic-O\'Connell'),
(78, 'Nader and Sons'),
(79, 'Ebert Inc'),
(80, 'Brown-Grant'),
(81, 'Torphy, Barrows and Murazik'),
(82, 'Sauer Inc'),
(83, 'Turcotte, Fahey and Padberg'),
(84, 'Skiles-O\'Hara'),
(85, 'Treutel-Hackett'),
(86, 'Mohr-Miller'),
(87, 'Dietrich, Bernier and White'),
(88, 'Rolfson, Jast and Wiza'),
(89, 'Gutkowski-Johnson'),
(90, 'Rutherford-O\'Connell'),
(91, 'Von and Sons'),
(92, 'O\'Kon and Sons'),
(93, 'Greenfelder LLC'),
(94, 'Tromp-Kassulke'),
(95, 'Langworth-Boyer'),
(96, 'Bruen and Sons'),
(97, 'Okuneva and Sons'),
(98, 'Green, Oberbrunner and Hirthe'),
(99, 'Swift, Hermiston and Renner'),
(100, 'Hayes-Ledner');

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `providers`
--
ALTER TABLE `providers`
  ADD PRIMARY KEY (`provider_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
