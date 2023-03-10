    'seguindo a logica do python usando double'
    static double sum(int n)
    {
      double i, s = 0.0;
      for (i = 1; i <= n; i++)
          s = s + 1/i;
      return s;
    }
 
    int n = 5;
    system.out.println(String.format("Resultado":, sum(n)))