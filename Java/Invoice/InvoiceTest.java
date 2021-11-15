public class InvoiceTest {
	public static void main(String[] args) {
		Invoice invoice1 = new Invoice(1.25, 2, "SourPatchKids", "55A");
		Invoice invoice2 = new Invoice(2.55, 5, "M&Ms", "88JJ");
		Invoice invoice3 = new Invoice(1.77, 3, "Twix", "577B");
		
		double total = ( invoice1.getInvoiceAmount() + invoice2.getInvoiceAmount() + invoice3.getInvoiceAmount() );
		
		System.out.printf("Your grand total will be %.2f", total);
	}
}