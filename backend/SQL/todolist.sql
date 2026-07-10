-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : ven. 10 juil. 2026 à 08:52
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `todolist`
--

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

CREATE TABLE `categories` (
  `id_categories` int(11) NOT NULL,
  `nom_categorie` varchar(50) NOT NULL,
  `created_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `categories`
--

INSERT INTO `categories` (`id_categories`, `nom_categorie`, `created_by`) VALUES
(1, 'Etude', 3),
(2, 'Personnel', 3);

-- --------------------------------------------------------

--
-- Structure de la table `historique`
--

CREATE TABLE `historique` (
  `id_historique` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `historique`
--

INSERT INTO `historique` (`id_historique`, `user_id`, `action`, `timestamp`) VALUES
(1, 1, 'Creation du compte', '2026-07-09 18:07:54'),
(2, 1, 'Connexion', '2026-07-09 18:08:40'),
(3, 1, 'Connexion', '2026-07-09 18:16:15'),
(4, 1, 'Creation de la tache #1', '2026-07-09 18:16:33'),
(5, 1, 'Modification de la tache #1', '2026-07-09 18:16:48'),
(6, 1, 'Connexion', '2026-07-09 18:19:08'),
(7, 1, 'Connexion', '2026-07-09 18:30:30'),
(8, 1, 'Connexion', '2026-07-09 19:36:03'),
(9, 1, 'Connexion', '2026-07-09 19:39:21'),
(10, 2, 'Creation du compte', '2026-07-09 19:48:05'),
(11, 1, 'Connexion', '2026-07-10 04:45:09'),
(12, 1, 'Connexion', '2026-07-10 05:04:46'),
(13, 1, 'Connexion', '2026-07-10 05:12:42'),
(14, 1, 'Suppression de la tache #1', '2026-07-10 05:12:55'),
(15, 1, 'Creation de la tache #2', '2026-07-10 05:14:34'),
(16, 1, 'Connexion', '2026-07-10 05:38:19'),
(17, 3, 'Creation du compte', '2026-07-10 05:38:52'),
(18, 3, 'Connexion', '2026-07-10 05:39:06'),
(19, 3, 'Modification de la tache #2', '2026-07-10 05:42:22'),
(20, 3, 'Connexion', '2026-07-10 05:47:06'),
(21, 3, 'Modification de la tache #2', '2026-07-10 05:47:23'),
(22, 3, 'Connexion', '2026-07-10 05:52:50'),
(23, 3, 'Connexion', '2026-07-10 05:58:17'),
(24, 3, 'Connexion', '2026-07-10 06:03:51'),
(25, 3, 'Connexion', '2026-07-10 06:31:02'),
(26, 3, 'Connexion', '2026-07-10 06:34:58'),
(27, 3, 'Connexion', '2026-07-10 06:46:55'),
(28, 3, 'Creation de la tache #3', '2026-07-10 06:47:32'),
(29, 3, 'Modification de la tache #2', '2026-07-10 06:48:18'),
(30, 3, 'Creation de la tache #4', '2026-07-10 06:48:56'),
(31, 3, 'Suppression de la tache #4', '2026-07-10 06:49:18');

-- --------------------------------------------------------

--
-- Structure de la table `taches`
--

CREATE TABLE `taches` (
  `id_tache` int(11) NOT NULL,
  `titre` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `priority` enum('basse','moyenne','haute') DEFAULT 'moyenne',
  `statut` enum('a_faire','en_cours','termine') DEFAULT 'a_faire',
  `due_date` date DEFAULT NULL,
  `categorie_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `assigned_to` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `taches`
--

INSERT INTO `taches` (`id_tache`, `titre`, `description`, `priority`, `statut`, `due_date`, `categorie_id`, `created_by`, `assigned_to`, `created_at`) VALUES
(2, 'Projet Symfony', 'gAAAAABqUJWyB0xbOOkZS9j0vBVfIHOoRKDaEdBhBrpuGvebJr57Csk7m9lIG8mGfcv5U5v5248HInzAT8Br40ggZsCBdx248RwYVdi6_x3YMGJZsDmvBd0=', 'haute', 'a_faire', '2026-07-16', NULL, 1, 1, '2026-07-10 05:14:34'),
(3, 'Révision', 'gAAAAABqUJWEUaoJRPyFWU2rYSa9drCTTwbYrCIuCzDNEhcTCp3fQH4HngLvsSEJWvXtTq48NmYxbZMA-Ewp-ZczIvw8YimwaA==', 'haute', 'a_faire', '2026-07-14', 1, 3, 2, '2026-07-10 06:47:32');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `id_utilisateur` int(11) NOT NULL,
  `nom_utilisateur` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`id_utilisateur`, `nom_utilisateur`, `email`, `password_hash`, `role`) VALUES
(1, 'Razafimandimby', 'razafimandimby@gmail.com', 'scrypt:32768:8:1$HxFLf3MXECkX0wIC$292c696d691764beebe4b9fee7408b98cb84aeeff79e6dfeacdbff76f7f64cf8ef5fb453db7849ed4ab987a6c7032654c725f69de3b00242d4167819da89e72a', 'utilisateur'),
(2, 'rasoanaivo', 'rasoanaivo@gmail.com', 'scrypt:32768:8:1$pgZtDutKNDHSyvSc$087eb6c2f494426091ae35265fb7f3747a3051fefe9d7f29be7e3a7ced24237f12f9832a9a7d12f7740cdc1c98a888fc32930e52df481fb157711aeb492ba96d', 'utilisateur'),
(3, 'Mirado', 'mirado@gmail.com', 'scrypt:32768:8:1$Y6oK3IWGpBX7iIaq$9acdf1b9e7e0fe0538f6b4e890d2a96499c0ac36673c3d687f18457a7f41afeae489869ee8241030c12289a193e2ff5a338715382435f2bf8fd3d65175a4739c', 'admin');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id_categories`),
  ADD KEY `created_by` (`created_by`);

--
-- Index pour la table `historique`
--
ALTER TABLE `historique`
  ADD PRIMARY KEY (`id_historique`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `taches`
--
ALTER TABLE `taches`
  ADD PRIMARY KEY (`id_tache`),
  ADD KEY `categorie_id` (`categorie_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `assigned_to` (`assigned_to`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`id_utilisateur`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `categories`
--
ALTER TABLE `categories`
  MODIFY `id_categories` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `historique`
--
ALTER TABLE `historique`
  MODIFY `id_historique` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT pour la table `taches`
--
ALTER TABLE `taches`
  MODIFY `id_tache` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  MODIFY `id_utilisateur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `utilisateur` (`id_utilisateur`);

--
-- Contraintes pour la table `historique`
--
ALTER TABLE `historique`
  ADD CONSTRAINT `historique_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `utilisateur` (`id_utilisateur`);

--
-- Contraintes pour la table `taches`
--
ALTER TABLE `taches`
  ADD CONSTRAINT `taches_ibfk_1` FOREIGN KEY (`categorie_id`) REFERENCES `categories` (`id_categories`),
  ADD CONSTRAINT `taches_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `utilisateur` (`id_utilisateur`),
  ADD CONSTRAINT `taches_ibfk_3` FOREIGN KEY (`assigned_to`) REFERENCES `utilisateur` (`id_utilisateur`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
