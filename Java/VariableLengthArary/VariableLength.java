public class VariableLength {
	public static int product(int... num) {
		int total = 1;
		for (int n : num) {
			total = total * n;
			}
		return total;
	}
	
	public static void main(String args[]) {
		int a = 10, b = 10, c = 10, d = 40, e = 13, f = 27, g = 0;
		System.out.println("Test for product of 10 x 10 x 10");
		System.out.println(product(a, b, c));
		
		System.out.println("\nTest for product of 40 x 13 x 27");
		System.out.println(product(d, e, f));
		
		System.out.println("\nTest for product of 13 x 27 x 40");
		System.out.println(product(e, f, d));
		
		System.out.println("\nTest for product of 0 x 40 x 10");
		System.out.println(product(g, d, b));
	}
}