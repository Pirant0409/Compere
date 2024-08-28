package be.unamur.game2048.controllers;

import be.unamur.game2048.models.GameParams;
import be.unamur.game2048.models.GameState;
import be.unamur.game2048.models.Grid;
import be.unamur.game2048.models.Tile;

import java.util.ArrayList;
import java.util.List;

public class GameController {

    private Grid grid;

    public Grid getGrid() {
        return grid;
    }

    private GameState gamestate = GameState.start;

    public GameState getGamestate() {
        return gamestate;
    }

    private int highestScore;

    public int getHighestScore() {
        return highestScore;
    }

    private int score;

    public int getScore() {
        return score;
    }

    private int tileAdded = 0;

    /**
     * Démarre le jeu avec une grille vide remplie d'un certain nombre de tuiles.
     */
    public void startGame() {
        if (gamestate != GameState.running) {
            resetData();
            grid = new Grid();
            for (int n = 0; n < GameParams.nbStartTileFilled; n++) {
                fillFirstEmptyTile();
            }
        }
    }

    /**
     * Démarre le jeu avec une grille déjà établie.
     */
    public void startGame(Tile[][] tiles) {
        if (gamestate != GameState.running) {
            resetData();
            this.grid = new Grid(tiles);
        }
    }

    private void resetData() {
        score = 0;
        highestScore = (-1);
        gamestate = GameState.running;
        tileAdded = 0;
    }

    /**
     * Remplis la première tuile vide en partant du haut à gauche dans la grille.
     */
    public boolean fillFirstEmptyTile() {
        for (int pos = 0; pos < GameParams.sideLength * GameParams.sideLength; pos++) {
            if (grid.getTile(pos) == null) {
                int val = 2;
                if (this.tileAdded >= 0 && this.tileAdded % 10 == 0)
                    val = 4;
                grid.setTile(pos, new Tile(val));
                tileAdded++;
                return true;
            }
        }
        return false;
    }

    public boolean moveUp(boolean checkingAvailableMoves) {
        return move(12, 15, 1, -4, checkingAvailableMoves);
    }

    public boolean moveDown(boolean checkingAvailableMoves) {
        return move(0, 3, 1, 4, checkingAvailableMoves);
    }

    public boolean moveLeft(boolean checkingAvailableMoves) {
        return move(3, 15, 4, -1, checkingAvailableMoves);
    }

    public boolean moveRight(boolean checkingAvailableMoves) {
        return move(0, 12, 4, 1, checkingAvailableMoves);
    }

    /**
     * CONSEIL : Ne perdez pas de temps à essayer de comprendre l'algorithme, faites plutôt du blackboxtesting ici.
     * Imaginez plutôt comment un mouvement dans une direction peut changer la grille.
     *
     * @param checkingAvailableMoves spécifie si on vérifie simplement si le mouvement est possible ou si on doit l'exécuter.
     * @return Vrai lorsque le mouvement est possible, faux sinon.
     */
    private boolean move(int firstStartPos, int lastStartPos, int startPosIncr, int nextPosIncr, boolean checkingAvailableMoves) {
        if (gamestate != GameState.running)
            return false;
        boolean hasMoved = false;
        for (int startPos = firstStartPos; startPos <= lastStartPos; startPos += startPosIncr) {
            List<int[]> history = new ArrayList<>();
            for (int step = GameParams.sideLength - 1; step > 0; step--) {
                int pos = startPos + (step - 1) * nextPosIncr;
                int nextPos = startPos + step * nextPosIncr;
                history.add(0, new int[]{pos, nextPos});
                if (grid.getTile(pos) == null)
                    continue;
                for (int[] positions : history) {
                    pos = positions[0];
                    nextPos = positions[1];
                    Tile next = grid.getTile(nextPos);
                    Tile curr = grid.getTile(pos);
                    boolean canMove = next == null || next.canMergeWith(curr);
                    if (checkingAvailableMoves && canMove)
                        return true;
                    if (!canMove)
                        continue;
                    if (next == null) {
                        grid.setTile(nextPos, curr);
                    } else if (next.canMergeWith(curr)) {
                        int value = next.mergeWith(curr);
                        updateScore(value);
                    }
                    grid.setTile(pos, null);
                    hasMoved = true;
                }
            }
        }

        if (hasMoved) {
            afterMove();
        }

        return hasMoved;
    }

    public void updateScore(int value) {
        if (value > highestScore)
            highestScore = value;
        score += value;
    }

    public void clearMerged() {
        grid.clearMerged();
    }

    private void afterMove() {
        if (highestScore < GameParams.scoreTarget) {
            clearMerged();
            fillFirstEmptyTile();
            if (!movesAvailable()) {
                gamestate = GameState.over;
            }
        } else if (highestScore == GameParams.scoreTarget)
            gamestate = GameState.won;
    }

    /**
     * Vérifie si on peut bouger.
     */
    boolean movesAvailable() {
        return moveUp(true) || moveDown(true) || moveLeft(true) || moveRight(true);
    }

}
