package referenz;
import java.util.Arrays;

class Solution {
    public int minSpeedOnTime(int[] dist, double hour) {
        int n = dist.length;
        int left = 1, right = (int)1e7; // maximum speed is 10^7 km/h
        while (left < right) {
            int mid = (left + right) / 2;
            double time = 0.0;
            for (int i = 0; i < n - 1; i++) {
                time += Math.ceil((double)dist[i] / mid);
            }
            time += (double)dist[n - 1] / mid;
            if (time <= hour) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left <= (int)1e7 ? left : -1;
    }
}


