import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.Color;
import java.io.*;
import java.util.*;

import javax.swing.*;

// Damit Objekte der Klasse BeispielListener
// zum ActionListener werden kann, muss das Interface
// ActionListener implementiert werden
public class auswahlDialog extends JFrame implements ActionListener {
    JButton abbrechenButton;
    JButton bestätigenButton;

    JPanel mainPanel;
    JPanel topPanel;
    JPanel centerPanel;
    JPanel buttonPanel;

    JScrollPane scrollPane;

    JLabel nickLabel = new JLabel("Kürzel : ", SwingConstants.CENTER);
    JLabel anredeLabel = new JLabel("Anrede : ", SwingConstants.CENTER);
    JLabel vornameLabel = new JLabel("Vorname : ", SwingConstants.CENTER);
    JLabel nachnameLabel = new JLabel("Nachname : ", SwingConstants.CENTER);
    JLabel stadtLabel = new JLabel("Stadt : ", SwingConstants.CENTER);
    JLabel plzLabel = new JLabel("Postleitzahl : ", SwingConstants.CENTER);
    JLabel straßeLabel = new JLabel("Straße : ", SwingConstants.CENTER);
    JLabel hausnummerLabel = new JLabel("Hausnummer : ", SwingConstants.CENTER);
    JLabel kundennummerLabel = new JLabel("Kundennummer : ", SwingConstants.CENTER);

    ArrayList<JCheckBox> checkBox = new ArrayList<JCheckBox>();

    public auswahlDialog() {
        this.setTitle("Kunde auswählen");
        mainPanel = new JPanel();
        topPanel = new JPanel();
        centerPanel = new JPanel();
        buttonPanel = new JPanel();

        mainPanel.setLayout(new java.awt.BorderLayout());
        centerPanel.setLayout(new javax.swing.BoxLayout(centerPanel, javax.swing.BoxLayout.Y_AXIS));
        topPanel.setLayout(new java.awt.GridLayout(1, 10));

        scrollPane = new JScrollPane(centerPanel);

        abbrechenButton = new JButton("Abbrechen");
        bestätigenButton = new JButton("Bestätigen");

        abbrechenButton.addActionListener(this);
        bestätigenButton.addActionListener(this);

        topPanel.add(nickLabel);
        topPanel.add(anredeLabel);
        topPanel.add(vornameLabel);
        topPanel.add(nachnameLabel);
        topPanel.add(stadtLabel);
        topPanel.add(plzLabel);
        topPanel.add(straßeLabel);
        topPanel.add(hausnummerLabel);
        topPanel.add(kundennummerLabel);
        topPanel.add(new JLabel());

        buttonPanel.add(bestätigenButton);
        buttonPanel.add(abbrechenButton);

        try {

            BufferedReader reader = new BufferedReader(new FileReader("Kunden.csv"));
            String line = reader.readLine();
            int lineNumber = 0;

            while (line != null) {

                JPanel linePanel = new JPanel();
                linePanel.setLayout(new java.awt.GridLayout(1, 10));
                linePanel.setSize(1600, 90);

                String[] lineElements = line.split(",");

                for (int i = 0; i < lineElements.length; i++) {
                    JLabel tempLabel = new JLabel(lineElements[i], SwingConstants.CENTER);
                    tempLabel.setSize(160, 90);
                    tempLabel.setBorder(BorderFactory.createLineBorder(Color.BLACK, 1));
                    linePanel.add(tempLabel);
                }

                checkBox.add(lineNumber, new JCheckBox());
                linePanel.add(checkBox.get(lineNumber++));

                centerPanel.add(linePanel);

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

        this.setSize(1600, 900);
    }

    @Override
    public void actionPerformed(ActionEvent ae) {

        if (ae.getSource() == this.abbrechenButton) {
            this.dispose();
        } else if (ae.getSource() == this.bestätigenButton) {

            // Bestätigungsfenster
            JDialog d = new JDialog();
            d.setTitle("Auswahl bestätigt");
            d.add(new JLabel("Rechnung wird erstellt", SwingConstants.CENTER));
            d.setSize(320, 180);
            d.setLocationRelativeTo(null);
            d.setVisible(true);

            // Erstellen der Rechnung

            // String templateName = "Rechnungsvorlage.docx";
            // HashMap<String, String> substitutionData = new HashMap<String, String>();
            // substitutionData.put("#{Anrede}", "Herr");
            // DocxManipulator.generateAndSendDocx(templateName, substitutionData);

            // Document doc = new Document("TEMPLATES_DIRECTORY/Rechnungsvorlage.docx");

            // doc.getRange().replace("#{Anrede}", "Herr", new FindReplaceOptions(FindReplaceDirection.FORWARD));

            // doc.save("neueRechnung.docx");

            this.dispose();
        }

    }
}