import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class CrudProxyApplication {

    public static void main(String[] args) {
        SpringApplication.run(CrudProxyApplication.class, args);
    }

    @Bean
    public DatabaseOperations databaseOperations() {
        return new DatabaseProxy(new DatabaseManager());
    }
}