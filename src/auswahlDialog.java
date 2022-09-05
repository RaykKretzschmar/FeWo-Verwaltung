import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.Color;
import java.io.*;

import javax.swing.*;

// Damit Objekte der Klasse BeispielListener
// zum ActionListener werden kann, muss das Interface
// ActionListener implementiert werden
public class auswahlDialog extends JFrame implements ActionListener {
    JButton abbrechenButton;

    JPanel mainPanel;
    JPanel topPanel;
    JPanel centerPanel;
    JPanel buttonPanel;

    JLabel nickLabel = new JLabel("Kürzel : ", SwingConstants.CENTER);
    JLabel anredeLabel = new JLabel("Anrede : ", SwingConstants.CENTER);
    JLabel vornameLabel = new JLabel("Vorname : ", SwingConstants.CENTER);
    JLabel nachnameLabel = new JLabel("Nachname : ", SwingConstants.CENTER);
    JLabel stadtLabel = new JLabel("Stadt : ", SwingConstants.CENTER);
    JLabel plzLabel = new JLabel("Postleitzahl : ", SwingConstants.CENTER);
    JLabel straßeLabel = new JLabel("Straße : ", SwingConstants.CENTER);
    JLabel hausnummerLabel = new JLabel("Hausnummer : ", SwingConstants.CENTER);
    JLabel kundennummerLabel = new JLabel("Kundennummer : ", SwingConstants.CENTER);

    public auswahlDialog() {
        this.setTitle("Kunde auswählen");
        this.setSize(1600, 900);
        mainPanel = new JPanel();
        topPanel = new JPanel();
        centerPanel = new JPanel();
        buttonPanel = new JPanel();

        mainPanel.setLayout(new java.awt.BorderLayout());
        centerPanel.setLayout(new java.awt.GridLayout(0, 9));
        topPanel.setLayout(new java.awt.GridLayout(1, 9));

        abbrechenButton = new JButton("Abbrechen");

        abbrechenButton.addActionListener(this);

        topPanel.add(nickLabel);
        topPanel.add(anredeLabel);
        topPanel.add(vornameLabel);
        topPanel.add(nachnameLabel);
        topPanel.add(stadtLabel);
        topPanel.add(plzLabel);
        topPanel.add(straßeLabel);
        topPanel.add(hausnummerLabel);
        topPanel.add(kundennummerLabel);

        buttonPanel.add(abbrechenButton);

        try {

            BufferedReader reader = new BufferedReader(new FileReader("Kunden.csv"));
            String line = reader.readLine();
            while (line != null) {
                String[] lineElements = line.split(",");

                for (int i = 0; i < lineElements.length; i++) {
                    JLabel tempLabel = new JLabel(lineElements[i], SwingConstants.CENTER);
                    tempLabel.setBorder(BorderFactory.createLineBorder(Color.BLACK, 1));
                    centerPanel.add(tempLabel);
                }

                line = reader.readLine();
            }

            reader.close();
        } catch (IOException e) {
            e.getStackTrace();
        }

        mainPanel.add(centerPanel, java.awt.BorderLayout.CENTER);
        mainPanel.add(topPanel, java.awt.BorderLayout.PAGE_START);
        mainPanel.add(buttonPanel, java.awt.BorderLayout.PAGE_END);

        this.add(mainPanel);
    }

    @Override
    public void actionPerformed(ActionEvent ae) {
        // Die Quelle wird mit getSource() abgefragt und mit den
        // Buttons abgeglichen. Wenn die Quelle des ActionEvents einer
        // der Buttons ist, wird der Text des JLabels entsprechend geändert
        if (ae.getSource() == this.abbrechenButton) {

            this.dispose();
        } else if (ae.getSource() == this.abbrechenButton) {
            this.dispose();
        }

    }
}