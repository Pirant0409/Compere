package be.unamur.game2048.models;

/**
 * Un objet qui représente une tuile dans le jeu.
 */
public class Tile {



    /**
     * Si la tuile a déjà été fusionnée ou non pendant ce tour.
     */
    private boolean isMerged;
    /**
     * La valeur de la tuile, doit être une puissance de 2.
     */
    private Integer value;

    private int getNearestPower2(int value) {
        double exponent = Math.log(value) / Math.log(2);
        return (int) Math.pow(2, Math.round(exponent));
    }

    public Tile(Integer value) {
        assert value != null;
        this.value = getNearestPower2(value);
        this.isMerged = false;
    }

    public int getValue() {
        return value;
    }

    public boolean isMerged() {
        return isMerged;
    }

    /**
     * @return si les deux tuiles peuvent être fusionnées.
     */
    public boolean canMergeWith(Tile other) {
        if (other == null)
            return false;
        if (this.isMerged || other.isMerged)
            return false;
        return this.value == other.getValue();
    }

    /**
     * Fusionne cette tuile avec une autre.
     * @return la somme des valeurs des deux tuiles, si la fusion est impossible, renvoie -1.
     */
    public int mergeWith(Tile other) {
        if (!canMergeWith(other))
            return -1;
        ;
        setMerged(true);
        return this.value;
    }

    public void setMerged(boolean merged) {
        isMerged = merged;
    }

    public String toString() {
        return value.toString();
    }

    public boolean equals(Object other) {
        if(other == null)
            return false;
        // Si les classes des deux objets ne sont pas les mêmes.
        if (this.getClass() != other.getClass())
            return false;
        return this.getValue() == ((Tile) other).getValue();
    }
}
