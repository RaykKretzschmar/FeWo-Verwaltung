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

        panel.add(nickLabel);
        panel.add(nickTextField);
        panel.add(new JLabel());
        panel.add(anredeLabel);
        panel.add(anredeTextField);
        panel.add(new JLabel());
        panel.add(vornameLabel);
        panel.add(vornameTextField);
        panel.add(new JLabel());
        panel.add(nachnameLabel);
        panel.add(nachnameTextField);
        panel.add(new JLabel());
        panel.add(stadtLabel);
        panel.add(stadtTextField);
        panel.add(new JLabel());
        panel.add(plzLabel);
        panel.add(plzTextField);
        panel.add(new JLabel());
        panel.add(straßeLabel);
        panel.add(straßeTextField);
        panel.add(new JLabel());
        panel.add(hausnummerLabel);
        panel.add(hausnummerTextField);
        panel.add(new JLabel());
        panel.add(kundennummerLabel);
        panel.add(kundennummerTextField);
        panel.add(new JLabel());

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
