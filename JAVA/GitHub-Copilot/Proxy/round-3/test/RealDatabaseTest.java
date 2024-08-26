// RealDatabaseTest.java
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class RealDatabaseTest {
    private RealDatabase realDatabase;

    @Before
    public void setUp() {
        realDatabase = new RealDatabase();
    }

    @Test
    public void testCreate() {
        realDatabase.create("Test Data");
    }

    @Test
    public void testRead() {
        String data = realDatabase.read(1);
        assertEquals("Data1", data);
    }

    @Test
    public void testUpdate() {
        realDatabase.update(1, "Updated Data");
    }

    @Test
    public void testDelete() {
        realDatabase.delete(1);
    }
}