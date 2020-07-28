public class NeuralNet {
    private double[] weights = new double[10];
    private double[] weights2 = new double[10];
    public char turn;
    public NeuralNet(char c) {
        for (int i = 0; i < weights.length; i++)
        {
            weights[i] = Math.random() * 9;
            weights2[i] = Math.random() * 9;
        }
        turn = c;
    }
    public NeuralNet() {
        for (int i = 0; i < weights.length; i++)
        {
            weights[i] = Math.random() * 9;
            weights2[i] = Math.random() * 9;
        }
        turn = 'X';
    }

    public void setTurn(char x)
    {
        turn = x;
    }

    public double[] getWeights()
    {
        return weights;
    }
    public double[] getWeights2()
    {
        return weights2;
    }

    public void setWeights(double[] hecc)
    {
        weights = hecc;
    }
    public void setWeights2(double[] hecc)
    {
        weights2 = hecc;
    }

    public int guess(double[] inputs) {
        if (turn == 'X')
        {
            double sum = 0;
            for (int i = 0; i < weights.length && i < inputs.length; i++) {
                sum += inputs[i] * weights[i];
            }
            int output = activate(sum);
            if (sum == 0)
                return activate(weights[9]);
            while (inputs[(output-1)] != 0)
            {
                output += (int)(Math.random() * 3) - 1;
                if (output < 1) {
                    output = 2;
                }
                if (output > 9) {
                    output = 8;
                }
            }
            return output;
        }
        else
        {
            double sum = 0;
            for (int i = 0; i < weights2.length && i < inputs.length; i++) {
                sum += inputs[i] * weights2[i];
            }
            int output = activate(sum);
            if (sum == 0)
                return activate(weights2[9]);
            while (inputs[(output-1)] != 0)
            {
                output += (int)(Math.random() * 3) - 1;
                if (output < 1) {
                    output = 2;
                }
                if (output > 9) {
                    output = 8;
                }
            }
            return output;
        }
    }

    public NeuralNet crossover(NeuralNet x) {
        double[] mom = this.getWeights2();
        double[] dad = x.getWeights2();
        double[] sonw = new double[mom.length];
        NeuralNet son = new NeuralNet();
        int f = mom.length/2;
        for (int l = 0; l < mom.length; l++)
        {
            int ran = (int)(Math.random() * 2);

            if (ran == 0)
            {
                sonw[l] = mom[l];
            }
            else if (ran == 1)
                sonw[l] = dad[l];
            else
                sonw[l] = (mom[l] + dad[l]) / 2;
        }
        son.setWeights2(sonw);
        mom = this.getWeights();
        dad = x.getWeights();
        sonw = new double[mom.length];
        f = mom.length / 2;
        if (this.turn == 'O' && x.turn != 'O')
        {
            sonw = this.weights2;
        }
        else if (this.turn != 'O' && x.turn == 'O')
        {
            sonw = x.weights2;
        }
        else {
            for (int l = 0; l < mom.length; l++) {
                int ran = (int) (Math.random() * 2);

                if (ran == 0) {
                    sonw[l] = mom[l];
                } else if (ran == 1)
                    sonw[l] = dad[l];
                else
                    sonw[l] = (mom[l] + dad[l]) / 2;
            }
        }
        /*
        for (int i = 0; i < sonw.length; i++)
        {
            sonw[i] = Math.random() * 9;
        }
        */
        son.setWeights(sonw);
        return son;
    }

    public void mutate(double p) {
        for (int i = 0; i < weights.length; i++)
        {
            if (Math.random() <= p)
            {
                if (Math.random() * 2 < 1)
                    weights[i] += (Math.random()*2) - 1;
                else
                    weights[i] = Math.random() * 9;
            }
        }
    }

    private int activate(double n) {
        double d = (n+9)/2;
        int l = (int)d;
        if (l > 9)
        {
            return 9;
        }
        else if (l < 1)
        {
            return 1;
        }
        else
            return l;
    }
}
