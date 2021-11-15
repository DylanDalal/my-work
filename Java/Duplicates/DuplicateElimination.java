import java.util.HashSet;
import java.util.Scanner;
	
public class DuplicateElimination {
	public static void main(String[] args) {
		HashSet<String> set = new HashSet<String>();
		Scanner sc = new Scanner(System.in);
		String name = "";
		String quit = "quit";
	
		System.out.println("Enter a series of first names; type 'quit' to stop.");
		while (!(name.equals(quit))) {
			name = sc.nextLine(); 
			set.add(name.toLowerCase());
		}
		
		name = "";
		System.out.println("Search for a first name; type 'quit' to stop.");
		//it doesn't say to put this in a loop but i thought it might be helpful
		while (!(name.equals(quit))) {
			name = sc.nextLine();
			if (set.contains(name.toLowerCase())) 
				System.out.println("The set contains " + name + ".");
			else
				System.out.println("The set does not contain " + name + ".");
		}
		sc.close();
	}
}
