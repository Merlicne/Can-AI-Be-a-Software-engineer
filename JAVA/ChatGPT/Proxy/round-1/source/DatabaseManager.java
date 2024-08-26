import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
public class DatabaseManager<T> implements DatabaseOperations<T> {

    @Autowired
    private JpaRepository<T, Long> repository; // Assume a generic repository is injected

    @Override
    @Transactional
    public T create(T entity) {
        return repository.save(entity);
    }

    @Override
    @Transactional(readOnly = true)
    public T read(Long id) {
        Optional<T> entity = repository.findById(id);
        return entity.orElseThrow(() -> new RuntimeException("Entity not found"));
    }

    @Override
    @Transactional
    public T update(Long id, T entity) {
        if (!repository.existsById(id)) {
            throw new RuntimeException("Entity not found");
        }
        return repository.save(entity);
    }

    @Override
    @Transactional
    public void delete(Long id) {
        if (!repository.existsById(id)) {
            throw new RuntimeException("Entity not found");
        }
        repository.deleteById(id);
    }
}
