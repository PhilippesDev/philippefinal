<?php
// Vérifier si le formulaire a été soumis
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Vérifier si tous les champs requis sont remplis
    if (isset($_POST['name']) && isset($_POST['email']) && isset($_POST['subject']) && isset($_POST['message'])) {
        // Récupérer les données du formulaire
        $name = $_POST['name'];
        $email = $_POST['email'];
        $subject = $_POST['subject'];
        $message = $_POST['message'];

        // Connexion à la base de données SQLite
        $db = new SQLite3('base.db');

        // Vérifier si la connexion a réussi
        if (!$db) {
            die("La connexion à la base de données a échoué");
        }

        // Préparer la requête SQL pour insérer les données dans la table appropriée
        $stmt = $db->prepare("INSERT INTO formulaire (nom, email, sujet, message) VALUES (:nom, :email, :sujet, :message)");
        $stmt->bindValue(':nom', $name);
        $stmt->bindValue(':email', $email);
        $stmt->bindValue(':sujet', $subject);
        $stmt->bindValue(':message', $message);

        // Exécuter la requête SQL
        $result = $stmt->execute();

        // Vérifier si l'insertion a réussi
        if ($result) {
            // Afficher un message de succès
            echo "Votre message a été sauvegardé avec succès dans la base de données.";
        } else {
            // Afficher un message d'erreur
            echo "Une erreur s'est produite lors de l'enregistrement de votre message dans la base de données.";
        }

        // Fermer la connexion à la base de données
        $db->close();
    } else {
        // Afficher un message d'erreur si des champs requis sont manquants
        echo "Tous les champs du formulaire sont obligatoires.";
    }
}
?>
