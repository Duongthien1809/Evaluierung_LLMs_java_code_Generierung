packages, int[][] boxes) {
        Arrays.sort(packages);
        Arrays.sort(boxes[0]);
        long[] prefix = new long[packages.length + 1];
        for(int i = 0;i < packages.length;++i){
            prefix[i + 1] = prefix[i] + packages[i];
        }
        long minWasted = Long.MAX_VALUE;
        for(int j = 0;j < boxes.length;++j){
            long wasted = 0;
            int head = 0, i = 0;
            while(i < packages.length){
                if(head >= boxes[j].length || packages[i] > boxes[j][head]){
                    wasted += boxes[j][head] - packages[i - 1];
                    head++;
                    i--;
                }else{
                    i++;
                    if(i < packages.length && packages[i] > boxes[j][head]){
                        wasted += boxes[j][head] - packages[i - 1];
                        head++;
                    }
                }
            }
            wasted += prefix[packages.length] - prefix[i];
            minWasted = Math.min(minWasted, wasted);
        }
        return (int)(minWasted % (1e9 + 7));
    }
}