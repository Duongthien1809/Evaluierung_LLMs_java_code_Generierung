package referenz;

public class Solution {
    public int minSpeedOnTime(int[] dist, double hour) {
        int left = 1;
        int right = 10000000; // Maximum possible speed

        while (left <= right) {
            int mid = left + (right - left) / 2;
            double totalTime = calculateTotalTime(dist, mid);

            if (totalTime <= hour) {
                right = mid - 1; // If current speed is possible, try for a lower speed
            } else {
                left = mid + 1; // If current speed is not enough, try for a higher speed
            }
        }

        return left; // 'left' will point to the minimum required speed
    }

    private double calculateTotalTime(int[] dist, int speed) {
        double totalTime = 0;
        for (int i = 0; i < dist.length; i++) {
            totalTime += Math.ceil((double) dist[i] / speed); // Calculate time for each train ride and round up
        }
        return totalTime;
    }
}