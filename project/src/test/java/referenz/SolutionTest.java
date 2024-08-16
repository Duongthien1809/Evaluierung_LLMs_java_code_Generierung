package referenz;


import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

import org.junit.jupiter.api.Test;

class SolutionTest {
    @Test
    void minSpeedOnTime() {
        assertThat(new Solution().minSpeedOnTime(new int[] {1, 3, 2}, 6), equalTo(1));
    }

    @Test
    void minSpeedOnTime2() {
        assertThat(new Solution().minSpeedOnTime(new int[] {1, 3, 2}, 2.7), equalTo(3));
    }

    @Test
    void minSpeedOnTime3() {
        assertThat(new Solution().minSpeedOnTime(new int[] {1, 3, 2}, 1.9), equalTo(-1));
    }
}

