import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class DatabaseManager implements DatabaseOperations {

    @Autowired
    private ItemRepository itemRepository;

    @Override
    public Item create(Item item) {
        return itemRepository.save(item);
    }

    @Override
    public Item read(Long id) {
        return itemRepository.findById(id).orElse(null);
    }

    @Override
    public Item update(Item item) {
        return itemRepository.save(item);
    }

    @Override
    public void delete(Long id) {
        itemRepository.deleteById(id);
    }
}