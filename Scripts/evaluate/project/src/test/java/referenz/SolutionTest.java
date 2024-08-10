import org.junit.Test;
import static org.junit.Assert.*;

public class SolutionTest {
    @Test
    public void testGetNumberOfBacklogOrders() {
        Solution solution = new Solution();
        assertEquals(6, solution.getNumberOfBacklogOrders(new int[][]{{10, 5, 0}, {15, 2, 1}, {25, 1, 1}, {30, 4, 0}}));
    }
}
