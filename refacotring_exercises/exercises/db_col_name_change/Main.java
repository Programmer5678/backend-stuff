

// --- Entity / Model ---
class User {
    
    private final UserId id; // raw string
    private final String name;


    public User(UserId id, String name) {
        this.id = id;
        this.name = name;
    }

    public UserId getId() {
        return id;
    }

    public String getName() {
        return name;
    }
}

// --- Repository Layer ---
class UserRepository {

    // Simulate a DB with a map
    private final java.util.Map<Integer, User> db = new java.util.HashMap<>();

    public void save(User user) {
        db.put(user.getId().value(), user);
    }

    public User findById(UserId id) {
        return db.get(id.value());
    }
}

// --- Service Layer ---
class UserService {
    private final UserRepository repo;

    public UserService(UserRepository repo) {
        this.repo = repo;
    }

    public User getUser(UserId id)  {
        return repo.findById(id);
    }

    public void greetUser(UserId id) {
        User user = getUser(id);
        System.out.println("Got user with id=" + String.valueOf(id) + " - hello, " + user.getName() + "!");
    }
}

// --- Controller / API Layer ---
class UserController {
    private final UserService service;

    public UserController(UserService service) {
        this.service = service;
    }

    public void handleRequest(UserId id) {
        service.greetUser( id);
    }
}


class UserId {
    // private String value;
    private int value;

    private class Conversions{
        static String convertIntString(int i){
            return String.valueOf(i);
        }

        static int convertStringInt(String s){
            return Integer.parseInt(s);
        }
    }

    UserId(int value) {
        this.value = value;
    }


    int value() {
        return value;
    }
}

// --- Main / Test ---
public class Main {

    private static void test_body(UserRepository repo, UserService service, 
            UserController controller, UserId uid1, UserId uid2) {

            // --- Create users ---
            User user1 = new User(uid1, "Alice");
            User user2 = new User(uid2, "Bob");

            repo.save(user1);
            repo.save(user2);

            // --- Test old API ---
            controller.handleRequest( uid1 );
            controller.handleRequest( uid2 );
        } 

    public static void main(String[] args) {

        
        UserRepository repo = new UserRepository();
        UserService service = new UserService(repo);
        UserController controller = new UserController(service);

        UserId uid1 = new UserId(1);
        UserId uid2 = new UserId(2);

        test_body(repo, service, controller, uid1, uid2);
    }
}
