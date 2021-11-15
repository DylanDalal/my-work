import java.security.SecureRandom;

public class SentenceMaker {
	static CharSequence[] article = {"the", "a", "one", "some", "any"};
	static CharSequence[] noun = {"boy", "girl", "dog", "town", "car"};
	static CharSequence[] preposition = {"to", "from", "over", "under", "on"};
	static CharSequence[] verb = {"drove", "jumped", "ran", "walked", "skipped"};
	static CharSequence[] toCap;
	
	
	public static void main(String[] args) {
		SecureRandom randomNumbers = new SecureRandom();
		StringBuilder sentence = new StringBuilder();
		
		for (int i = 0; i < 20; i++) {
			int a = randomNumbers.nextInt(5);
			int b = randomNumbers.nextInt(5);
			int c = randomNumbers.nextInt(5);
			int d =	randomNumbers.nextInt(5);
			int e = randomNumbers.nextInt(5);
			int f = randomNumbers.nextInt(5);
			
			sentence.append(article[a])		;
			sentence.append(" ");
			sentence.append(noun[b]);
			sentence.append(" ");
			sentence.append(verb[c]);
			sentence.append(" ");
			sentence.append(preposition[d]);
			sentence.append(" ");
			sentence.append(article[e]);
			sentence.append(" ");
			sentence.append(noun[f]);
			sentence.append(".");
			
			if (sentence.charAt(0) == 't')
				sentence.setCharAt(0, 'T');
			else if (sentence.charAt(0) == 'a')
				sentence.setCharAt(0, 'A');
			else if (sentence.charAt(0) == 'o')
				sentence.setCharAt(0, 'O');
			else if (sentence.charAt(0) == 's')
				sentence.setCharAt(0, 'S');
				
			System.out.println(sentence);
			sentence.setLength(0);
		}
		
	}
	
}
