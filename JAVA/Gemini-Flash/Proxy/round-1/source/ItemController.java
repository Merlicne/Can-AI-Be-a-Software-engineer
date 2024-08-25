import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class ItemController {

    @Autowired
    private DatabaseOperations databaseOperations;

    @PostMapping("/create")
    public ResponseEntity<Item> create(@RequestBody Item item) {
        Item createdItem = databaseOperations.create(item);
        return new ResponseEntity<>(createdItem, HttpStatus.CREATED);
    }

    @GetMapping("/read/{id}")
    public ResponseEntity<Item> read(@PathVariable Long id) {
        Item item = databaseOperations.read(id);
        if (item == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        return new ResponseEntity<>(item, HttpStatus.OK);
    }

    @PutMapping("/update/{id}")
    public ResponseEntity<Item> update(@PathVariable Long id, @RequestBody Item item) {
        if (!id.equals(item.getId())) {
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
        Item updatedItem = databaseOperations.update(item);
        return new ResponseEntity<>(updatedItem, HttpStatus.OK);
    }

    @DeleteMapping("/delete/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        databaseOperations.delete(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}