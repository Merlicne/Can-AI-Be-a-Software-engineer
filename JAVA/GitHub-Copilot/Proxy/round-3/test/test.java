// APITest.java
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class APITest {
    private API api;
    private DatabaseProxy databaseProxy;

    @Before
    public void setUp() {
        databaseProxy = mock(DatabaseProxy.class);
        api = new API();
    }

    @Test
    public void testCreateData() {
        api.createData("Test Data");
        verify(databaseProxy).create("Test Data");
    }

    @Test
    public void testReadData() {
        when(databaseProxy.read(1)).thenReturn("Data1");
        String data = api.readData(1);
        assertEquals("Data1", data);
        verify(databaseProxy).read(1);
    }

    @Test
    public void testUpdateData() {
        api.updateData(1, "Updated Data");
        verify(databaseProxy).update(1, "Updated Data");
    }

    @Test
    public void testDeleteData() {
        api.deleteData(1);
        verify(databaseProxy).delete(1);
    }
}