-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Φιλοξενητής: 127.0.0.1
-- Χρόνος δημιουργίας: 13 Μαρ 2021 στις 20:21:38
-- Έκδοση διακομιστή: 10.4.17-MariaDB
-- Έκδοση PHP: 8.0.2

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
-- Δομή πίνακα για τον πίνακα `vehicles`
--

CREATE TABLE `vehicles` (
  `id` varchar(36) NOT NULL,
  `brand` varchar(13) DEFAULT NULL,
  `type` varchar(4) DEFAULT NULL,
  `brand_id` varchar(36) DEFAULT NULL,
  `model` varchar(22) DEFAULT NULL,
  `release_year` varchar(4) DEFAULT NULL,
  `variant` varchar(17) DEFAULT NULL,
  `usable_battery_size` float(4,1) DEFAULT NULL,
  `ac_charger_ports_0` varchar(5) DEFAULT NULL,
  `ac_charger_ports_1` varchar(5) DEFAULT NULL,
  `ac_charger_usable_phases` int(1) DEFAULT NULL,
  `dc_charger_0` varchar(7) DEFAULT NULL,
  `dc_charger_1` varchar(9) DEFAULT NULL,
  `dc_charger_2` varchar(9) DEFAULT NULL,
  `energy_consumption` float(3,1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `vehicles`
--

INSERT INTO `vehicles` (`id`, `brand`, `type`, `brand_id`, `model`, `release_year`, `variant`, `usable_battery_size`, `ac_charger_ports_0`, `ac_charger_ports_1`, `ac_charger_usable_phases`, `dc_charger_0`, `dc_charger_1`, `dc_charger_2`, `energy_consumption`) VALUES
('059c028d-b2a6-4a8d-947a-158c7537b290', 'Audi', 'bev', '89c2668c-0c50-4344-9386-93e4000f7673', 'e-tron 50', '2019', '22kW-AC', 86.8, 'type2', '', 3, 'ccs', '', '', 22.7),
('09022e0a-c322-46e7-9171-b48fdd953cca', 'Peugeot', 'phev', 'f458fe7d-f545-45f3-8c23-2ab8140b8b5d', '3008', '2020', 'HYbrid4 3,7 kW-AC', 64.5, 'type1', '', 1, '', '', '', 15.2),
('0a663bbf-3b87-4e7a-bd7a-3e9c39961a2b', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model S', '', '85', 86.3, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 19.1),
('0a7e79c1-ecd6-4639-bac1-9c9e49fec84c', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'ID.3', '2020', 'Standard Range', 57.9, 'type2', '', 2, 'ccs', '', '', 16.4),
('0aa5220a-6da7-4dc0-a0a1-714bea4fded3', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model X', '2017', 'P100D', 74.3, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 22.0),
('0ec3f440-136c-49f1-8917-c629a27146c7', 'BMW', 'bev', '0742668c-bf59-4191-890e-2b0883508808', 'i3', '', '94 Ah', 53.4, 'type2', '', 3, 'ccs', '', '', 16.0),
('0f7eae0b-43be-48f8-b4a0-1a8266fd07a9', 'Kia', 'bev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'e-Niro', '2018', '64 kWh', 67.1, 'type2', '', 1, 'ccs', '', '', 17.3),
('15023eb9-eba6-436e-ad98-2086f1cb31c4', 'Volkswagen', 'phev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'Golf GTE', '2017', '', 67.2, 'type2', '', 1, '', '', '', 11.4),
('176af738-f385-4dc8-9243-9c701fbd7759', 'Mazda', 'bev', '9b829849-1219-48b8-964e-90ddc1a4fa85', 'MX-30', '2020', '', 76.6, 'type2', '', 1, 'ccs', '', '', 17.8),
('1847e3aa-750c-4b12-a80a-56e792b3aadb', 'Mitsubishi', 'phev', '3cf8cf51-60ac-4cac-9f25-131c21eda12e', 'Outlander PHEV', '2018', '', 65.2, 'type1', '', 1, 'chademo', '', '', 15.2),
('18bb40bd-321b-4326-a404-e46652538830', 'Skoda', 'bev', '43763587-6999-406b-8843-28977e1b82c3', 'Enyaq iV', '2020', '82 kWh 50 kW-DC', 58.1, 'type2', '', 3, 'ccs', '', '', 19.0),
('1b3105fa-527a-491f-ac26-5bfa94bfa45d', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model X', '2019', '75D', 74.4, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 20.0),
('1c13fba9-2c09-4be1-b5c6-aecd2b253afb', 'Renault', 'bev', 'c0d8a60c-34b8-44fe-8af7-9eeb62eedb4b', 'Kangoo ZE', '', '', 60.4, 'type2', '', 1, '', '', '', 19.4),
('1c9126d4-24d6-4e9f-a49d-15813fa49728', 'Artega', 'bev', '97d0d03a-63c6-4f33-99d7-6e944f71d7c5', 'Karo', '2020', 'Range Plus', 86.9, 'type2', '', 1, '', '', '', 7.2),
('1cec7821-632f-4f17-8a58-644b6ab23f44', 'Opel', 'bev', '3500fb3e-bd2c-478e-ae5e-ac9ee490594b', 'Corsa-e', '2020', '7,2 kW-AC', 51.2, 'type2', '', 1, 'ccs', '', '', 16.4),
('1d43c981-02be-4d41-a34b-65a40ff25f7b', 'smart', 'bev', 'a462c115-33b4-438b-b590-bc4a33382d1c', 'fortwo EQ', '', '', 74.5, 'type2', '', 1, '', '', '', 16.7),
('1e8c0cc5-20db-491f-9242-12cf3bc7b962', 'Mercedes Benz', 'phev', 'b2282fbe-f5d9-48d9-943f-a9b66ec51423', 'A 250 e', '2020', '7,4 kW-AC + DC', 60.6, 'type2', '', 2, 'ccs', '', '', 15.0),
('22f521ce-42ca-40d7-bfdb-5d33b1bd9cbe', 'Fiat', 'bev', '3291e5ba-862c-49fa-8437-71105743875e', '500e', '2020', '', 76.0, 'type2', '', 3, 'ccs', '', '', 16.8),
('2644bfd3-a593-4276-bb1f-c8965e33797e', 'Nissan', 'bev', 'dab5a47a-e8ce-4d34-9139-0701499205b1', 'e-NV 200', '', '24 kWh 6,6 kW-AC', 74.7, 'type1', '', 1, 'chademo', '', '', 20.0),
('27d7610e-9a77-498a-b1b5-28d4bc92cbf2', 'Audi', 'bev', '89c2668c-0c50-4344-9386-93e4000f7673', 'e-tron 55', '2019', '22kW-AC', 97.7, 'type2', '', 3, 'ccs', '', '', 23.4),
('28b61ff5-734a-412e-9241-dec4c27d1a38', 'Peugeot', 'bev', 'f458fe7d-f545-45f3-8c23-2ab8140b8b5d', 'I-on', '', '', 96.1, 'type1', '', 1, 'chademo', '', '', 12.9),
('2ae110f8-8906-4b03-b4bc-83e5577c1cc1', 'Maxus', 'bev', '171a1e6d-8cbc-41a9-a8bb-e05b7ee98889', 'EV80', '2018', '', 94.1, 'type2', '', 2, 'ccs', '', '', 35.0),
('2c7abcf4-0ba0-4feb-9e9b-b47661072feb', 'Mitsubishi', 'bev', '3cf8cf51-60ac-4cac-9f25-131c21eda12e', 'i-Miev', '', '', 67.6, 'type1', '', 1, 'chademo', '', '', 12.9),
('2eea1ef2-0fd1-481d-adee-68044666614e', 'Seat', 'bev', '91c527ff-aa74-4dbb-9091-36fb5ddd44b6', 'Mii Electric', '2020', 'CCS', 61.8, 'type2', '', 2, 'ccs', '', '', 16.6),
('2f2b159b-9b03-450f-9818-c139323d1735', 'Fiat', 'bev', '3291e5ba-862c-49fa-8437-71105743875e', '500e', '2014', '', 50.1, 'type1', '', 1, '', '', '', 18.0),
('3038b11b-2dfc-4f9f-b22c-4bfdc08d0c4b', 'Hyundai', 'bev', '9771afb8-9e25-4ae6-a5b3-b2a5b9f363f0', 'Ioniq', '2019', '', 68.7, 'type2', '', 1, 'ccs', '', '', 15.3),
('32922583-e434-4ed2-afc1-4d8fde67aeda', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model S', '', '90', 91.1, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 18.2),
('34b5ef32-efea-48fc-8386-3800d0b737f0', 'Porsche', 'bev', '68e11a25-d316-4d22-9444-45c7306c8ab7', 'Taycan', '2020', '4S', 61.8, 'type2', '', 3, 'ccs', '', '', 19.5),
('355eadbb-0c97-4a66-993d-8fdc61a77ef5', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model X', '2019', 'Performance', 100.0, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 22.0),
('3667752d-17a5-4166-abaf-dcf227948bfd', 'Hyundai', 'phev', '9771afb8-9e25-4ae6-a5b3-b2a5b9f363f0', 'Ioniq', '2016', 'PHEV', 61.3, 'type2', '', 1, '', '', '', 15.4),
('3b5bb8d1-0f34-4c05-861c-45d19a8883b9', 'DS', 'bev', '37bfdacf-1aca-4eb7-8daa-8dc5b14c59e9', '3 Crossback E-Tense', '2020', '7,2 kW-AC', 75.1, 'type2', '', 1, 'ccs', '', '', 18.4),
('3b649ae3-935b-425b-b5d6-75c549b96d40', 'Nissan', 'bev', 'dab5a47a-e8ce-4d34-9139-0701499205b1', 'Leaf', '2011', '24 kWh 6,6 kW-AC', 81.8, 'type1', '', 1, 'chademo', '', '', 16.9),
('3c933da2-1fa1-4094-825a-a181610dbfd0', 'Kia', 'bev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'e-Soul', '2019', '64 kWh', 50.1, 'type2', '', 1, 'ccs', '', '', 17.5),
('41c9d96c-6a19-4db0-ba3a-931ab99c6f15', 'Skoda', 'phev', '43763587-6999-406b-8843-28977e1b82c3', 'Superb iV', '2020', 'PHEV', 60.2, 'type2', '', 1, '', '', '', 14.0),
('430ca2cd-bd4b-482a-8776-85a8c7d3435c', 'DS', 'bev', '37bfdacf-1aca-4eb7-8daa-8dc5b14c59e9', '3 Crossback E-Tense', '2020', '11 kW-AC', 81.1, 'type2', '', 3, 'ccs', '', '', 18.4),
('45b68c71-cd11-4bd7-a03f-fdaae259635d', 'Citroen', 'bev', '3b3fc191-f4c3-45da-bc3b-21efbe1b264f', 'C-Zero', '', '', 64.7, 'type1', '', 1, 'chademo', '', '', 17.1),
('46240342-6f7e-4767-b66d-3234ba874a30', 'Mercedes Benz', 'phev', 'b2282fbe-f5d9-48d9-943f-a9b66ec51423', 'A 250 e', '2020', '7,4 kW-AC', 85.6, 'type2', '', 2, '', '', '', 15.0),
('4c04db3b-c493-4b90-9859-21b7304a4ffc', 'Porsche', 'bev', '68e11a25-d316-4d22-9444-45c7306c8ab7', 'Taycan', '2020', 'Turbo S', 60.4, 'type2', '', 3, 'ccs', '', '', 22.3),
('4dc6b014-8612-4fa7-bb34-9ea4d7fa5220', 'Skoda', 'bev', '43763587-6999-406b-8843-28977e1b82c3', 'Enyaq iV', '2020', '62 kWh 50 kW-DC', 56.6, 'type2', '', 3, 'ccs', '', '', 18.7),
('4df1d4d6-f001-4d0a-b284-5ffc07e6ade2', 'BMW', 'phev', '0742668c-bf59-4191-890e-2b0883508808', 'X5', '2020', 'PHEV', 52.3, 'type2', '', 1, '', '', '', 21.3),
('4ea0fb0a-8d77-4a03-a147-5e962f8ea766', 'Ford', 'phev', '6cf9e9b6-28aa-44c7-b6c3-438d518ac12f', 'Kuga', '2020', 'PHEV', 73.0, 'type2', '', 1, '', '', '', 19.0),
('4f408d10-82c3-4850-ae2b-141f21d745b3', 'e.GO Mobile', 'bev', '771bb157-23a2-4917-908c-810d241718d5', 'Life 40', '2019', '', 75.7, 'type2', '', 1, '', '', '', 15.5),
('5335d545-cfeb-4bca-bb11-cf0966f1b5ca', 'Mercedes Benz', 'bev', 'b2282fbe-f5d9-48d9-943f-a9b66ec51423', 'EQC', '2019', '', 92.7, 'type2', '', 2, 'ccs', '', '', 21.6),
('55ac0aaf-6bae-4a8e-ba50-4a9a7ab5b4af', 'Skoda', 'bev', '43763587-6999-406b-8843-28977e1b82c3', 'Enyaq iV', '2020', '62 kWh 100 kW-DC', 86.6, 'type2', '', 3, 'ccs', '', '', 18.7),
('57184038-ae77-4540-9367-ccb98beb8cc3', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'e-up', '2020', '', 63.7, 'type2', '', 2, '', '', '', 16.6),
('58661a4c-e1f9-4dc2-8d09-3bb42be62554', 'Kia', 'bev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'e-Soul', '2019', '39 kWh', 78.3, 'type2', '', 1, 'ccs', '', '', 17.0),
('5bfa9a87-7b35-4e3a-bd3f-dc2ac55e184b', 'Honda', 'bev', '9ca5e092-76e2-4868-afc1-c06abeedf81b', 'e', '2020', '', 55.8, 'type2', '', 1, 'ccs', '', '', 16.0),
('5e1746c9-56a2-4fb9-8a76-b75c95a037ee', 'Kia', 'bev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'Soul', '', '30 kWh', 51.9, 'type2', '', 1, 'chademo', '', '', 17.6),
('6033b26c-1b3c-441b-9f78-7b7cd5512051', 'Aiways', 'bev', 'a43d2607-eead-46c2-9fd5-2ebd3c49d895', 'U5', '2020', '', 84.3, 'type2', '', 1, 'ccs', '', '', 18.8),
('66cb7bea-24b7-458f-ae3e-11d4a852568b', 'Kia', 'bev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'e-Niro', '2018', '39 kWh', 82.6, 'type2', '', 1, 'ccs', '', '', 16.3),
('68cbedff-8994-4b77-bfb5-6aa22962e3a2', 'Kia', 'bev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'e-Niro', '2020', '64 kWh', 61.4, 'type2', '', 3, 'ccs', '', '', 17.3),
('6990914a-6a0d-49d4-87f5-ee86ee33344c', 'Porsche', 'bev', '68e11a25-d316-4d22-9444-45c7306c8ab7', 'Taycan', '2020', '4S Plus', 94.7, 'type2', '', 3, 'ccs', '', '', 19.7),
('6a3a76f6-a0d0-41ff-afc9-5ad2f0879b4d', 'smart', 'bev', 'a462c115-33b4-438b-b590-bc4a33382d1c', 'forfour EQ', '', '', 60.7, 'type2', '', 1, '', '', '', 17.6),
('6a4c5e58-d1cb-49ad-a1cf-c0025fb7246f', 'Chevrolet', 'bev', 'cbca5847-9b23-47d9-80d3-24fa9a8ca21a', 'Spark EV', '2015', '19 kWh', 53.9, 'type1', '', 1, 'ccs', '', '', 14.0),
('6cc437e9-b842-4c1b-9c08-9ca2d46d22a9', 'Hyundai', 'bev', '9771afb8-9e25-4ae6-a5b3-b2a5b9f363f0', 'Kona', '2018', '39 kWh', 85.5, 'type2', '', 1, 'ccs', '', '', 15.4),
('6cd5ba89-6523-4bca-9423-ea92227a8b8d', 'Ford', 'bev', '6cf9e9b6-28aa-44c7-b6c3-438d518ac12f', 'Focus electric', '2013', '', 78.2, 'type2', '', 1, '', '', '', 16.4),
('6f96c616-e87a-4958-bbe7-b4278be00170', 'Opel', 'bev', '3500fb3e-bd2c-478e-ae5e-ac9ee490594b', 'Corsa-e', '2020', '11 kW-AC', 100.0, 'type2', '', 3, 'ccs', '', '', 16.4),
('6fa12374-6162-451e-8464-5e0e73091839', 'Renault', 'phev', 'c0d8a60c-34b8-44fe-8af7-9eeb62eedb4b', 'Captur E-Tech', '2020', 'PHEV', 82.7, 'type2', '', 1, '', '', '', 17.4),
('71cc8552-391f-49b0-b106-2202fa222161', 'Mercedes Benz', 'bev', 'b2282fbe-f5d9-48d9-943f-a9b66ec51423', 'B-Klasse', '', '', 58.3, 'type2', '', 3, '', '', '', 16.6),
('72695d36-29c4-4726-8ca8-5333fb3f9865', 'Peugeot', 'bev', 'f458fe7d-f545-45f3-8c23-2ab8140b8b5d', 'e-2008', '2020', '7,2 kW-AC', 85.4, 'type2', '', 1, 'ccs', '', '', 18.0),
('737441e8-6b5f-4185-9b0b-e51585ab6ea8', 'Renault', 'bev', 'c0d8a60c-34b8-44fe-8af7-9eeb62eedb4b', 'Zoe', '2017', 'R 90', 74.2, 'type2', '', 3, '', '', '', 16.1),
('7490520f-fe11-4148-a9b6-3882f06ee082', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model X', '2017', '100D', 99.3, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 20.0),
('74f2c3a5-f78f-459a-823a-dfc0a21e5aeb', 'Nissan', 'bev', 'dab5a47a-e8ce-4d34-9139-0701499205b1', 'Leaf', '2015', '30 kWh 6,6 kW-AC', 72.7, 'type1', '', 1, 'chademo', '', '', 16.5),
('7508892b-e7e7-42ba-9cca-57753426cd86', 'Chevrolet', 'bev', 'cbca5847-9b23-47d9-80d3-24fa9a8ca21a', 'Spark EV', '2013', '21 kWh', 78.7, 'type1', '', 1, 'ccs', '', '', 16.0),
('77028f96-eb9b-4c65-b452-c92011b1fc1c', 'Nissan', 'bev', 'dab5a47a-e8ce-4d34-9139-0701499205b1', 'Leaf', '2017', '40 kWh', 81.1, 'type2', '', 1, 'chademo', '', '', 16.4),
('785c65be-3122-44ad-b574-9291c0793c37', 'smart', 'bev', 'a462c115-33b4-438b-b590-bc4a33382d1c', 'fortwo ED', '', '', 80.7, 'type2', '', 1, '', '', '', 16.7),
('78b14a0f-5c62-4885-95ef-2e3f81197260', 'Nissan', 'bev', 'dab5a47a-e8ce-4d34-9139-0701499205b1', 'Leaf', '2019', 'e+ 62 kWh', 68.6, 'type2', '', 1, 'chademo', '', '', 17.2),
('7ba60564-7eda-457b-b7d5-46dd1b15cc0e', 'Peugeot', 'phev', 'f458fe7d-f545-45f3-8c23-2ab8140b8b5d', '3008', '2020', 'HYbrid4 7,4 kW-AC', 70.7, 'type1', '', 1, '', '', '', 15.2),
('7dbad968-7058-4440-9c8f-8f483cdd973a', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model 3', '', 'Performance', 90.0, 'type2', '', 3, 'ccs', 'tesla_ccs', '', 16.7),
('7de25a64-e9fa-484f-bf99-d02b02cfb17d', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model 3', '', 'LR', 51.5, 'type2', '', 3, 'ccs', 'tesla_ccs', '', 16.1),
('7f4bf402-f8e2-47da-b456-30f1bdfce8ac', 'Opel', 'bev', '3500fb3e-bd2c-478e-ae5e-ac9ee490594b', 'Ampera e-Pionier', '2012', '', 83.0, 'type1', '', 1, '', '', '', 16.9),
('7f709186-39c3-420f-9caf-1fdb424f7953', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model S', '', '75', 93.7, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 18.5),
('805b5810-074c-449b-ad19-d6c852ebf8f6', 'smart', 'bev', 'a462c115-33b4-438b-b590-bc4a33382d1c', 'forfour EQ', '', '22 kW-AC', 70.1, 'type2', '', 3, '', '', '', 17.6),
('80e7ef22-27f8-4e93-8c86-7a6a0a227e5d', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model S', '', '70', 61.5, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 18.5),
('83ec0576-bfb8-400a-9af9-483b2684673c', 'Nissan', 'bev', 'dab5a47a-e8ce-4d34-9139-0701499205b1', 'Leaf', '2015', '30 kWh', 83.2, 'type1', '', 1, 'chademo', '', '', 16.5),
('84f2fcc1-cc73-4919-8d76-0f1ba8eaf685', 'Kia', 'phev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'XCeed', '2020', 'PHEV', 96.8, 'type2', '', 1, '', '', '', 11.3),
('86290f48-f554-4db5-bd35-4a8b7828689a', 'Nissan', 'bev', 'dab5a47a-e8ce-4d34-9139-0701499205b1', 'e-NV 200', '', '24 kWh', 90.2, 'type1', '', 1, 'chademo', '', '', 20.0),
('87e73c44-93ba-4687-877c-32a3aa940a09', 'Kia', 'bev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'e-Soul', '2020', '64 kWh 11 kW-AC', 89.0, 'type2', '', 3, 'ccs', '', '', 17.5),
('8b0195b6-5318-46d9-a6fd-1b5f75e8b495', 'MG', 'bev', '5663b87a-d940-4bab-9846-d74c8c0ae260', 'ZS EV', '2020', '', 93.0, 'type2', '', 1, 'ccs', '', '', 19.8),
('8b51a06f-676a-46aa-9074-4d3364ea1cca', 'Mercedes Benz', 'phev', 'b2282fbe-f5d9-48d9-943f-a9b66ec51423', 'GLE', '2020', '350 de/e', 50.9, 'type2', '', 1, 'ccs', '', '', 31.2),
('8cfce5f4-23b6-470a-87fa-a04095fe0334', 'Mini', 'phev', '6d9d9248-de4a-4b13-976b-4e9f6688b0b1', 'Countryman ALL4', '2019', '', 50.7, 'type2', '', 1, '', '', '', 13.2),
('8da12395-cf7a-4ccf-886f-e25ade426457', 'Jaguar', 'bev', '61fc79a2-04ca-418e-9333-caf5f67ba02f', 'i-Pace', '', '', 69.1, 'type2', '', 1, 'ccs', '', '', 23.2),
('8df35b23-dcc6-4590-83c7-5578da4c4809', 'Hyundai', 'bev', '9771afb8-9e25-4ae6-a5b3-b2a5b9f363f0', 'Kona', '2018', '64 kWh', 61.9, 'type2', '', 1, 'ccs', '', '', 15.8),
('8f6db2f5-1dd9-46f6-bb97-eba419dbaea4', 'Renault', 'bev', 'c0d8a60c-34b8-44fe-8af7-9eeb62eedb4b', 'Twizy', '', '', 90.8, 'type2', '', 1, '', '', '', 8.4),
('908e578f-f890-4716-93e8-7c0f75e46bb5', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model X', '2016', 'P90D', 59.9, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 21.0),
('926efa33-4c55-43df-80f3-4b8d2d65a00a', 'Peugeot', 'bev', 'f458fe7d-f545-45f3-8c23-2ab8140b8b5d', 'e-208', '2020', '7,2 kW-AC', 72.2, 'type2', '', 1, 'ccs', '', '', 16.1),
('92ffd46c-fe26-4805-81ba-fbadce4d524f', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model X', '2016', '60D', 85.8, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 16.0),
('93c82e06-1aa3-4c19-8f81-b9fac0c598c3', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model 3', '', 'SR+', 96.4, 'type2', '', 3, 'ccs', 'tesla_ccs', '', 15.3),
('9666138c-1d24-4fa8-9083-0ffba09ab1ef', 'Renault', 'bev', 'c0d8a60c-34b8-44fe-8af7-9eeb62eedb4b', 'Zoe', '2013', 'Q 210', 86.5, 'type2', '', 3, '', '', '', 15.5),
('975b064b-626e-4318-b60c-3ce0729743fd', 'e.GO Mobile', 'bev', '771bb157-23a2-4917-908c-810d241718d5', 'Life 20', '2019', '', 68.3, 'type2', '', 1, '', '', '', 15.5),
('98aacbc9-5a97-4fe4-abcf-4f7bb2910a9f', 'e.GO Mobile', 'bev', '771bb157-23a2-4917-908c-810d241718d5', 'Life 60', '2019', '', 91.1, 'type2', '', 1, '', '', '', 15.5),
('9d101a26-eaaa-4058-a251-5221b45ffd91', 'Peugeot', 'bev', 'f458fe7d-f545-45f3-8c23-2ab8140b8b5d', 'e-2008', '2020', '11 kW-AC', 64.8, 'type2', '', 3, 'ccs', '', '', 18.0),
('a0347619-a7fe-4dd2-be4e-3ef615783481', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'e-up', '2013', 'CCS', 90.7, 'type2', '', 1, 'ccs', '', '', 16.8),
('a12f033f-f2c2-44bd-b62c-7019898a72d0', 'Porsche', 'bev', '68e11a25-d316-4d22-9444-45c7306c8ab7', 'Taycan', '2020', 'Turbo ', 57.9, 'type2', '', 3, 'ccs', '', '', 21.5),
('a883bb35-270d-4f31-9169-ccf06ae3c0c5', 'Kia', 'phev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'Niro', '2020', 'PHEV', 74.8, 'type2', '', 1, '', '', '', 9.8),
('a9a177bf-9ce5-4b67-b3ef-51af248b48c2', 'Audi', 'bev', '89c2668c-0c50-4344-9386-93e4000f7673', 'e-tron 55', '2019', '', 97.4, 'type2', '', 3, 'ccs', '', '', 23.4),
('aa69b5e8-fc4e-40f8-8060-2c96248f62ef', 'Skoda', 'bev', '43763587-6999-406b-8843-28977e1b82c3', 'Enyaq iV', '2020', '82 kWh 125 kW-DC', 74.4, 'type2', '', 3, 'ccs', '', '', 19.0),
('ac812f08-3c8a-4af5-a07a-b520ec9e16cc', 'Volvo', 'phev', '2e55ea02-c829-4256-94fd-ffc971a1dd8e', 'XC 60 T8', '2018', '', 54.2, 'type2', '', 1, '', '', '', 24.5),
('add28704-7b59-474d-bfa6-2338e54ccaef', 'Kia', 'bev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'Soul', '', '27 kWh', 66.1, 'type2', '', 1, 'chademo', '', '', 17.6),
('b0da6660-c20e-40c3-9db7-0b19c478c6cb', 'Mercedes Benz', 'phev', 'b2282fbe-f5d9-48d9-943f-a9b66ec51423', 'GLC 300 de 4MATIC', '2020', 'PHEV', 68.3, 'type2', '', 1, '', '', '', 18.2),
('b3fd3e84-4dd4-4ac0-914f-3c3c582fc600', 'Renault', 'bev', 'c0d8a60c-34b8-44fe-8af7-9eeb62eedb4b', 'Zoe', '2015', 'R 240', 80.7, 'type2', '', 3, '', '', '', 15.5),
('b5aa307e-a6b9-46e7-939e-2dd525870c13', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model S', '', '100', 69.1, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 18.4),
('b7c4ddb8-4806-4328-a4e6-4abb4746016d', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model X', '2019', 'Standard Range', 87.6, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 20.0),
('b8a76fa8-97f1-4f27-8f9f-80f26df230d1', 'Chevrolet', 'bev', 'cbca5847-9b23-47d9-80d3-24fa9a8ca21a', 'Bolt', '2017', '60 kWh', 81.6, 'type1', 'type2', 2, 'ccs', '', '', 12.9),
('b97f749b-5361-4116-8103-c208dc601a0b', 'Kia', 'phev', '3337d5f0-39de-4ded-831b-843dfec1ebbd', 'Ceed SW', '2020', 'PHEV', 86.8, 'type2', '', 1, '', '', '', 11.3),
('bad55b90-4b4f-4760-83ea-fa96280e7310', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'e-Golf', '2017', '', 61.7, 'type2', '', 2, '', '', '', 16.4),
('bcd8700d-241c-43a1-b9df-24ee310ea8e4', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'e-up', '2013', '', 52.4, 'type2', '', 1, '', '', '', 16.8),
('c0a26929-1157-4fb4-a999-4f172df9cad7', 'Ford', 'bev', '6cf9e9b6-28aa-44c7-b6c3-438d518ac12f', 'Focus electric', '2017', '', 69.5, 'type2', '', 1, 'ccs', '', '', 16.4),
('c1fd1277-5d77-416b-bb25-84bd21f57963', 'Hyundai', 'bev', '9771afb8-9e25-4ae6-a5b3-b2a5b9f363f0', 'Kona', '2020', '64 kWh', 72.4, 'type2', '', 3, 'ccs', '', '', 15.8),
('c53b5947-23a3-420c-9798-f3846732e41a', 'Renault', 'bev', 'c0d8a60c-34b8-44fe-8af7-9eeb62eedb4b', 'Zoe', '2019', 'R110 ZE 40', 62.0, 'type2', '', 3, 'ccs', '', '', 16.1),
('c576bee8-8066-4174-bc69-5fe9f2e666ee', 'Hyundai', 'bev', '9771afb8-9e25-4ae6-a5b3-b2a5b9f363f0', 'Ioniq', '2016', '', 84.2, 'type2', '', 1, 'ccs', '', '', 14.4),
('c6a6bd26-6a8f-4ab7-baf3-6cfa057044e3', 'Audi', 'bev', '89c2668c-0c50-4344-9386-93e4000f7673', 'e-tron 50', '2019', '', 56.5, 'type2', '', 3, 'ccs', '', '', 22.7),
('c8e05c0b-05c0-4aac-9f12-35a6a3687e10', 'Audi', 'phev', '89c2668c-0c50-4344-9386-93e4000f7673', 'A3 Sportback 40 e-tron', '2020', '', 64.0, 'type2', '', 1, '', '', '', 12.4),
('c9025ab4-1c85-40d8-86ab-ee406de3b716', 'Polestar', 'bev', '391f000f-d9d1-4c13-b744-95f0b9c8a2e1', '2', '2020', '', 52.7, 'type2', '', 3, 'ccs', '', '', 17.1),
('cb995cc3-84d9-4c87-89dc-f9dee7a47156', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'ID.3', '2020', 'Long Range', 94.6, 'type2', '', 3, 'ccs', '', '', 17.1),
('d03d6e42-d6f8-4e3f-b527-a3c1d1e40f9d', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model X', '2016', '90D', 82.0, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 20.0),
('d8044adf-2538-4d45-b2d8-2b2fd0951766', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'ID.3', '2020', 'Mid Range', 53.0, 'type2', '', 3, 'ccs', '', '', 16.6),
('d8c11860-a582-4784-9e58-d29e94a67fc2', 'Mini', 'bev', '6d9d9248-de4a-4b13-976b-4e9f6688b0b1', 'Cooper SE', '2020', '', 60.0, 'type2', '', 3, 'ccs', '', '', 16.1),
('d97748b1-e384-4238-a225-d498bccd902c', 'Artega', 'bev', '97d0d03a-63c6-4f33-99d7-6e944f71d7c5', 'Karo', '2020', 'Range', 92.7, 'type2', '', 1, '', '', '', 6.4),
('daa3573d-60ea-4c7a-8048-79c575e3db4c', 'Nissan', 'bev', 'dab5a47a-e8ce-4d34-9139-0701499205b1', 'e-NV 200', '', '40 kWh', 63.3, 'type1', '', 1, 'chademo', '', '', 20.0),
('dbf24ffc-3270-409b-b4da-ec386fa36657', 'BMW', 'bev', '0742668c-bf59-4191-890e-2b0883508808', 'i3', '', '120 Ah', 77.5, 'type2', '', 3, 'ccs', '', '', 16.1),
('dc7d163b-29bc-45cf-8156-60eb3e3b1294', 'Nissan', 'bev', 'dab5a47a-e8ce-4d34-9139-0701499205b1', 'Leaf', '2011', '24 kWh', 80.7, 'type1', '', 1, 'chademo', '', '', 16.9),
('de3a8751-00c9-46d1-9e7a-ad830835c6a7', 'Renault', 'bev', 'c0d8a60c-34b8-44fe-8af7-9eeb62eedb4b', 'Zoe', '2019', 'ZE50', 82.5, 'type2', '', 3, 'ccs', '', '', 16.5),
('de7bac96-33ed-44f2-964e-21a4878e9f00', 'Peugeot', 'bev', 'f458fe7d-f545-45f3-8c23-2ab8140b8b5d', 'e-208', '2020', '11 kW-AC', 55.4, 'type2', '', 3, 'ccs', '', '', 16.1),
('e3525b59-d3b9-4eef-9a01-1408358c5534', 'smart', 'bev', 'a462c115-33b4-438b-b590-bc4a33382d1c', 'fortwo ED', '', '22 kW-AC', 98.0, 'type2', '', 3, '', '', '', 16.7),
('e604a056-9338-4044-93dd-5a595d4a3ef3', 'Renault', 'bev', 'c0d8a60c-34b8-44fe-8af7-9eeb62eedb4b', 'Zoe', '2017', 'Q 90', 77.9, 'type2', '', 3, '', '', '', 16.4),
('e60a8ec6-a6dd-46ae-846a-35cb57f1d8e3', 'Peugeot', 'bev', 'f458fe7d-f545-45f3-8c23-2ab8140b8b5d', 'Partner', '', '', 99.8, 'type1', '', 1, '', '', '', 20.5),
('e67dc450-d658-4bee-bd0f-a750d445b2f9', 'BMW', 'bev', '0742668c-bf59-4191-890e-2b0883508808', 'i3', '', '60 Ah', 94.6, 'type2', '', 1, 'ccs', '', '', 14.5),
('e81564b0-46e3-41f6-b6a6-70370a37f685', 'Hyundai', 'bev', '9771afb8-9e25-4ae6-a5b3-b2a5b9f363f0', 'Kona', '2020', '39 kWh 11 kW-AC', 78.3, 'type2', '', 3, 'ccs', '', '', 15.4),
('e8773876-6036-4a6c-926e-5490aae58971', 'Citroen', 'bev', '3b3fc191-f4c3-45da-bc3b-21efbe1b264f', 'Berlingo Electric', '', '', 60.3, 'type1', '', 1, '', '', '', 17.7),
('eb8d28ec-8df7-40a8-8dd7-badf738f0832', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model X', '2019', 'Maximum Range', 68.8, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 20.0),
('ec3b0af7-67c6-400d-b3c2-aa2f3be24c8a', 'Volkswagen', 'phev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'Passat GTE', '2019', '', 94.8, 'type2', '', 1, '', '', '', 16.2),
('ed3fe177-d852-49bd-84ca-8ecd8d7ec3b1', 'Tesla', 'bev', 'f37896c3-6bc5-45e1-b442-b9cbc38e3a7c', 'Model S', '', '70, 22 kW-AC', 77.1, 'type2', '', 3, 'ccs', 'chademo', 'tesla_suc', 18.5),
('ee64213e-fa1d-425e-b90e-6cff9c2a3469', 'DS', 'phev', '37bfdacf-1aca-4eb7-8daa-8dc5b14c59e9', '7 Crossback', '2020', 'E-Tense 4X4 PHEV', 94.9, 'type2', '', 1, '', '', '', 17.4),
('f0132135-9415-4403-818b-cee07f81ceb2', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'e-Golf', '2017', 'CCS', 54.7, 'type2', '', 2, 'ccs', '', '', 16.4),
('f0b185de-9b9d-4a08-924f-450c4dadc7a6', 'smart', 'bev', 'a462c115-33b4-438b-b590-bc4a33382d1c', 'fortwo EQ', '', '22 kW-AC', 56.8, 'type2', '', 3, '', '', '', 16.7),
('f1b46b0a-b101-4072-a246-0b52f0cc51f5', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'e-Golf', '2014', 'CCS', 88.7, 'type2', '', 1, 'ccs', '', '', 15.8),
('f33f0a4f-9b53-4e21-807b-f8b2ca4a24f6', 'Opel', 'bev', '3500fb3e-bd2c-478e-ae5e-ac9ee490594b', 'Ampera e', '2017', 'CCS', 96.4, 'type2', '', 1, 'ccs', '', '', 17.3),
('f45de10a-764f-4a7e-9591-b974d0b87038', 'Mercedes Benz', 'phev', 'b2282fbe-f5d9-48d9-943f-a9b66ec51423', 'A 250 e', '2020', '3,7 kW-AC', 92.4, 'type2', '', 1, '', '', '', 15.0),
('fc5b3c94-c0eb-4515-af3d-4a4106ffe29f', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'e-up', '2020', 'CCS', 84.7, 'type2', '', 2, 'ccs', '', '', 16.6),
('fda95cb7-d391-4344-851e-a1b5a548b42b', 'Volkswagen', 'bev', '481793f5-c8b0-4dc9-b3d4-cc615085ac07', 'e-Golf', '2014', '', 56.2, 'type2', '', 1, '', '', '', 15.8),
('ff261470-8556-4051-afec-c049abd5fe6a', 'Skoda', 'bev', '43763587-6999-406b-8843-28977e1b82c3', 'Enyaq iV', '2020', '55 kWh', 81.3, 'type2', '', 2, 'ccs', '', '', 18.7),
('ffcd3116-4e17-49ff-a926-941c062643ea', 'Skoda', 'bev', '43763587-6999-406b-8843-28977e1b82c3', 'CITIGOe iV', '2020', 'CCS', 64.2, 'type2', '', 2, 'ccs', '', '', 16.6);

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
