/**
 * Kundenverwaltungsprogramm für Ferienwohnungen.
 * 
 * by Rayk Kretzschmar
 */
import java.util.*;
import java.io.*;

import org.apache.pdfbox.pdmodel.*;

//TODO: Firmen als Kunden
public class FewoVerwaltung {
    public static void main(String[] args) throws Exception {
       
        VerwaltungListener v = new VerwaltungListener();
        v.setVisible(true);
    }
}
