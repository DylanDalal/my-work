public class Invoice {
	private double price;
	private int quantity;
	private String description;
	private String partNumber;
	
	/* Constructor */
	
	public Invoice(double price, int quantity, String description, String partNumber) {
		this.price = price;
		this.quantity = quantity;
		this.description = description;
		this.partNumber = partNumber;
	}
	
	/* Getters and Setters */
	
	public double getPrice() {
		return price;
	} public void setPrice(double price) {
		this.price = price;
	}
	
	public int getQuantity() {
		return quantity;
	} public void setQuantity(int quantity) {
		this.quantity = quantity;
	}
	
	public String getDescription() {
		return description;
	} public void setDescription(String description) {
		this.description = description;
	}
	
	public String getPartNumber() {
		return partNumber;
	} public void setPartNumber(String partNumber) {
		this.partNumber = partNumber;
	}
	
	/* Methods */
	
	public double getInvoiceAmount() { 
		double invoiceAmount = quantity * price;
		return invoiceAmount;
	} 
}
