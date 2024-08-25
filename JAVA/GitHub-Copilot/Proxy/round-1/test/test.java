import static org.mockito.Mockito.*;
import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;
import org.mockito.*;

public class DatabaseProxyTest {

    @Mock
    RealDatabase realDatabase;

    @InjectMocks
    DatabaseProxy databaseProxy;

    @Before
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testCreate() {
        String data = "testData";
        databaseProxy.create(data);
        verify(realDatabase, times(1)).create(data);
    }

    @Test
    public void testRead() {
        int id = 1;
        String expectedData = "testData";
        when(realDatabase.read(id)).thenReturn(expectedData);
        String actualData = databaseProxy.read(id);
        assertEquals(expectedData, actualData);
        verify(realDatabase, times(1)).read(id);
    }

    @Test
    public void testUpdate() {
        int id = 1;
        String data = "updatedData";
        databaseProxy.update(id, data);
        verify(realDatabase, times(1)).update(id, data);
    }

    @Test
    public void testDelete() {
        int id = 1;
        databaseProxy.delete(id);
        verify(realDatabase, times(1)).delete(id);
    }

    @Test
    public void testReadNonExistentRecord() {
        int id = 999;
        when(realDatabase.read(id)).thenReturn(null);
        String actualData = databaseProxy.read(id);
        assertNull(actualData);
        verify(realDatabase, times(1)).read(id);
    }
}

public class APITest {

    @Mock
    DatabaseProxy databaseProxy;

    @InjectMocks
    API api;

    @Before
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testCreateData() {
        String data = "testData";
        api.createData(data);
        verify(databaseProxy, times(1)).create(data);
    }

    @Test
    public void testReadData() {
        int id = 1;
        String expectedData = "testData";
        when(databaseProxy.read(id)).thenReturn(expectedData);
        String actualData = api.readData(id);
        assertEquals(expectedData, actualData);
        verify(databaseProxy, times(1)).read(id);
    }

    @Test
    public void testUpdateData() {
        int id = 1;
        String data = "updatedData";
        api.updateData(id, data);
        verify(databaseProxy, times(1)).update(id, data);
    }

    @Test
    public void testDeleteData() {
        int id = 1;
        api.deleteData(id);
        verify(databaseProxy, times(1)).delete(id);
    }

    @Test
    public void testReadNonExistentRecord() {
        int id = 999;
        when(databaseProxy.read(id)).thenReturn(null);
        String actualData = api.readData(id);
        assertNull(actualData);
        verify(databaseProxy, times(1)).read(id);
    }
}