package referenz;

// #Medium #Array #Binary_Search #Binary_Search_II_Day_6
// #2022_05_10_Time_86_ms_(88.58%)_Space_100.1_MB_(51.38%)
public class Solution {
    public int minSpeedOnTime(int[] dist, double hour) {
        int left = 1;
        int right = 10000000; // Maximum possible speed

        while (left <= right) {
            int mid = left + (right - left) / 2;
            double timeTaken = calculateTime(dist, mid);

            if (timeTaken <= hour) {
                // If the current speed is possible, explore lower speeds
                right = mid - 1;
            } else { 
                // Need a higher speed
                left = mid + 1;
            }
        }

        return left; 
    }

    private double calculateTime(int[] dist, int speed) {
        double totalTime = 0;
        for (int distance : dist) {
            totalTime += Math.ceil((double) distance / speed); // ceil to account for waiting time
        }
        return totalTime;
    }
}