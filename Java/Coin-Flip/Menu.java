import java.security.SecureRandom;
import java.util.Scanner;

public class Menu {
	public static void main(String[] args) {
		Boolean run = true;
		Scanner input = new Scanner(System.in);
		double heads = 0, tails = 0;
		while (run) {
			System.out.println("Enter the number of the action you'd like to perform");
			System.out.println("1: Toss Coin");
			System.out.println("2: Display Results");
			System.out.println("3: Exit\n");
			int x = input.nextInt();
			if (x == 1) {
				Coin flipped = flip();
				if (flipped == Coin.HEADS) {
					System.out.println("\nHeads.\n");
					heads++;
				} else if (flipped == Coin.TAILS) {
					System.out.println("\nTails.\n");
					tails++;
				} 
			} else if (x == 2) {
				System.out.printf("\nResults \nHeads: %.0f \nTails: %.0f\n\n", heads, tails);
			} else if (x == 3) {
				System.out.println("\nThanks for playing!");
				run = false;
			}
		}
	} 
	
	public static Coin flip() {
		SecureRandom randomNumbers = new SecureRandom();
		int randomValue = randomNumbers.nextInt(2);
		if (randomValue == 0) {
			return Coin.HEADS;
		} else if (randomValue == 1) {
			return Coin.TAILS;
		} else {
			return Coin.HEADS; //will never be used but avoids compiler errors
		}
	}
	
}
