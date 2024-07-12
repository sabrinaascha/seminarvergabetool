-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server-Version:               8.4.0 - MySQL Community Server - GPL
-- Server-Betriebssystem:        Win64
-- HeidiSQL Version:             12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Exportiere Datenbank-Struktur für seminarvergabetool
CREATE DATABASE IF NOT EXISTS `seminarvergabetool` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `seminarvergabetool`;

-- Exportiere Struktur von Tabelle seminarvergabetool.art
CREATE TABLE IF NOT EXISTS `art` (
  `art_id` int NOT NULL AUTO_INCREMENT,
  `art_typ` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`art_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.art: ~5 rows (ungefähr)
INSERT INTO `art` (`art_id`, `art_typ`) VALUES
	(1, 'Bachelorarbeit'),
	(2, 'Projektseminar'),
	(3, 'Masterarbeit'),
	(4, 'Praxisseminar'),
	(5, 'Theoretisches Seminar');

-- Exportiere Struktur von Tabelle seminarvergabetool.fach
CREATE TABLE IF NOT EXISTS `fach` (
  `fach_id` int NOT NULL AUTO_INCREMENT,
  `bezeichnung` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`fach_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.fach: ~2 rows (ungefähr)
INSERT INTO `fach` (`fach_id`, `bezeichnung`) VALUES
	(1, 'Wirtschaftsinformatik'),
	(2, 'BWL mit Schwerpunkt WI');

-- Exportiere Struktur von Tabelle seminarvergabetool.gruppe
CREATE TABLE IF NOT EXISTS `gruppe` (
  `gruppe_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`gruppe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.gruppe: ~0 rows (ungefähr)

-- Exportiere Struktur von Tabelle seminarvergabetool.lehrstuhl
CREATE TABLE IF NOT EXISTS `lehrstuhl` (
  `lehrstuhl_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `homepage` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `professor` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`lehrstuhl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.lehrstuhl: ~9 rows (ungefähr)
INSERT INTO `lehrstuhl` (`lehrstuhl_id`, `name`, `homepage`, `professor`) VALUES
	(1, 'Lehrstuhl für Wirtschaftsinformatik I - Informationssysteme', 'https://www.uni-regensburg.de/informatik-data-science/wi-pernul/startseite/index.html', 'Pernul'),
	(2, 'Lehrstuhl für Wirtschaftsinformatik II', 'https://www.uni-regensburg.de/informatik-data-science/wi-heinrich/start/index.html', 'Heinrich'),
	(3, 'Lehrstuhl für Wirtschaftsinformatik III - Business Engineering', 'https://www.uni-regensburg.de/informatik-data-science/wi-leist/news/index.html', 'Leist'),
	(4, 'Lehrstuhl für Wirtschaftsinformatik IV', 'https://www.uni-regensburg.de/informatik-data-science/wi-kesdogan/startseite/index.html', 'Kesdogan'),
	(5, 'Lehrstuhl für Maschinelles Lernen, insbes. Uncertainty Quantification', 'https://www.uni-regensburg.de/informatik-data-science/maschinelles-lernen-insb-uncertainty-quantific', 'Schnurr'),
	(6, 'Lehrstuhl für Internet Business und Digitale Soziale Medien', 'https://www.uni-regensburg.de/informatik-data-science/wi-klier/start/index.html', 'Klier'),
	(7, 'Lehrstuhl für IoT-based Information Systems', 'https://www.uni-regensburg.de/informatik-data-science/wi-schoenig/startseite/index.html', 'Schönig'),
	(8, 'Lehrstuhl für Künstliche Intelligenz in der IT-Sicherheit', 'https://www.uni-regensburg.de/informatik-data-science/ki-in-it-sicherheit/startseite/index.html', 'Leitner'),
	(9, 'Lehrstuhl für Nachvollziehbare Künstliche Intelligenz in der Betrieblichen Wertschöpfung', 'https://www.uni-regensburg.de/informatik-data-science/nachvollziehbare-ki/startseite/index.html', 'Kraus');

-- Exportiere Struktur von Tabelle seminarvergabetool.mitarbeiter
CREATE TABLE IF NOT EXISTS `mitarbeiter` (
  `ma_id` int NOT NULL AUTO_INCREMENT,
  `vorname` varchar(20) DEFAULT NULL,
  `nachname` varchar(30) DEFAULT NULL,
  `nds` varchar(10) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `lehrstuhl_lehrstuhl_id` int DEFAULT NULL,
  PRIMARY KEY (`ma_id`),
  KEY `lehrstuhl_lehrstuhl_id` (`lehrstuhl_lehrstuhl_id`),
  CONSTRAINT `mitarbeiter_ibfk_1` FOREIGN KEY (`lehrstuhl_lehrstuhl_id`) REFERENCES `lehrstuhl` (`lehrstuhl_id`),
  CONSTRAINT `mitarbeiter_chk_1` CHECK (regexp_like(`nds`,_utf8mb4'^[a-zA-Z0-9]+$')),
  CONSTRAINT `mitarbeiter_chk_2` CHECK ((`email` like _utf8mb4'%@%'))
) ENGINE=InnoDB AUTO_INCREMENT=195 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.mitarbeiter: ~30 rows (ungefähr)
INSERT INTO `mitarbeiter` (`ma_id`, `vorname`, `nachname`, `nds`, `email`, `lehrstuhl_lehrstuhl_id`) VALUES
	(125, 'Maximilian', 'Wittig', 'wim50594', 'maximilian.wittig@ur.de', 4),
	(127, 'Bernd', 'Heinrich', 'heb20733', 'Bernd.Heinrich@wiwi.uni-regensburg.de', 2),
	(128, 'Susanne', 'Leist', 'les09103', 'susanne.leist@wiwi.uni-regensburg.de', 3),
	(130, 'Marc', 'Roßberger', 'rom26690', 'Marc.Rossberger@wiwi.uni-regensburg.de', 4),
	(131, 'Jan', 'Kolter', 'koj03239', 'jan.kolter@wiwi.uni-regensburg.de', 1),
	(132, 'Volker', 'Berg', 'bev27879', 'volker.berg@ur.de', 3),
	(133, 'Maria', 'Leitner', 'mle12345', 'maria.leitner@ur.de', 8),
	(135, 'Mathias', 'Kraus', 'krm12345', 'mathias.kraus@informatik.uni-regensburg.de', 9),
	(136, 'Stefan', 'Schönig', 'scs01281', 'tefan.Schoenig@wiwi.uni-regensburg.de', 7),
	(137, 'Marietheres', 'Dietz', 'dim29618', 'marietheres.dietz@wiwi.uni-regensburg.de', 1),
	(138, 'Sabri', 'Hassan', 'has11237', 'sabri.hassan@wiwi.uni-regensburg.de', 1),
	(139, 'Alexander', 'Schiller', 'Sca56792', 'Alexander.Schiller@wiwi.uni-regensburg.de', 2),
	(141, 'Paul', 'Bärnreuther', 'bap21113', 'Paul.Baernreuther@wiwi.uni-regensburg.de', 2),
	(144, 'Stefan', 'Winderl', 'scp08240', 'stefan.winderl@ur.de', 4),
	(153, 'Armin', 'Steinwender', 'sta11392', 'armin.steinwender@wiwi.uni-regensburg.de', 2),
	(155, 'Julia', 'Klier', 'hej26719', 'julia.klier@wiwi.uni-regensburg.de', 6),
	(156, 'Doğan', 'Kesdoğan', 'ked19347', 'Dogan.Kesdogan@wiwi.uni-regensburg.de', 4),
	(159, 'Vinh', 'Pham', 'phv64007', 'Vinh.Pham@uni-regensburg.de', 4),
	(162, 'Günther', 'Pernul', 'peg14514', 'Guenther.Pernul@wiwi.uni-regensburg.de', 1),
	(166, 'Alexander', 'Schiller', 'Sca56792', 'Alexander.Schiller@wiwi.uni-regensburg.de', 2),
	(169, 'Markus', 'Lang', 'lam45043', 'Markus.Lang@wiwi.uni-regensburg.de', 3),
	(171, 'Alperen', 'Aksoy', 'aka50880', 'alperen.aksoy@ur.de', 4),
	(175, 'Michael', 'Szubartowicz', 'szm61364', 'michael.szubartowicz@wiwi.uni-regensburg.de', 2),
	(176, 'Daniel', 'Schlette', 'scd10910', 'daniel.schlette@wiwi.ur.de', 1),
	(184, 'Sabrina', 'Friedl', 'saf33768', 'sabrina.friedl@wiwi.uni-regensburg.de', 1),
	(187, 'Moritz', 'Hofmann', 'hom06921', 'moritz.hofmann@gmail.com', 3),
	(188, 'Daniel', 'Konadl', 'dko1234', 'daniel.konadl@informatik-ur.de', 3),
	(189, 'Janik', 'Wörner', 'woj08673', 'Janik.woerner@ur.de', 3),
	(191, 'Markus', 'Hornsteiner', 'hom14652', 'markus.hornsteiner@uni-regensburg.de', 7),
	(192, 'Leo', 'Poss', 'pol42460', 'leo.poss@ur.de', 7);

-- Exportiere Struktur von Tabelle seminarvergabetool.phase
CREATE TABLE IF NOT EXISTS `phase` (
  `phase_id` int NOT NULL AUTO_INCREMENT,
  `semester` varchar(20) DEFAULT NULL,
  `start_p1` datetime DEFAULT NULL,
  `ende_p1` datetime DEFAULT NULL,
  `start_p2` datetime DEFAULT NULL,
  `ende_p2` datetime DEFAULT NULL,
  `start_p3` datetime DEFAULT NULL,
  `ende_p3` datetime DEFAULT NULL,
  `start_vorstellung` datetime DEFAULT NULL,
  `ende_vorstellung` datetime DEFAULT NULL,
  PRIMARY KEY (`phase_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.phase: ~1 rows (ungefähr)
INSERT INTO `phase` (`phase_id`, `semester`, `start_p1`, `ende_p1`, `start_p2`, `ende_p2`, `start_p3`, `ende_p3`, `start_vorstellung`, `ende_vorstellung`) VALUES
	(2, 'Sommersemester 2024', '2024-07-02 12:00:00', '2024-07-06 12:00:00', '2024-07-07 12:00:00', '2024-07-14 12:00:00', '2024-07-14 12:00:00', '2024-07-20 12:00:00', '2024-07-03 10:00:00', '2024-07-04 20:00:00');

-- Exportiere Struktur von Tabelle seminarvergabetool.projekt
CREATE TABLE IF NOT EXISTS `projekt` (
  `projekt_id` int NOT NULL AUTO_INCREMENT,
  `titel` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `beschreibung` varchar(2500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `max_anzahl` int DEFAULT NULL,
  `neu` tinyint(1) DEFAULT NULL,
  `studiengang_studiengang_id` int DEFAULT NULL,
  `fach_fach_id` int DEFAULT NULL,
  `art_art_id` int DEFAULT NULL,
  `lehrstuhl_lehrstuhl_id` int DEFAULT NULL,
  PRIMARY KEY (`projekt_id`),
  KEY `studiengang_studiengang_id` (`studiengang_studiengang_id`),
  KEY `art_art_id` (`art_art_id`),
  KEY `lehrstuhl_lehrstuhl_id` (`lehrstuhl_lehrstuhl_id`),
  KEY `fach_fach_id` (`fach_fach_id`),
  CONSTRAINT `projekt_ibfk_1` FOREIGN KEY (`studiengang_studiengang_id`) REFERENCES `studiengang` (`studiengang_id`),
  CONSTRAINT `projekt_ibfk_2` FOREIGN KEY (`art_art_id`) REFERENCES `art` (`art_id`),
  CONSTRAINT `projekt_ibfk_3` FOREIGN KEY (`lehrstuhl_lehrstuhl_id`) REFERENCES `lehrstuhl` (`lehrstuhl_id`),
  CONSTRAINT `projekt_ibfk_4` FOREIGN KEY (`fach_fach_id`) REFERENCES `fach` (`fach_id`),
  CONSTRAINT `projekt_chk_1` CHECK ((`max_anzahl` > 0)),
  CONSTRAINT `projekt_chk_2` CHECK ((`neu` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.projekt: ~36 rows (ungefähr)
INSERT INTO `projekt` (`projekt_id`, `titel`, `beschreibung`, `max_anzahl`, `neu`, `studiengang_studiengang_id`, `fach_fach_id`, `art_art_id`, `lehrstuhl_lehrstuhl_id`) VALUES
	(55, 'Usability von Transparency Enhancing Technologies/Tools – TET', 'Ziel eines TET ist die Nachvollziehbarkeit für den Nutzer herzustellen, welche Daten durch die Nutzung digitaler Anwendungen preisgegeben werden und wie diese verwendet oder missbraucht werden können. Dies ist abhängig von der Usability, mit welcher der Nutzer seine Ziele effektiv, effizient und zufriedenstellend erreichen kann. \\r\\nIm Seminar sind folgende Fragen zu beantworten: Wodurch zeichnet sich „gute“ Usability aus, insbesondere bei TET? Gibt es hier Besonderheiten, die einen Einfluss auf die Gestaltung der TET haben? Wie kann die Usability von TET gemessen und bewertet werden? In einer Nutzerstudie soll die Usability ausgewählter Transparency Enhancing Tools überprüft werden.', 1, 0, 2, 1, 1, 2),
	(57, 'Überblick über nutzerfreundliche Privatsphäre-gewährender Apps für Android / iOS ', 'Für verschiedene Zwecke gibt es jeweils unzählige Apps. Nur wenige davon berücksichtigen die Privatheit der Nutzer und zeichnen sich durch „gute“ Usability aus. In diesem Seminar sind relevante Usability Standards und Usability Best Practices für Apps zu bestimmen und die Besonderheiten, die sich durch den Schutz der Privatheit ergeben (Anonymität vs. Personalisierung), mit einzubeziehen. Kriterien für nutzerfreundliche Privatsphäre-gewährende Eigenschaften sind zu entwickeln und Apps anhand dieser zu Beurteilen.', 2, 0, 2, 1, 2, 4),
	(59, 'Data Uncertainty: Neuronale Netze bei unsicheren Inputdaten', 'Neuronale Netze sind in der Lage komplexe Sachverhalte abzubilden und werden daher mitunter in der Analyse komplexer Prozesse verwendet\r\nAllerdings sind traditionelle Neuronale Netze nicht in der Lage unsichere Inputdaten zu berücksichtigen, obwohl dies hochgradig relevant ist.\r\n\r\nForschungsfrage: Auf welche Weise können unsichere Inputdaten beim Trainieren und/oder in der Anwendung von Neuronalen Netzen berücksichtigt werden?\r\n\r\nAufgabenstellung \r\nImplementierung und Analyse eines Verfahrens zum Trainieren und/oder Anwenden von Neuronalen Netzen unter Verwendung von gegebenen unsicheren Inputdaten\r\nEvaluation der Güte des Verfahrens\r\nEmpfohlen: Starkes Interesse und Spaß an Data Analytics und der mathematischen Modellierung ', 1, 0, 3, 1, 3, 9),
	(60, 'Erkennung von Datenduplikaten', '- Unternehmen halten große Mengen an Daten in ihren Bestandsführungssystemen (z. B. Stammdaten bei Versicherungen)\r\nOftmals beziehen sich mehrere Dateneinträge auf dieselbe\r\nreale Entität, wie z. B. Kunden, die als „Duplikate“ bezeichnet werden. Diese ziehen gravierende Probleme nach sich (z. B. in der Kundenansprache)\r\nAufgabenstellung \r\n- Einarbeitung in eine existierende Methode zur Duplikaterkennung\r\n- Ausgestaltung und Anwendung der Methode bei verschiedenen Datensätzen (mit entsprechendem Programmcode)\r\n- Analyse und Bewertung der Güte der Methode im Rahmen einer Evaluation\r\n\r\nBetreuung: Dr. Alexander Schiller', 3, 0, 1, 1, 2, 2),
	(62, 'Erkennung von Datenduplikaten', '- Unternehmen halten große Mengen an Daten in ihren Bestandsführungssystemen (z. B. Stammdaten bei Versicherungen)\r\nOftmals beziehen sich mehrere Dateneinträge auf dieselbe\r\nreale Entität, wie z. B. Kunden, die als „Duplikate“ bezeichnet werden. Diese ziehen gravierende Probleme nach sich (z. B. in der Kundenansprache)\r\nAufgabenstellung \r\n- Einarbeitung in eine existierende Methode zur Duplikaterkennung\r\n- Ausgestaltung und Anwendung der Methode bei verschiedenen Datensätzen (mit entsprechendem Programmcode)\r\n- Analyse und Bewertung der Güte der Methode im Rahmen einer Evaluation\r\n\r\nBetreuung: Dr. Alexander Schiller', 3, 0, 2, 1, 4, 2),
	(63, 'Design Principles für Cyber Threat Intelligence Observables im Identity Management', 'Stell dir vor du bist ein Manager und bekommst die Aufgabe die Berechtigungen von deinem Team zu checken. Nur ist da jetzt ein Praktikant, für den du verantwortlich bist, von dem du noch nie was gehört hast und der auch noch mehr Berechtigungen als alle anderen zusammen hat: Irgendwie verdächtig. Als verantwortungsbewusster Manager möchtest du diese Beobachtung strukturiert an die Kollegen vom SIEM (Security Information and Event Management) weiterleiten. Dazu gibt es CTI (Cyber Threat Intelligence) Formate. \r\n\r\nZiel der Arbeit ist es, mögliche Beobachtungen im Identity Management zu identifizieren, zu beschreiben, in eine Erweiterung für CTI Formate zu überführen und mit Design Principles theoretisch zusammenzufassen. Eine Design Science Research Methodik wird erwartet', 4, 0, 2, 1, 2, 1),
	(64, 'Digital Honey: Konvertierung eines digitalen Zwillings in einen Honeypot', 'Honeypots imitieren Echtwelt-Systeme, die es Unternehmen erlauben, den State-of-the Art von Angreifern hinsichtlich deren Techniken etc. zu lernen. Je länger ein Angreifer mit einem Honeypot interagiert und im Glauben bleibt, dieser sei ein Echtwelt-System, desto größer ist der Erkenntnisgewinn für Unternehmen. Um diesen Lerneffekt zu maximieren, könnten digitale Zwillinge als Honeypots genutzt werden. Digitale Zwillinge sind virtuelle Abbilder von (physischen) Objekten. Durch diese werden Systeme wahrheitsgetreu abgebildet, wodurch der Erkenntnisgewinn für das jeweilige Unternehmen steigen kann. Zielstellung dieses Themas ist, es die Konvertierung von digitalen Zwillingen zu Honeypots prototypisch zu implementieren.', 2, 0, 2, 2, 4, 1),
	(65, 'Benchmarking ISIS12', 'Wie bewährt sich ein ISMS aus Kundensicht? Diese Frage taucht oft bei KMUs auf, wenn es darum geht, sich für ein Produkt am Markt zu entscheiden. Weder liegen auf qualitativer Ebene belastbare Aussagen vor, noch gibt es in quantitativer Hinsicht Erkenntnisse darüber, wie wirkungsvoll ISIS12 im Einsatz im Vergleich zu anderen ISMS einzuschätzen ist. Daher soll dieses Projekt Ansätze zu einem derartigen Benchmarking entwickeln. Konkret: Gibt es erkennbare und identifizierbare Unterschiede in der Wirksamkeit von ISIS12 im Vergleich zu anderen ISMS? Wie ist die Literaturlage?', 1, 0, 4, 2, 1, 2),
	(66, 'Analyse und Erhebung passender Visualisierungstechniken in Splunk für eine Live Digital Forensics Investigation', 'Basierend auf unserer aktuellen Forschung im Bereich der Live Digital Forensics Investigation [1] soll die Software Splunk hinsichtlich der Nutzbarkeit und Adaption vorhandener Visualisierungstechniken untersucht werden. Das Ziel ist es die Visualisierungstechniken hinsichtlich der Erkennung von Indicators of compromise (IOCs) sowie weitere Anomalien eines laufenden und infizierten Systems zu erheben und zu bewerten. Für die Bearbeitung der Bachelorarbeit werden gute Kenntnisse in der Netzwerktechnik durch den erfolgreichen Besuch des Kurses „Internettechnologien und Network Computing“ zwingend vorausgesetzt.\r\n[1] https://www.researchgate.net/publication/340777856_Designing_a_Decision-Support_Visualization_for_Live_Digital_Forensic_Investigations\r\n[2] https://www.researchgate.net/publication/340777856_Designing_a_Decision-Support_Visualization_for_Live_Digital_Forensic_Investigations', 1, 0, 1, 2, 1, 1),
	(67, 'Konzeption bewusstseinssteigernde Maßnahmen zum Schutz vor Webtracker', 'Webtracking setzt Techniken zum Re-Identifizieren (Langzeit-Identifier) von Benutzer ein, um Informationen zu seinem Browsing-Verhalten zu sammeln und bspw. für Werbezwecke zu analysieren (personalisierte Werbung). Aktuelle Literaturstudien zeigen einen Trend zu einer Schattenwirtschaft, bei der die Akteure auf dem Werbemarkt ohne Einflussnahme des Nutzers personenbezogene Daten sammeln. Nutzer haben in diesem Szenario, trotz der Bestimmungen der europäischen Datenschutz-Grundverordnung, keine Möglichkeiten der informationellen Selbstbestimmung.\r\nZiel dieser Bachelorarbeit ist es daher, Konzepte zu bewusstseinssteigernde Maßnahmen zu untersuchen und weiterzuentwickeln. Zu diesem Zweck sollen in dieser Arbeit verschiedene Möglichkeiten (Software, Hardware, Zertifikate, Kennzahlen etc.) hinsichtlich diverser Faktoren (Information, Relevanz, Vertrauen, Orientierung etc.) evaluiert werden. Für die Evaluation wäre eine Untersuchung mit Probanden wünschenswert.', 1, 0, 1, 1, 1, 4),
	(68, 'Text Analytics: Messung der Aktualität textueller Daten ', '- Ähnlich wie strukturierte Daten können auch Aussagen in Textdaten veralten\r\n- Ein Übertrag der Messung der Aktualität von strukturierten Daten auf Textdaten ist nicht direkt möglich\r\n- Machine Learning-Verfahren können komplexe Zusammenhänge lernen und werden im Text Analytics für verschiedenste Aufgaben eingesetzt\r\n- Forschungsfrage: Können diese Verfahren auch genutzt werden, um die Aktualität textueller Daten messen?\r\n- Zusammenarbeit mit dem Unternehmen Xapio\r\nAufgabenstellung:\r\n- Schaffung einer Datenbasis durch geeignete Annotation von Wikipedia-Daten\r\n- Nutzung von Machine Learning-Verfahren zur Messung der Aktualität von Wikipedia-Daten\r\n- Evaluation der Güte des Verfahrens', 1, 0, 1, 1, 1, 2),
	(70, 'Security Orchestration für IoT - Konzeption und prototypische Implementierung', 'Informationssicherheit spielt für IoT-Geräte eine wichtige Rolle. Da sich Angreifer kontinuierlich neuer Methoden bedienen und Software sowie Konfiguration von IoT-Geräten regelmäßig geupdatet werden muss, ist die Orchestrierung der IT-Sicherheit ein wichtiges Themenfeld. In dieser Bachelorarbeit sollen zunächst die theoretischen Grundlagen zu IoT-Netzwerken, Software Defined Networks und bestehenden Frameworks  erarbeitet werden. Darauf aufbauend soll ein Konzept entwickelt und implementiert werden, dass auf open-source Komponenten (z.B. Ansible) basiert und ausreichende Orchestrierungsfunktionalität für einen Beispielanwendungsfall bietet.', 1, 0, 1, 1, 1, 7),
	(71, 'Implementierung und Evaluation eines intelligenten Ampel-Steuer-Systems in SUMO', 'In der heutigen Zeit entstehen immer größer werdende Verkehrsflüsse und insbesondere Städte können (zur Rush-Hour) dadurch stark überlastet werden. Ein Lösungsansatz, um Verkehrsflüsse zu verbessern ist das System von intelligenten Ampelschaltungen. Im Gegensatz zu klassischen Ampelschaltungen, welche statisch nach x Sekunden umschalten, können diese auf bestehende Verkehrssituationen reagieren und je nach Verkehrsaufkommen gewisse Fahrbahnen bevorzugen.\r\nMithilfe der Simulations-Software SUMO können komplexe Verkehrsflüsse simuliert werden und Auswertungen über z.B. die Wartezeiten von Fahrzeigen an Ampeln gemacht werden.\r\nIn dieser Arbeit sollen bestehende Ansätze zur Ampelschaltung in SUMO betrachtet und evaluiert werden, sowie ein neuer verbesserter Ansatz entwickelt werden.\r\nEs werden Kenntnisse und Begeisterung an der Programmierung vorausgesetzt. Die bestehende Implementierung ist in Python umgesetzt.', 1, 0, 2, 1, 1, 4),
	(73, 'Simulation of the network congestion in transport layer', 'Your task is deeply to understand what is congestion and how congestion occurs.\r\nMake a computer simulation of some scenarios given in book named "Computer Networking a Top Down Approach, Authors: Kurose and Ross" pages between 259 - 283. You can use any programming language.\r\nResults must be the same as the given in the book and discussed. If possible, a new congestion control algorithm may be proposed.', 1, 0, 2, 1, 1, 8),
	(75, 'Graph-basierte Persistierung von Cyber Threat Intelligence', 'Mit zunehmender Relevanz von Cyber Threat Intelligence (CTI) zur Vereinheitlichung des Austauschs von sicherheitsrelevanten Informationen über Unternehmensgrenzen hinaus, wird die Notwendigkeit einer Plattform zur Verwaltung der CTI immer klarer. Dabei bestehen unterschiedlichste Anforderungen an eine solche Plattform, wie beispielsweise die Durchsetzung des gewählten CTI-Formates (z.B. STIX2.x) oder eine flexible Abfragemöglichkeit von Informationen. Ein zentraler Bestandteil einer entsprechenden Lösung ist das Speichern und Abfragen der CTI.\\r\\nDabei finden im Umfeld von CTI häufig Graph-basierte Ansätze Verwendung (wie auch das Format STIX2.x auf Graph-Konzepten basiert). Mit dem neuen API-Paradigma GraphQL (im Gegensatz zur REST API) lassen sich ein Großteil der Anforderungen an das Backend einer CTI-Plattform erfüllen.\\r\\n\\r\\nZiel dieser Bachelorarbeit ist die Entwicklung eines Datenbankschemas, das auf Eigenschaften von CTI eingeht. Dieses kann dann der Konzeption und Implementierung einer GraphQL-API zum Speichern, Abfragen, Aktualisieren und Löschen von STIX2.x-basierter CTI dienen.', 1, 0, 1, 2, 3, 1),
	(76, 'Aufbau einer modernen Web-Plattform zur Analyse der Forschung im Kontext von Visualisierungen in der IT-Sicherheit', 'Visualisierungsansätze wurde in wissenschaftlichen Publikationen vorgestellt. Nur die wenigsten der oft sehr innovativen Ansätze werden jedoch auch operativ in der Praxis eingesetzt. Ein Grund hierfür ist die Unübersichtlichkeit der großen Menge der zur Verfügung stehenden Forschungsergebnisse. Strukturierte Literaturanalysen versuchen, solch große Mengen an Forschungsergebnissen sowohl qualitativ als auch quantitativ zusammenzufassen. Allerdings sind diese Analysen oft schon zum Zeitpunkt ihrer Veröffentlichung nicht mehr aktuell und werden auch nicht aktualisiert. Nur wenn strukturierte Literaturanalysen auch langfristig die aktuell verfügbare Literatur zusammenfassen, bieten sie auch einen tatsächlichen Mehrwert.\\r\\n\\r\\nZiel dieser Bachelorarbeit ist es, eine interaktive Web-Plattform zu konzeptionieren und prototypisch umzusetzen, welche im Stile einer strukturierten Literaturanalyse langfristig einen Überblick über die verfügbare Forschung zu Visualisierungen für die IT-Sicherheit geben kann. Dabei sollen ausgehend von den zentralen Methodiken für strukturierte Literaturanalysen, die wichtigsten qualitativen Metriken (bspw. wichtige Forschungsgruppen, Entwicklung der Publikationen im Zeitverlauf) verfügbar sein. Zudem soll auch ein Überblick über die qualitativen Analyseergebnisse der Forschung (bspw. genutzte Daten, Visualisierungstechniken) möglich sein.', 1, 0, 1, 2, 3, 1),
	(77, 'Analyse und Bewertung von aktuellen Methoden zur IT-forensischen Analyse von Internet of Things (IoT)', 'Die IT-forensische Untersuchung gewinnt immer mehr an Bedeutung, speziell aufgrund der ansteigenden Anzahl an IoT-Geräten. Um Ressourcen zur Analyse zu erhalten, müssen Methoden und Tools gezielt ausgewählt werden. Ziel der Arbeit ist es, aktuelle Methoden zur IT-forensischen Analyse von IoT zu erheben und zu bewerten.', 1, 0, 1, 1, 1, 7),
	(78, 'Analyse und strukturierte Aufbereitung von file corruption vulnerabilities', 'Moderne Anwendungen beinhalten immer noch gravierende Sicherheitslücken, welche es Angreifern erlaub in das System einzudringen und maliziöse Handlungen auszuführen [1, 2]. Im Rahmen der theoretischen Bachelorarbeit sollen aktuelle file corruption vulnerabilities (bzw. file-system exploitation methods) hinsichtlich der Vorgehensweise analysiert und aufbereitet werden. \r\nFür die Bearbeitung der theoretischen Bachelorarbeit sind ein gutes Grundverständnis von IT-Sicherheit (Nachgewiesen durch „IT-Security I“) und gute Englischkenntnisse zwingend notwendig! Start ab Ende Februar 2021\r\n[1] https://thehackernews.com/2020/10/antivirus-software-vulnerabilities.html\r\n[2] https://www.cyberark.com/resources/threat-research-blog/anti-virus-vulnerabilities-who-s-guarding-the-watch-tower ', 3, 0, 1, 2, 5, 1),
	(79, 'State of the Art der Governance in Decentralized Autonomous Organizations (DAOs)', 'Im Rahmen des Seminars sollen Selbstverwaltungsmechanismen (Governance) von DAOs untersucht werden. Dabei soll eine umfassende Liste bestehender DAO Projekte erstellt werden, die auf Funktionalitäten und Prozesse untersucht werden. Anschließend sollen die Funktionalitäten kategorisiert und miteinander verglichen werden. Eine Diskussion der Ausgereiftheit (maturity) und Sicherheitsaspekte sollte dabei nicht fehlen. Abschließend soll eine Einschätzung der Eignung solcher Funktionalitäten für private Blockchain Netzwerke getroffen werden.', 1, 0, 1, 1, 5, 9),
	(80, 'Analyse und Bewertung von Methoden der pro-aktiven IT-Security für die Digital Forensic Acquisition', 'Im Rahmen des theoretischen Seminars soll der aktuelle Stand in der Literatur hinsichtlich der Verwendung von Methoden aus der pro-aktiven IT-Security für die Gewinnung von digitalen Beweisen erhoben werden. Dabei werden u.a. Methoden für die Erkennung auch Ausnutzung von bekannten und unbekannten Schwachstellen für die Gewinnung von digitalen Beweisen verwendet. Die Studierenden sollen eine strukturierte Literaturrecherche durchführen und die Ergebnisse hinsichtlich der Verwendung auf Smartphones (IPhones) bewertet werden. Das Seminar kann zu zweit (als Gruppe) bearbeitet werden', 2, 0, 1, 1, 5, 8),
	(82, 'Datenformate und Standards im Bereich Informationssicherheit', 'In der Informationssicherheit existiert eine Vielzahl an Datenformaten und Standards, die mit verschiedenen Zielsetzungen Informationen strukturieren (z.B. CPE, CVE, CVSS, STIX, MISP, etc.).\\r\\nZiel dieses theoretischen Seminars ist es ausgehend von einer Publikation der Agentur der Europäischen Union für Cybersicherheit (ENISA) eine aktuelle Übersicht über alle Datenformate in Bereich der Informationssicherheit zu erstellen. In diesem Kontext ist eine systematische Recherche durchzuführen.', 2, 0, 1, 1, 5, 1),
	(83, 'Wartung und Optimierung von Attributbasierten Zugriffskontrollregeln – Aktueller Stand und Trends', 'Die Modellierung von attributbasierten Zugriffskontrollregeln hat in Forschung und Praxis großes Interesse erfahren. Da Zugriffskontrollregeln mit der Zeit jedoch veralten, müssen sie auch aktuell gehalten werden. Ziel dieser Arbeit ist die strukturierte Aufarbeitung des aktuellen Forschungsstandes sowie offener Fragen zur Wartung von attributbasierten Zugriffskontrollregeln. Hierfür soll die existierende Literatur erfasst und anhand zu definierender Kriterien analysiert und aufbereitet werden. Abschließend soll eine Zusammenfassung des aktuellen Forschungsstandes und offener Fragestellungen erstellt werden.', 2, 0, 1, 1, 5, 2),
	(85, 'Konzeptentwicklung eines Verfahrens zur Transformation bestehender Geschäftsprozesse in nachhaltige ', 'In diesem Seminar sollen zunächst Kriterien und Anforderungen an nachhaltige Geschäftsprozesse erhoben werden. Im Anschluss daran soll ein Konzept zur Transformation bestehender Geschäftsprozesse', 3, 0, 5, 1, 5, 4),
	(86, 'Untersuchung von Internet Email-Verkehr für eine Disclosure Attack', 'E-Mails stellen heute weiterhin einen großen Teil an Kommunikation im Internet dar und es gibt verschiedene Ansätze zur Sicherstellung von Authentizität und Vertraulichkeit von ihnen. Dennoch kam es in den letzten Jahren immer wieder zu verschiedenen Vorfällen, welche Unsicherheiten in eingesetzten Systemen aufzeigten.\r\nBei einer Disclosure-Attack versucht ein Angreifer meist Meta-Informationen über ein System, z.B. Webseite herauszufinden. In dieser Arbeit soll ein bestehender aufgezeichneter E-Mail Verkehr untersucht werden, um herauszufinden, inwiefern ein Disclosure-Angriff auf diesen Datensatz angewandt werden kann', 1, 0, 1, 2, 3, 3),
	(90, 'Text Analytics: Prüfung der Aktualität textueller Daten mit OIE', '- Ähnlich wie strukturierte Daten können auch Aussagen in Textdaten veralten\r\n- Mit Ansätzen aus der Open Information Extraction (OIE) können (semi-) strukturierte Informationen aus Texten gewonnen werden, u.a. in Form von Tripeln (Subjekt, Prädikat, Objekt)\r\n- Diese Informationen können mit anderen Infos (z.B. aus Referenztexten, Wissensbasen) abgeglichen werden\r\n- Forschungsfrage: Kann ein solches Verfahren genutzt werden, um die Aktualität textueller Daten zu prüfen?\r\nAufgabenstellung\r\n- Erweiterung/Schaffung einer Datenbasis durch geeignete Annotation von Wikipedia-Daten\\r\\n- Nutzung und Weiterentwicklung eines bestehenden OIE-Verfahrens zur Messung der Aktualität von Wikipedia-Daten\r\n- Evaluation der Güte des Verfahren\r\nEmpfohlen\r\n- PC mit geeigneter CUDA (SDK 10.0)-fähiger Grafikkarte', 1, 0, 1, 1, 3, 2),
	(92, 'Extraction and Visualization of Industrial IoT Data', 'Aufbauen einer Datenerfassung aus Sensoren und SPS (Speicherprogrammierbaren Steuerungen von Maschinen) mittels Node Red (dafür gibt es Plugins), speichern der Daten in Datenbanken; Visualisierung der Daten über Grafana; (Kann alles im IoT Labor durchgeführt werden)', 3, 0, 1, 2, 4, 7),
	(93, 'Identifikationsmethoden von „trolls“ in Social Media (WI)', 'Theoretischer Hintergrund: Trolle in Social Media, Social Media\r\nMethode: Literaturrecherche\r\nLiteraturanalyse hinsichtlich der verschiedenen Methoden zur Identifikation von Trollen in online communities; strukturierte Gegenüberstellung der Methoden anhand geeigneter Parameter (Def., Ziel, Einsatzgebiete, Charakteristika, etc.)\r\nAufzeigen von Limitationen und Potentiale anhand geeigneter Beispiele/ Einsatzgebiete von Trollen (Trolle, die Fake News verbreiten, opinion manipulation Trolle, etc.)\r\nEinstiegsliteratur: Mihaylov, T., Mihaylova, T., Nakov, P., Màrquez, L., Georgiev, G. D., & Koychev, I. K. (2018). The dark side of news community forums: Opinion manipulation trolls. Internet Research.', 1, 0, 1, 2, 3, 6),
	(94, 'Entwicklung eines nachhaltigen IT-Sicherheitskonzepts für KMUs', 'Kleine und mittelständische Unternehmen (KMUs) stehen vor besonderen Herausforderungen in der IT-Sicherheit, da sie oft nicht die gleichen Ressourcen wie große Unternehmen haben. Ziel dieses Projekts ', 2, 0, 1, 2, 4, 3),
	(95, 'Implementierung eines datenschutzkonformen CRM-Systems', 'Customer Relationship Management (CRM) Systeme sind ein zentrales Werkzeug in vielen Unternehmen, um Kundenbeziehungen zu pflegen und zu verbessern. In diesem Projekt soll ein CRM-System entwickelt werden.', 3, 0, 2, 2, 4, 4),
	(96, 'Analyse von Sicherheitslücken in IoT-Umgebungen', 'Das Internet der Dinge (IoT) bringt eine Vielzahl neuer Geräte ins Netzwerk, die oft nicht ausreichend gesichert sind und somit Angriffsvektoren für Cyberkriminelle darstellen. ', 4, 0, 6, 1, 4, 7),
	(97, 'Parallel Implementation of Hitting Set Attack Algorithm on Mix Anonymity Networks', '- Implement a simulation program of Hitting Set Attack on Mix Networks by using multi-thread programming techniques.\r\n- Compare running time with the single-thread version of the algorithm.\r\n- About the Hitting Set Attack, this paper may be observed. https://www.freehaven.net/anonbib/papers/Hitting_Set_Attack.pdf\r\n\r\n- If you have questions, you can reach by alperen.aksoy@fau.de and we can set a meeting about the details.', 2, 0, 2, 2, 4, 4),
	(98, 'Vorgehensmodelle zur Modellierung von Security Requirements im Industrial IoT', 'Das Industrial IoT läutet eine neue Phase in der Industrie ein. Es ist damit möglich, Maschinen auf noch nie dagewesene Weise zu vernetzen und dadurch riesige Potentiale zu schaffen. Allerdings bringt diese Vernetzung auch Risiken mit sich, die wir bereits aus dem „normalen“ Internet kennen. Viren, Trojaner, Hackerangriffe und ähnliches. Um zukünftig solchen Gefahren besser begegnen zu können, gibt es Design Paradigmen wie „Security by design“. Um diese in der Industrie umsetzen zu können, ist es wichtig, mit Hilfe eines strukturierten Vorgehensmodells alle Aspekte eines Prozesses aufzunehmen. Das heißt, die Prozessbeteiligten, die Geräte, die Kommunikationswege etc. um daraus Security Requirements ableiten zu können. In dieser Arbeit geht es darum, herauszufinden, welche Möglichkeiten es dazu bisher in der Literatur gibt und wie gut diese auf die spezifischen Aspekte des IIoT anwendbar sind. ', 2, 0, 1, 1, 5, 7),
	(99, 'Aktueller Überblick über die IS-Forschung hinsichtlich Social Sustainability', 'Theoretischer Hintergrund\r\nMethodisches Vorgehen: Literature Review\\Strukturierte Aufarbeitung der aktuellen Forschungsliteratur im Bereich Social Sustainability in der IS-Forschung; Strukturierung anhand geeigneter Parameter (Thema: Menschenrechte, Diversität im Job, etc.; Stakeholder: Mitarbeiter*in, Konsument*in; Rolle von IS/ Umsetzung in Information System)\r\nDiskussion über Potentiale der IS im Bereich social sustainability\r\nEinstiegsliteratur: Schoormann, T., & Kutzner, K. (2020). Towards Understanding Social Sustainability: An Information Systems Research-Perspective. ICIS.', 1, 1, 4, 2, 1, 3),
	(104, 'Developing of interactive data acquisition agents for a compliance-driven continuous maturity assess', 'A capability maturity model (CMM) in the area of information technology is generally focused on development processes and phases within organizations and the involved information systems. They build a sound fundamental base for an evaluation. Therefore, the structure of the model is based on a stepwise progress for improvements. Every step acts as an assessment for the quantity and quality of processes, techniques, and methods within enterprises and systems. Such an assessment can affect all areas of a company and is very time-consuming. Therefore, a comprehensive assessment is usually done only every few years and it is discovered too late if the company have lost capabilities. Within the bachelor thesis, the requirements for interactive data acquisition agents based on compliance requirements have to be determined and prototypically implemented. Information should inserted into a database using the push or pull principle and it should be possible to carry out a daily self-assessment using a given maturity model [1]. Good programming skills in at least one object-oriented programming language and good knowledge of web development are expected. The Bachelor\\\'s thesis can be written in German or English. \r\nhttps://www.researchgate.net/publication/330077045_Towards_a_capability_maturity_model_for_digital_forensic_readiness\r\n', 1, 1, 3, 1, 1, 4),
	(105, 'Funktionserweiterung der Fakultätsapplikation „Masterbewerbung“ von Zend (zf1) in Laminas', 'Bestandteile: Einarbeitung in die bereits implementierten Funktionen, Identifizierung der fehlenden Komponenten, Transformation der Komponenten, Qualitätsanalyse, Fehleranalyse\r\nVoraussetzungen: MySQL, PHP, Linux, Kenntnisse in MVC Systemen', 4, 1, 1, 1, 2, 3),
	(106, 'Förderung von nachhaltigem Handeln durch Gamification', 'Theoretische Einordnung: Gamification, sustainability in information system, etc.\r\nMethode: Literature Review\r\nLiteraturüberblick über die aktuelle Forschung im Bereich Gamification zur Förderung individuell nachhaltiges Handeln: Welche Möglichkeiten der Gamification gibt es, um Individuen zu nachhaltigem Handeln zu motivieren?Aufarbeitung der Literatur zu Ansatzpunkten von Gamification\r\nAufarbeitung der Literatur zu Gamification im Bereich sustainability\r\nAbleitung von offenen Ansatzpunkten / weiteren Möglichkeiten \r\nDiskussion der Umsetzung von weiteren Möglichkeiten\r\nEinstiegsliteratur: Seidler, A. R., Henkel, C., Fiedler, M., Kranz, J., Ixmeier, A., & Strunk, K. S. (2020). Promoting Eco-Sustainable Behavior with Gamification: An Experimental Study on the Alignment of Competing Goals. ICIS 2020.', 1, 1, 1, 2, 5, 3);

-- Exportiere Struktur von Tabelle seminarvergabetool.projekt_mitarbeiter
CREATE TABLE IF NOT EXISTS `projekt_mitarbeiter` (
  `pb_id` int NOT NULL AUTO_INCREMENT,
  `mitarbeiter_ma_id` int DEFAULT NULL,
  `projekt_projekt_id` int DEFAULT NULL,
  PRIMARY KEY (`pb_id`),
  KEY `mitarbeiter_ma_id` (`mitarbeiter_ma_id`),
  KEY `projekt_projekt_id` (`projekt_projekt_id`),
  CONSTRAINT `projekt_mitarbeiter_ibfk_1` FOREIGN KEY (`mitarbeiter_ma_id`) REFERENCES `mitarbeiter` (`ma_id`) ON DELETE CASCADE,
  CONSTRAINT `projekt_mitarbeiter_ibfk_2` FOREIGN KEY (`projekt_projekt_id`) REFERENCES `projekt` (`projekt_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.projekt_mitarbeiter: ~42 rows (ungefähr)
INSERT INTO `projekt_mitarbeiter` (`pb_id`, `mitarbeiter_ma_id`, `projekt_projekt_id`) VALUES
	(1, 132, 85),
	(2, 187, 85),
	(3, 169, 99),
	(7, 169, 95),
	(9, 132, 104),
	(10, 139, 55),
	(11, 188, 94),
	(12, 132, 105),
	(13, 191, 96),
	(15, 176, 66),
	(16, 176, 78),
	(17, 138, 76),
	(19, 139, 65),
	(20, 137, 75),
	(21, 130, 71),
	(22, 191, 77),
	(23, 130, 67),
	(24, 133, 73),
	(25, 141, 68),
	(26, 141, 90),
	(27, 191, 70),
	(28, 138, 64),
	(29, 162, 64),
	(30, 138, 63),
	(31, 162, 63),
	(32, 184, 63),
	(33, 166, 60),
	(34, 166, 62),
	(35, 155, 93),
	(36, 135, 59),
	(37, 125, 57),
	(38, 171, 97),
	(39, 136, 92),
	(40, 192, 92),
	(41, 131, 82),
	(42, 133, 80),
	(43, 192, 98),
	(44, 132, 106),
	(45, 169, 106),
	(46, 189, 86),
	(47, 135, 79),
	(48, 175, 83),
	(49, 132, 99),
	(50, 138, 107),
	(51, 132, 108);

-- Exportiere Struktur von Tabelle seminarvergabetool.student
CREATE TABLE IF NOT EXISTS `student` (
  `stud_id` int NOT NULL AUTO_INCREMENT,
  `nachname` varchar(30) DEFAULT NULL,
  `vorname` varchar(20) DEFAULT NULL,
  `nds` varchar(10) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `matrikelnummer` int DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `gruppe_gruppe_id` int DEFAULT NULL,
  `studiengang_studiengang_id` int DEFAULT NULL,
  PRIMARY KEY (`stud_id`),
  KEY `gruppe_gruppe_id` (`gruppe_gruppe_id`),
  KEY `studiengang_studiengang_id` (`studiengang_studiengang_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`gruppe_gruppe_id`) REFERENCES `gruppe` (`gruppe_id`),
  CONSTRAINT `student_ibfk_2` FOREIGN KEY (`studiengang_studiengang_id`) REFERENCES `studiengang` (`studiengang_id`),
  CONSTRAINT `student_chk_1` CHECK (regexp_like(`nds`,_utf8mb4'^[a-zA-Z0-9]+$')),
  CONSTRAINT `student_chk_2` CHECK ((`email` like _utf8mb4'%@%')),
  CONSTRAINT `student_chk_3` CHECK ((`status` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.student: ~14 rows (ungefähr)
INSERT INTO `student` (`stud_id`, `nachname`, `vorname`, `nds`, `email`, `matrikelnummer`, `status`, `gruppe_gruppe_id`, `studiengang_studiengang_id`) VALUES
	(2, 'Müller', 'Anna', 'ana12345', 'anna.mueller@example.com', 2287303, 1, NULL, 2),
	(3, 'Schmidt', 'Paul', 'pau67890', 'paul.schmidt@example.com', 2287304, 1, NULL, 2),
	(4, 'Keller', 'Julia', 'jul23456', 'julia.keller@example.com', 2287305, 1, NULL, 3),
	(6, 'Bauer', 'Emma', 'emm34567', 'emma.bauer@example.com', 2287307, 1, NULL, 4),
	(7, 'Fischer', 'Leon', 'leo89012', 'leon.fischer@example.com', 2287308, 1, NULL, 4),
	(8, 'Wagner', 'Mia', 'mia45678', 'mia.wagner@example.com', 2287309, 1, NULL, 5),
	(9, 'Becker', 'Noah', 'noa90123', 'noah.becker@example.com', 2287310, 1, NULL, 5),
	(10, 'Hofmann', 'Sophia', 'sop56789', 'sophia.hofmann@example.com', 2287311, 1, NULL, 6),
	(11, 'Schneider', 'Elias', 'eli01234', 'elias.schneider@example.com', 2287312, 1, NULL, 6),
	(12, 'Klein', 'Lina', 'lin67890', 'lina.klein@example.com', 2287313, 1, NULL, 7),
	(13, 'Neumann', 'Ben', 'ben34567', 'ben.neumann@example.com', 2287314, 1, NULL, 7),
	(14, 'Schwarz', 'Lara', 'lar89012', 'lara.schwarz@example.com', 2287315, 1, NULL, 8),
	(15, 'Zimmermann', 'Finn', 'fin12345', 'finn.zimmermann@example.com', 2287316, 1, NULL, 8),
	(17, 'Scharlach', 'Sabrina', 'scs42083', 'Sabrina.Scharlach@stud.uni-regensburg.de', 20876750, NULL, NULL, 3);

-- Exportiere Struktur von Tabelle seminarvergabetool.student_art
CREATE TABLE IF NOT EXISTS `student_art` (
  `stud_art_id` int NOT NULL AUTO_INCREMENT,
  `Art_art_id` int DEFAULT NULL,
  `Student_stud_id` int DEFAULT NULL,
  PRIMARY KEY (`stud_art_id`),
  KEY `Art_art_id` (`Art_art_id`),
  KEY `Student_stud_id` (`Student_stud_id`),
  CONSTRAINT `student_art_ibfk_1` FOREIGN KEY (`Art_art_id`) REFERENCES `art` (`art_id`),
  CONSTRAINT `student_art_ibfk_2` FOREIGN KEY (`Student_stud_id`) REFERENCES `student` (`stud_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.student_art: ~16 rows (ungefähr)
INSERT INTO `student_art` (`stud_art_id`, `Art_art_id`, `Student_stud_id`) VALUES
	(1, 1, 16),
	(2, 2, 16),
	(5, 4, 3),
	(6, 1, 4),
	(10, 5, 13),
	(11, 2, 2),
	(12, 1, 2),
	(13, 4, 17),
	(14, 4, 4),
	(17, 1, 3),
	(21, 3, 8),
	(22, 1, 8),
	(23, 3, 15),
	(24, 5, 15),
	(26, 1, 7),
	(29, 3, 17);

-- Exportiere Struktur von Tabelle seminarvergabetool.studiengang
CREATE TABLE IF NOT EXISTS `studiengang` (
  `studiengang_id` int NOT NULL AUTO_INCREMENT,
  `bezeichnung` varchar(50) DEFAULT NULL,
  `abschluss` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`studiengang_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.studiengang: ~8 rows (ungefähr)
INSERT INTO `studiengang` (`studiengang_id`, `bezeichnung`, `abschluss`) VALUES
	(1, 'Wirtschaftsinformatik', 'Bachelor'),
	(2, 'Informatik', 'Bachelor'),
	(3, 'Data Science', 'Bachelor'),
	(4, 'BWL', 'Bachelor'),
	(5, 'Digital Business', 'Bachelor'),
	(6, 'Wirtschaftsinformatik', 'Master'),
	(7, 'Informatik', 'Master'),
	(8, 'BWL', 'Master');

-- Exportiere Struktur von Tabelle seminarvergabetool.superuser
CREATE TABLE IF NOT EXISTS `superuser` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nds` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.superuser: ~1 rows (ungefähr)
INSERT INTO `superuser` (`id`, `nds`) VALUES
	(1, 'hom06921');

-- Exportiere Struktur von Tabelle seminarvergabetool.wahl
CREATE TABLE IF NOT EXISTS `wahl` (
  `wahl_id` int NOT NULL AUTO_INCREMENT,
  `prio` int DEFAULT NULL,
  `student_stud_id` int DEFAULT NULL,
  `projekt_projekt_id` int DEFAULT NULL,
  `art_art_id` int DEFAULT NULL,
  PRIMARY KEY (`wahl_id`),
  KEY `student_stud_id` (`student_stud_id`),
  KEY `projekt_projekt_id` (`projekt_projekt_id`),
  KEY `wahl_ibfk_3` (`art_art_id`),
  CONSTRAINT `wahl_ibfk_1` FOREIGN KEY (`student_stud_id`) REFERENCES `student` (`stud_id`) ON DELETE CASCADE,
  CONSTRAINT `wahl_ibfk_2` FOREIGN KEY (`projekt_projekt_id`) REFERENCES `projekt` (`projekt_id`) ON DELETE RESTRICT,
  CONSTRAINT `wahl_ibfk_3` FOREIGN KEY (`art_art_id`) REFERENCES `art` (`art_id`)
) ENGINE=InnoDB AUTO_INCREMENT=218 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportiere Daten aus Tabelle seminarvergabetool.wahl: ~27 rows (ungefähr)
INSERT INTO `wahl` (`wahl_id`, `prio`, `student_stud_id`, `projekt_projekt_id`, `art_art_id`) VALUES
	(30, 1, 3, 92, 4),
	(31, 2, 3, 94, 4),
	(32, 3, 3, 62, 4),
	(33, 1, 4, 55, 1),
	(34, 2, 4, 67, 1),
	(35, 3, 4, 66, 1),
	(66, 1, 13, 80, 5),
	(67, 2, 13, 98, 5),
	(68, 3, 13, 82, 5),
	(162, 1, 2, 63, 2),
	(163, 2, 2, 60, 2),
	(164, 3, 2, 105, 2),
	(165, 1, 2, 67, 1),
	(166, 2, 2, 76, 1),
	(167, 3, 2, 68, 1),
	(188, 1, 8, 68, 1),
	(189, 2, 8, 99, 1),
	(190, 3, 8, 76, 1),
	(203, 1, 15, 78, 3),
	(204, 2, 15, 59, 3),
	(205, 3, 15, 90, 3),
	(206, 1, 15, 80, 5),
	(207, 2, 15, 98, 5),
	(208, 3, 15, 79, 5),
	(212, 1, 7, 68, 1),
	(213, 2, 7, 75, 1),
	(214, 3, 7, 99, 1),
	(215, 1, 17, 92, 4),
	(216, 2, 17, 94, 4),
	(217, 3, 17, 64, 4);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
