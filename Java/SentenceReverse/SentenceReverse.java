import java.util.Scanner;

public class SentenceReverse {
	public static void main(String[] args) {
		System.out.println("Enter a sentence to be reversed: ");
		Scanner in = new Scanner(System.in);
		String input = in.nextLine();
		String piece = "";
		String[] pieces;

		for (int i = input.length() - 1; i >= 0; i--) {
			if (input.charAt(i) == ' ') {
				piece = input.substring(i, input.length());
				input = input.substring(0, i);
				piece = piece.substring(1, piece.length());
				System.out.print(piece);
				System.out.print(" ");
				
			}
		}
		System.out.print(input);
	}
}