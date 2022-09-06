import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;

// Damit Objekte der Klasse BeispielListener
// zum ActionListener werden kann, muss das Interface
// ActionListener implementiert werden
public class VerwaltungListener extends JFrame implements ActionListener {
    JButton neuerKundeButton;
    JButton rechnungButton;
    JPanel panel;

    // erzeugt zwei Button
    // je nachdem ob man einen neuen Kunden hinzufügen oder eine Rechnung erstellen
    // möchte
    public VerwaltungListener() {
        this.setTitle("Fewo Kundenverwaltung by Rayk Kretzschmar");
        this.setSize(1600, 900);
        panel = new JPanel();

        neuerKundeButton = new JButton("neuer Kunde");
        rechnungButton = new JButton("Rechnung erstellen");

        neuerKundeButton.addActionListener(this);
        rechnungButton.addActionListener(this);

        panel.add(neuerKundeButton, java.awt.BorderLayout.CENTER);
        panel.add(rechnungButton, java.awt.BorderLayout.CENTER);

        this.add(panel);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
    }

    @Override
    public void actionPerformed(ActionEvent ae) {
        if (ae.getSource() == this.neuerKundeButton) {
            neuerKundeDialog kd = new neuerKundeDialog();
            kd.setVisible(true);
        } else if (ae.getSource() == this.rechnungButton) {
            // Kunden auswählen und dann Rechnung erstellen
            auswahlDialog ad = new auswahlDialog();
            ad.setVisible(true);
        }

    }
}