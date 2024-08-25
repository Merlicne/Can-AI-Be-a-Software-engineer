import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

class DatabaseTest {
    private Database database;

    @BeforeEach
    void setUp() {
        database = new RealDatabase();
    }

    @Test
    void testCreate() {
        database.create("data");
        assertEquals("data", database.read(1));
    }

    @Test
    void testRead() {
        database.create("data");
        assertEquals("data", database.read(1));
    }

    @Test
    void testUpdate() {
        database.create("data");
        database.update(1, "newData");
        assertEquals("newData", database.read(1));
    }

    @Test
    void testDelete() {
        database.create("data");
        database.delete(1);
        assertNull(database.read(1));
    }

    @Test
    void testReadNonExistentRecord() {
        assertNull(database.read(999));
    }
}

class DatabaseProxyTest {
    private DatabaseProxy proxy;
    private RealDatabase realDatabase;

    @BeforeEach
    void setUp() {
        realDatabase = mock(RealDatabase.class);
        proxy = new DatabaseProxy(realDatabase);
    }

    @Test
    void testCreateDelegation() {
        proxy.create("data");
        verify(realDatabase).create("data");
    }

    @Test
    void testReadDelegation() {
        when(realDatabase.read(1)).thenReturn("data");
        assertEquals("data", proxy.read(1));
        verify(realDatabase).read(1);
    }

    @Test
    void testUpdateDelegation() {
        proxy.update(1, "newData");
        verify(realDatabase).update(1, "newData");
    }

    @Test
    void testDeleteDelegation() {
        proxy.delete(1);
        verify(realDatabase).delete(1);
    }

    @Test
    void testReadNonExistentRecord() {
        when(realDatabase.read(999)).thenReturn(null);
        assertNull(proxy.read(999));
    }
}

class APITest {
    private API api;
    private DatabaseProxy proxy;

    @BeforeEach
    void setUp() {
        proxy = mock(DatabaseProxy.class);
        api = new API(proxy);
    }

    @Test
    void testCreateData() {
        api.createData("data");
        verify(proxy).create("data");
    }

    @Test
    void testReadData() {
        when(proxy.read(1)).thenReturn("data");
        assertEquals("data", api.readData(1));
        verify(proxy).read(1);
    }

    @Test
    void testUpdateData() {
        api.updateData(1, "newData");
        verify(proxy).update(1, "newData");
    }

    @Test
    void testDeleteData() {
        api.deleteData(1);
        verify(proxy).delete(1);
    }

    @Test
    void testReadNonExistentRecord() {
        when(proxy.read(999)).thenReturn(null);
        assertNull(api.readData(999));
    }
}