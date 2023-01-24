    for x = 1:10 {
        sqrt_x = 1;
        for i = 1:10000 {
            sqrt_x = (sqrt_x + x / sqrt_x) / 2;
        }
        print [x , sqrt_x];
    }