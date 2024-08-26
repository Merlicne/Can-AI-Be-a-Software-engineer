// DatabaseProxyTest.java
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class DatabaseProxyTest {
    private DatabaseProxy databaseProxy;
    private RealDatabase realDatabase;

    @Before
    public void setUp() {
        realDatabase = mock(RealDatabase.class);
        databaseProxy = new DatabaseProxy();
    }

    @Test
    public void testCreate() {
        databaseProxy.create("Test Data");
        verify(realDatabase).create("Test Data");
    }

    @Test
    public void testRead() {
        when(realDatabase.read(1)).thenReturn("Data1");
        String data = databaseProxy.read(1);
        assertEquals("Data1", data);
        verify(realDatabase).read(1);
    }

    @Test
    public void testUpdate() {
        databaseProxy.update(1, "Updated Data");
        verify(realDatabase).update(1, "Updated Data");
    }

    @Test
    public void testDelete() {
        databaseProxy.delete(1);
        verify(realDatabase).delete(1);
    }
}