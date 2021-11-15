import java.util.HashMap;
import java.util.Scanner;

public class DuplicateWords {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		HashMap<String, Integer> map = new HashMap<String, Integer>();
		System.out.println("Enter a sentence:");
	    String input = sc.nextLine();
	    String[] pieces = input.split(" ");
	    String in = "";

	    for (String piece : pieces) {
            for (char c : piece.toCharArray()) {
            	if (Character.isWhitespace(c))
            		continue;
            	if (Character.isLetterOrDigit(c))
            		in += c;
            }
            in.toLowerCase();
	    if (map.containsKey(in))
	    	map.put(in, (map.get(in) + 1));
	    else
	    	map.put(in, 1);
	    in = "";
	    }
	
	System.out.printf("%nMap contains:%nKey\t\tValue%n");

    for (String key : map.keySet()) {
       System.out.printf("%-10s%10s%n", key, map.get(key));
    }
    
    sc.close();
	}
}
