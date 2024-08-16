package referenz;

import java.util.Arrays;

public class Solution {
    public int minSpeedOnTime(int[] dist, double hour) {
        int n = dist.length;
        // check if it's possible to be on time with the slowest train
        double minSpeed = (double)dist[n-1] / (hour - (n-1));
        if (minSpeed > 10000000) return -1; // the answer exceeds the limit
        // binary search for the minimum possible speed
        int left = 1, right = 10000000;
        while (left < right) {
            int mid = (left + right) / 2; // current speed
            double doubleTime = 0;
            for (int i = 0; i < n-1; i++) {
                doubleTime += Math.ceil((double)dist[i] / mid); // add travel time
            }
            doubleTime += (double)dist[n-1] / mid; // last train
            if (doubleTime > hour) left = mid + 1; // need lower speed, move to left side
            else right = mid; // speed of mid is possible, move to left side
        }
        return left;
    }
}