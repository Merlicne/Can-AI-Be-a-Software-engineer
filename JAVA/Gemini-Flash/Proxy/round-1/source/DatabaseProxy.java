import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class DatabaseProxy implements DatabaseOperations {

    private static final Logger logger = LoggerFactory.getLogger(DatabaseProxy.class);

    private final DatabaseOperations databaseOperations;

    public DatabaseProxy(DatabaseOperations databaseOperations) {
        this.databaseOperations = databaseOperations;
    }

    @Override
    public Item create(Item item) {
        logger.info("Creating item: {}", item);
        return databaseOperations.create(item);
    }

    @Override
    public Item read(Long id) {
        logger.info("Reading item with id: {}", id);
        return databaseOperations.read(id);
    }

    @Override
    public Item update(Item item) {
        logger.info("Updating item: {}", item);
        return databaseOperations.update(item);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting item with id: {}", id);
        databaseOperations.delete(id);
    }
}