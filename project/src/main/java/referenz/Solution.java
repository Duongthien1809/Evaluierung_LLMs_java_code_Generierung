package referenz;
class Solution {
    public int minSpeedOnTime(int[] dist, double hour) {
        int n = dist.length;
        double left = 1, right = 10000000;
        while (left <= right) {
            double mid = left + (right - left) / 2;
            double time = 0;
            for (int i = 0; i < n - 1; i++) {
                time += Math.ceil((double)dist[i] / mid);
            }
            time += (double)dist[n - 1] / mid;
            if (time <= hour) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        return left > 10000000 ? -1 : (int)left;
    }
}
