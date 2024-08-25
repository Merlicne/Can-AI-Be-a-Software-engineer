import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/entities")
public class EntityController {

    @Autowired
    private DatabaseProxy<Entity> databaseProxy;

    @PostMapping("/create")
    public Entity create(@RequestBody Entity entity) {
        return databaseProxy.create(entity);
    }

    @GetMapping("/read/{id}")
    public Entity read(@PathVariable Long id) {
        return databaseProxy.read(id);
    }

    @PutMapping("/update/{id}")
    public Entity update(@PathVariable Long id, @RequestBody Entity entity) {
        return databaseProxy.update(id, entity);
    }

    @DeleteMapping("/delete/{id}")
    public void delete(@PathVariable Long id) {
        databaseProxy.delete(id);
    }
}
