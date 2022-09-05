import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;

// Damit Objekte der Klasse BeispielListener
// zum ActionListener werden kann, muss das Interface
// ActionListener implementiert werden
public class VerwaltungListener extends JFrame implements ActionListener {
    JButton neuerKundeButton;
    JButton auswaehlenKundeButton;
    JPanel panel;

    public VerwaltungListener() {
        this.setTitle("Fewo Kundenverwaltung by Rayk Kretzschmar");
        this.setSize(1600, 900);
        panel = new JPanel();

        neuerKundeButton = new JButton("neuer Kunde");
        auswaehlenKundeButton = new JButton("Kunde auswählen");

        neuerKundeButton.addActionListener(this);
        auswaehlenKundeButton.addActionListener(this);

        panel.add(neuerKundeButton);
        panel.add(auswaehlenKundeButton);

        this.add(panel);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
    }

    @Override
    public void actionPerformed(ActionEvent ae) {
        // Die Quelle wird mit getSource() abgefragt und mit den
        // Buttons abgeglichen. Wenn die Quelle des ActionEvents einer
        // der Buttons ist, wird der Text des JLabels entsprechend geändert
        if (ae.getSource() == this.neuerKundeButton) {
            neuerKundeDialog kd = new neuerKundeDialog();
            kd.setVisible(true);
        } else if (ae.getSource() == this.auswaehlenKundeButton) {
            // hole eine Liste aller Kunden und zeige sie in einem Fenster
            // Kunden auswählen und dann Rechnung erstellen
            auswahlDialog ad = new auswahlDialog();
            ad.setVisible(true);
        }

    }
}