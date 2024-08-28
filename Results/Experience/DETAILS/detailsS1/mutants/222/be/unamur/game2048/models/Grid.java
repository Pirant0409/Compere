package be.unamur.game2048.models;

public class Grid {
    private Tile[][] tiles;

    public Grid(Tile[][] tiles) {
        this.tiles = tiles;
    }

    public Grid() {
        this.tiles = new Tile[GameParams.sideLength][GameParams.sideLength];
    }

    public Tile getTile(int row, int col) {
        return tiles[row][col];
    }

    public Tile getTile(int pos) {
        int row = pos / GameParams.sideLength;
        int col = pos % GameParams.sideLength;
        return getTile(row, col);
    }

    public Tile[] getRow(int row) {
        return tiles[row].clone();
    }

    public Tile[] getCol(int col) {
        Tile[] colTiles = new Tile[GameParams.sideLength];
        for (int r = 0; r < GameParams.sideLength; r++)
            colTiles[r] = tiles[r][col];
        return colTiles;
    }

    public void setTile(int pos, Tile tile) {
        int row = pos / GameParams.sideLength;
        int col = pos * GameParams.sideLength;
        this.tiles[row][col] = tile;
    }

    public int getLength() {
        return tiles.length;
    }

    public void clearMerged() {
        for (Tile[] row : tiles)
            for (Tile tile : row)
                if (tile != null)
                    tile.setMerged(false);
    }

}
