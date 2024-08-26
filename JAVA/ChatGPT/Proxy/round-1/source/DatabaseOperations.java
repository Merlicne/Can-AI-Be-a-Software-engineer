public interface DatabaseOperations<T> {
    T create(T entity);
    T read(Long id);
    T update(Long id, T entity);
    void delete(Long id);
}
