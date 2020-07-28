import java.util.Arrays;

public class TicTacToe {
    private char[][] board;
    private int turn;

    public TicTacToe() {
        board = new char[3][3];
        for (int i = 0; i < board.length; i++)
        {
            Arrays.fill(board[i], ' ');
        }
        turn = 0;
    }

    public char[][] getBoard() {
        return board;
    }

    public void setNext(int num) {
        int row = (num-1)/3;
        int col = (num-1)%3;
        if (board[row][col] != ' ')
        {
            if (turn == 0)
                turn = 1;
            else
                turn = 0;
            return;
        }
        if (turn == 0)
        {
            board[row][col] = 'X';
            turn = 1;
        }
        else
        {
            board[row][col] = 'O';
            turn = 0;
        }
    }

    public void printBoard() {
        String fin = "";
        for (int i = 0; i < board.length; i++)
        {
            fin += "     |     |     \n";
            fin += "  " + board[i][0] + "  |  " + board[i][1] + "  |  " + board[i][2] +  " \n";
            if (i != 2)
                fin += "_____|_____|_____\n";
            else
                fin += "     |     |     \n";
        }
        System.out.println(fin);
    }

    public char checkWin() {
        for (int i = 0; i < board.length; i++)
        {
            if (board[i][0] == 'X' && board[i][1] == 'X' && board[i][2] == 'X')
                return 'X';
            if (board[i][0] == 'O' && board[i][1] == 'O' && board[i][2] == 'O')
                return 'O';
        }
        for (int i = 0; i < board.length; i++)
        {
            if (board[0][i] == 'X' && board[1][i] == 'X' && board[2][i] == 'X')
                return 'X';
            if (board[0][i] == 'O' && board[1][i] == 'O' && board[2][i] == 'O')
                return 'O';
        }
        if (board[0][0] == 'X' && board[1][1] == 'X' && board[2][2] == 'X')
            return 'X';
        if (board[0][0] == 'O' && board[1][1] == 'O' && board[2][2] == 'O')
            return 'O';
        if (board[0][2] == 'X' && board[1][1] == 'X' && board[2][0] == 'X')
            return 'X';
        if (board[0][2] == 'O' && board[1][1] == 'O' && board[2][0] == 'O')
            return 'O';

        for (int i = 0; i < board.length; i++)
        {
            for (int j = 0; j < board[i].length; j++)
            {
                if (board[i][j] == ' ')
                    return ' ';
            }
        }

        return 'Z';
    }

    public void reset() {
        for (int i = 0; i < board.length; i++)
        {
            Arrays.fill(board[i], ' ');
        }
        turn = 0;
    }

    public double[] getInputData(char i) {
        double[] spot = new double[9];
        char[][] l = getBoard();
        //System.out.println(Arrays.deepToString(game.getBoard()));
        int count = 0;
        for (char[] c : l) {
            for (char y : c) {
                if (y == i)
                    spot[count] = 1;
                else if (y == ' ')
                    spot[count] = 0;
                else
                    spot[count] = -1;
                count++;
            }
        }
        return spot;
    }
}
