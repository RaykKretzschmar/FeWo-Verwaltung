import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import javax.swing.*;

// Damit Objekte der Klasse BeispielListener
// zum ActionListener werden kann, muss das Interface
// ActionListener implementiert werden
public class neuerKundeDialog extends JFrame implements ActionListener {
    JButton speichernButton;
    JButton abbrechenButton;
    JPanel mainPanel;
    JPanel panel;
    JPanel buttonPanel;

    JPanel nickPanel = new JPanel();
    JPanel anredePanel = new JPanel();
    JPanel vornamePanel = new JPanel();
    JPanel nachnamePanel = new JPanel();
    JPanel stadtPanel = new JPanel();
    JPanel plzPanel = new JPanel();
    JPanel straßePanel = new JPanel();
    JPanel hausnummerPanel = new JPanel();
    JPanel kundennummerPanel = new JPanel();

    JPanel nickTextPanel = new JPanel();
    JPanel anredeTextPanel = new JPanel();
    JPanel vornameTextPanel = new JPanel();
    JPanel nachnameTextPanel = new JPanel();
    JPanel stadtTextPanel = new JPanel();
    JPanel plzTextPanel = new JPanel();
    JPanel straßeTextPanel = new JPanel();
    JPanel hausnummerTextPanel = new JPanel();
    JPanel kundennummerTextPanel = new JPanel();

    JLabel nickLabel = new JLabel("Kürzel : ", SwingConstants.RIGHT);
    JLabel anredeLabel = new JLabel("Anrede : ", SwingConstants.RIGHT);
    JLabel vornameLabel = new JLabel("Vorname : ", SwingConstants.RIGHT);
    JLabel nachnameLabel = new JLabel("Nachname : ", SwingConstants.RIGHT);
    JLabel stadtLabel = new JLabel("Stadt : ", SwingConstants.RIGHT);
    JLabel plzLabel = new JLabel("Postleitzahl : ", SwingConstants.RIGHT);
    JLabel straßeLabel = new JLabel("Straße : ", SwingConstants.RIGHT);
    JLabel hausnummerLabel = new JLabel("Hausnummer : ", SwingConstants.RIGHT);
    JLabel kundennummerLabel = new JLabel("Kundennummer : ", SwingConstants.RIGHT);

    JTextField nickTextField = new JTextField(20);
    JTextField anredeTextField = new JTextField(20);
    JTextField vornameTextField = new JTextField(20);
    JTextField nachnameTextField = new JTextField(20);
    JTextField stadtTextField = new JTextField(20);
    JTextField plzTextField = new JTextField(20);
    JTextField straßeTextField = new JTextField(20);
    JTextField hausnummerTextField = new JTextField(20);
    JTextField kundennummerTextField = new JTextField(20);

    public neuerKundeDialog() {
        this.setTitle("Neuer Kunde");
        this.setSize(1600, 900);
        mainPanel = new JPanel();
        panel = new JPanel();
        buttonPanel = new JPanel();

        mainPanel.setLayout(new java.awt.BorderLayout());
        panel.setLayout(new java.awt.GridLayout(9, 3));

        speichernButton = new JButton("Speichern");
        abbrechenButton = new JButton("Abbrechen");

        speichernButton.addActionListener(this);
        abbrechenButton.addActionListener(this);

        nickTextPanel.setSize(200, 20);
        anredeTextPanel.setSize(200, 20);
        vornameTextPanel.setSize(200, 20);
        nachnameTextPanel.setSize(200, 20);
        stadtTextPanel.setSize(200, 20);
        plzTextPanel.setSize(200, 20);
        straßeTextPanel.setSize(200, 20);
        hausnummerTextPanel.setSize(200, 20);
        kundennummerTextPanel.setSize(200, 20);

        nickPanel.setLayout(new java.awt.BorderLayout());
        anredePanel.setLayout(new java.awt.BorderLayout());
        vornamePanel.setLayout(new java.awt.BorderLayout());
        nachnamePanel.setLayout(new java.awt.BorderLayout());
        stadtPanel.setLayout(new java.awt.BorderLayout());
        plzPanel.setLayout(new java.awt.BorderLayout());
        straßePanel.setLayout(new java.awt.BorderLayout());
        hausnummerPanel.setLayout(new java.awt.BorderLayout());
        kundennummerPanel.setLayout(new java.awt.BorderLayout());

        nickTextPanel.add(nickTextField);
        anredeTextPanel.add(anredeTextField);
        vornameTextPanel.add(vornameTextField);
        nachnameTextPanel.add(nachnameTextField);
        stadtTextPanel.add(stadtTextField);
        plzTextPanel.add(plzTextField);
        straßeTextPanel.add(straßeTextField);
        hausnummerTextPanel.add(hausnummerTextField);
        kundennummerTextPanel.add(kundennummerTextField);

        nickPanel.add(nickTextPanel, java.awt.BorderLayout.CENTER);
        anredePanel.add(anredeTextPanel, java.awt.BorderLayout.CENTER);
        vornamePanel.add(vornameTextPanel, java.awt.BorderLayout.CENTER);
        nachnamePanel.add(nachnameTextPanel, java.awt.BorderLayout.CENTER);
        stadtPanel.add(stadtTextPanel, java.awt.BorderLayout.CENTER);
        plzPanel.add(plzTextPanel, java.awt.BorderLayout.CENTER);
        straßePanel.add(straßeTextPanel, java.awt.BorderLayout.CENTER);
        hausnummerPanel.add(hausnummerTextPanel, java.awt.BorderLayout.CENTER);
        kundennummerPanel.add(kundennummerTextPanel, java.awt.BorderLayout.CENTER);

        panel.add(nickLabel);
        panel.add(nickPanel);
        panel.add(new JLabel());
        panel.add(anredeLabel);
        panel.add(anredePanel);
        panel.add(new JLabel());
        panel.add(vornameLabel);
        panel.add(vornamePanel);
        panel.add(new JLabel());
        panel.add(nachnameLabel);
        panel.add(nachnamePanel);
        panel.add(new JLabel());
        panel.add(stadtLabel);
        panel.add(stadtPanel);
        panel.add(new JLabel());
        panel.add(plzLabel);
        panel.add(plzPanel);
        panel.add(new JLabel());
        panel.add(straßeLabel);
        panel.add(straßePanel);
        panel.add(new JLabel());
        panel.add(hausnummerLabel);
        panel.add(hausnummerPanel);
        panel.add(new JLabel());
        panel.add(kundennummerLabel);
        panel.add(kundennummerPanel);

        buttonPanel.add(speichernButton);
        buttonPanel.add(abbrechenButton);

        mainPanel.add(panel, java.awt.BorderLayout.CENTER);
        mainPanel.add(buttonPanel, java.awt.BorderLayout.PAGE_END);

        this.add(mainPanel);
    }

    @Override
    public void actionPerformed(ActionEvent ae) {
        // Die Quelle wird mit getSource() abgefragt und mit den
        // Buttons abgeglichen. Wenn die Quelle des ActionEvents einer
        // der Buttons ist, wird der Text des JLabels entsprechend geändert
        if (ae.getSource() == this.speichernButton) {
            try {
                BufferedWriter bw = new BufferedWriter(new FileWriter("Kunden.csv", true));
                bw.write(nickTextField.getText() + ",");
                bw.write(anredeTextField.getText() + ",");
                bw.write(vornameTextField.getText() + ",");
                bw.write(nachnameTextField.getText() + ",");
                bw.write(stadtTextField.getText() + ",");
                bw.write(plzTextField.getText() + ",");
                bw.write(straßeTextField.getText() + ",");
                bw.write(hausnummerTextField.getText() + ",");
                bw.write(kundennummerTextField.getText());
                bw.newLine();
                bw.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
            this.dispose();
        } else if (ae.getSource() == this.abbrechenButton) {
            this.dispose();
        }

    }
}
