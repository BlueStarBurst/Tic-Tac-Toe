import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class GameRunner {
    public static void main(String[] args) {
        TicTacToe game = new TicTacToe();
        Scanner in = new Scanner(System.in);
        int genz = 0;
        /*
        NeuralNet net = new NeuralNet('X');
        boolean end = false;
        while (!end)
        {
            double[] spot = new double[9];
            char[][] l = game.getBoard();
            System.out.println(Arrays.deepToString(game.getBoard()));
            int count = 0;
            for (char[] c : l)
            {
                for (char x: c)
                {
                    if (x == 'X')
                        spot[count] = 1;
                    else if (x == 'O')
                        spot[count] = -1;
                    count++;
                }
            }

            game.setNext(net.guess(spot));
            game.printBoard();
            System.out.println(net.guess(spot));
            char x = game.checkWin();
            if (x != ' ')
            {
                System.out.println(x + " has won!");
                break;
            }
            game.setNext(in.nextInt());
            game.printBoard();
            x = game.checkWin();
            if (x != ' ')
            {
                System.out.println(x + " has won!");
                break;
            }
        }


         */
        System.out.println("Would you like to...\n1.) Run Generations\n2.) Run a Specific Neural Net\n");
        int spec = in.nextInt();
        in.nextLine();
        NeuralNet net = new NeuralNet();
        if (spec == 2) {
            System.out.println("Please enter an array of weights:");
            String s = in.nextLine();
            //s = in.nextLine();
            System.out.println(s);
            s = s.substring(1,s.length()-1);
            String[] str = s.split(", ");
            double[] flip = new double[10];
            for (int u = 0; u < str.length; u++)
            {
                flip[u] = Double.parseDouble(str[u]);
            }
            net.setWeights(flip);
            System.out.println(Arrays.toString(net.getWeights()));

            System.out.println("Please enter another array of weights:");
            s = in.nextLine();
            System.out.println(s);
            s = s.substring(1,s.length()-1);
            str = s.split(", ");
            flip = new double[10];
            for (int u = 0; u < str.length; u++)
            {
                flip[u] = Double.parseDouble(str[u]);
            }
            net.setWeights2(flip);
            System.out.println(Arrays.toString(net.getWeights2()));
        }
        else {

            System.out.println("How many generations would you like to run?");
            genz = in.nextInt();
            ArrayList<NeuralNet> netlist = new ArrayList<NeuralNet>();
            NeuralNet[] hecc = new NeuralNet[100];

            for (int i = 0; i < hecc.length; i++) {
                if (i % 2 != 0)
                    hecc[i] = new NeuralNet('O');
                else
                    hecc[i] = new NeuralNet('X');
            }
            for (int b = 0; b < genz; b++) {
                netlist = new ArrayList<NeuralNet>();
                //for (int o = 0; o < 30; o++)
                    //System.out.println("Gen " + b);

                for (int i = 0; i < hecc.length; i += 2) {
                    //System.out.println("Game " + i);
                    NeuralNet net1 = hecc[i];
                    net1.setTurn('X');
                    NeuralNet net2 = hecc[i + 1];
                    net2.setTurn('O');
                    game.reset();
                    char win = ' ';
                    while (true) {
                        double[] spot = game.getInputData('X');

                        game.setNext(net1.guess(spot));
                        //System.out.println(net1.guess(spot));
                        char x = game.checkWin();
                        if (x != ' ') {
                            win = x;
                            break;
                        }
                        spot = game.getInputData('O');

                        game.setNext(net2.guess(spot));
                        //System.out.println(net1.guess(spot));
                        x = game.checkWin();
                        if (x != ' ') {
                            win = x;
                            break;
                        }
                    }
                    if (win == 'X') {
                        netlist.add(net1);
                        netlist.add(net1);
                        netlist.add(net1);
                    }
                    else if (win == 'O') {
                        netlist.add(net2);
                        netlist.add(net2);
                        netlist.add(net2);
                    }
                    else {
                        netlist.add(net2);
                        netlist.add(net1);
                    }
                }
                for (int i = 0; i < hecc.length; i++) {
                    hecc[i] = netlist.get((int) (Math.random() * netlist.size())).crossover(netlist.get((int) (Math.random() * netlist.size())));
                    hecc[i].mutate(0.05);
                }
            }
            netlist = new ArrayList<NeuralNet>();
            for (int i = 0; i < hecc.length; i++) {
                netlist.add(hecc[i]);
            }

            while (netlist.size() != 1)
            {
                NeuralNet net1 = netlist.get(0);
                net1.setTurn('X');
                NeuralNet net2 = netlist.get(1);
                net2.setTurn('O');
                game.reset();
                char win = ' ';
                while (true) {
                    double[] spot = game.getInputData('X');

                    game.setNext(net1.guess(spot));
                    //System.out.println(net1.guess(spot));
                    char x = game.checkWin();
                    if (x != ' ') {
                        win = x;
                        break;
                    }
                    spot = game.getInputData('O');

                    game.setNext(net2.guess(spot));
                    //System.out.println(net1.guess(spot));
                    x = game.checkWin();
                    if (x != ' ') {
                        win = x;
                        break;
                    }
                }
                if (win == 'X')
                    netlist.remove(net2);
                else
                    netlist.remove(net1);
            }



            game.reset();
            net = netlist.get(0);
            //System.out.println(Arrays.toString(net.getWeights()));
        }
        boolean end = false;
        while (!end)
        {
            double[] spot = game.getInputData('X');
            System.out.println(Arrays.deepToString(game.getBoard()));

            game.setNext(net.guess(spot));
            game.printBoard();
            System.out.println(net.guess(spot));
            char x = game.checkWin();
            if (x != ' ')
            {
                if (x == 'Z')
                {
                    System.out.println("It's a Tie!");
                    break;
                }
                System.out.println(x + " has won!");
                break;
            }
            game.setNext(in.nextInt());
            game.printBoard();
            x = game.checkWin();
            if (x != ' ')
            {
                if (x == 'Z')
                {
                    System.out.println("It's a Tie!");
                    break;
                }
                System.out.println(x + " has won!");
                break;
            }
        }
        System.out.println("Generation: " + genz + " = " +Arrays.toString(net.getWeights()) + "\n" + Arrays.toString(net.getWeights2()));

    }
}
