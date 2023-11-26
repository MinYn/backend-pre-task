CREATE TABLE `label` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `contacts` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `profile_picture` varchar(200) NOT NULL,
    `name` varchar(50) NOT NULL,
    `email` varchar(100) NOT NULL,
    `tel` varchar(50) NOT NULL,
    `company` varchar(50) DEFAULT NULL,
    `grade` varchar(50) DEFAULT NULL,
    `note` varchar(50) DEFAULT NULL,
    `address` varchar(200) DEFAULT NULL,
    `birthday` date DEFAULT NULL,
    `website` varchar(200) DEFAULT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `contacts_labels` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `contact_id` bigint(20) NOT NULL,
    `label_id` bigint(20) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique_contact_label` (`contact_id`,`label_id`),
    KEY `contacts_labels_label_id_b5d263e3_fk_label_id` (`label_id`),
    CONSTRAINT `contacts_labels_contact_id_89aa11b3_fk_contacts_id` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`id`),
    CONSTRAINT `contacts_labels_label_id_b5d263e3_fk_label_id` FOREIGN KEY (`label_id`) REFERENCES `label` (`id`)
);