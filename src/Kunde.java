public class Kunde {
    /**
     * Kürzel
     */
    private String nickname = "neuer Kunde";

    public String getNickname() {
        return nickname;
    }

    public void setNickname(String nickname) {
        this.nickname = nickname;
    }

    /**
     * Anrede
     */
    private String anrede;

    public String getAnrede() {
        return anrede;
    }

    public void setAnrede(String anrede) {
        this.anrede = anrede;
    }

    /**
     * Vorname
     */
    private String vorname;

    public String getVorname() {
        return vorname;
    }

    public void setVorname(String vorname) {
        this.vorname = vorname;
    }

    /**
     * Nachname
     */
    private String nachname;

    public String getNachname() {
        return nachname;
    }

    public void setNachname(String nachname) {
        this.nachname = nachname;
    }

    /**
     * Stadt
     */
    private String stadt;

    public String getStadt() {
        return stadt;
    }

    public void setStadt(String stadt) {
        this.stadt = stadt;
    }

    /**
     * Postleitzahl
     */
    private String plz;

    public String getPlz() {
        return plz;
    }

    public void setPlz(String plz) {
        this.plz = plz;
    }

    /**
     * Straße
     */
    private String straße;

    public String getStraße() {
        return straße;
    }

    public void setStraße(String straße) {
        this.straße = straße;
    }

    /**
     * Hausnummer
     */
    private String hausnummer;

    public String getHausnummer() {
        return hausnummer;
    }

    public void setHausnummer(String hausnummer) {
        this.hausnummer = hausnummer;
    }

    /**
     * Kundennummer
     */
    private String kundennummer;

    public String getKundennummer() {
        return kundennummer;
    }

    public void setKundennummer(String kundennummer) {
        this.kundennummer = kundennummer;
    }

    /**
     * class contructor
     */
    public Kunde() {
        setNickname("Nickname");
        setAnrede("Anrede");
        setVorname("Vorname");
        setNachname("Nachname");
        setStadt("Stadt");
        setPlz("PLZ");
        setStraße("Straße");
        setHausnummer("Hausnummer");
        setKundennummer("Kundennummer");
    }

    /**
     * class constructor
     * 
     * @param nickname
     * @param anrede
     * @param vorname
     * @param nachname
     * @param stadt
     * @param plz
     * @param straße
     * @param hausnummer
     * @param kundennummer
     */
    public Kunde(String nickname, String anrede, String vorname, String nachname, String stadt, String plz,
            String straße, String hausnummer, String kundennummer) {
        setNickname(nickname);
        setAnrede(anrede);
        setVorname(vorname);
        setNachname(nachname);
        setStadt(stadt);
        setPlz(plz);
        setStraße(straße);
        setHausnummer(hausnummer);
        setKundennummer(kundennummer);
    }

}